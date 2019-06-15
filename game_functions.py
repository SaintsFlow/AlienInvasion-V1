import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """ нажатие клавиш """
    if event.key == pygame.K_RIGHT:
        # Move right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move right
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
        # Создание новой пули и включение е в группу bullets
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullets(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """ отпускание клавиш """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    # mouse and keyboard  checking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, 
							bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, 
						bullets, mouse_x, mouse_y):
	""" Запускает новую игру при нажатии Play """
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if  button_clicked and not stats.game_active:
		# Сброс игровых настроек.
		ai_settings.initialize_dynamic_settings()

		#Указатель мыши скрывается
		pygame.mouse.set_visible(False)
		# Сброс статистики 
		stats.reset_stats()

		#Очистка списка пришельцев и пуль
		aliens.empty()
		bullets.empty()

		#Создание нового флота и размещение корабля
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
		stats.game_active = True

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Обновляет позиции пуль и удаляет старые пули."""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        check_bullet_alien_collision(
            ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """ Обработка колизий пуль  """
    # Проверка попаданий в пришельцев.
    # При обнаружении попадания удалить пулю и пришельца.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)
    """ Уничтожение существующих пульи создание нового флота """
    if (len(aliens) == 0):
		#Уничтожение пель, повышение скорости и создание новго флота
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

def check_high_score(stats, sb):

    """Проверяет, появился ли новый рекорд."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()



def create_fleet(ai_settings, screen, ship, aliens):
    """ Создание флота  """
    # Создание пришельца и вычисление колл-ва пришельцев в ряду
    # Интервал между соседними пришельцами

    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(
        ai_settings, ship.rect.height, alien.rect.height)

    # Создание флота
    for row_number in range(number_rows):
        # Создание первого ряда пришльцев
        for alien_number in range(number_aliens_x):
            # Создание пришельца и размещение в ряду
            alien = Alien(ai_settings, screen)
            alien.x = alien_width + 2 * alien_width * alien_number
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
            alien.rect.x = alien.x
            aliens.add(alien)


def get_number_aliens_x(ai_settings, alien_width):
    """ Вычисляет кол-во пришельцев в ряду """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """ Создает пришельца и размещает его в ряду """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def check_fleet_edges(ai_settings, aliens):
    """ Checks the edges of aliens """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """ Проверяет добралдись ли пришельцы до нижнего края экрана """
    screen_rect = screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >= screen_rect.bottom:
            # То же что и при столкновении с кораблем
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def change_fleet_direction(ai_settings, aliens):
    """ Drops the feelt down and changes the direction """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """ Обрабатывает столкновение корабля с пришельцем """
    if stats.ships_left > 0:
                # Уменьшение ships_left
        stats.ships_left -= 1
        # Очистка списков пришульцев и пуль
        aliens.empty()
        bullets.empty()
        # Создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        stats.reset_stats()
        # Пауза
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """ Checks if the fleet got to the edge
                then updates the position """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Проверка колизии пришелец-корабль
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # screen.fill(bg_color)
    screen.fill(ai_settings.bg_color)

    # Все пули выводятся позади изображений корабля и пришельцев
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    #Вывод счета
    sb.show_score()
    # Кнопка Play отображается при неактивной игре
    if not stats.game_active:
        play_button.draw_button()
    # Отображение последнего прорисованного экрана
    pygame.display.flip()
