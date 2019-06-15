import pygame

class Ship():
	"""docstring for Ship"""
	def __init__(self, ai_settings ,screen):
		""" Initialization spaceship"""
		self.screen = screen
		self.ai_settings = ai_settings
		#Ships img
		self.image = pygame.image.load('img/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		# Каждый новый корабль появляется внизу экрана
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom

		#Сохранение веще твенной координаты
		self.center = float(self.rect.centerx)
		#Flag moving
		self.moving_right = False
		self.moving_left = False

	def update(self):
		""" Обновление корабля с учетом флага """
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor

		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
		self.rect.centerx = self.center
	def blitme(self):
		""" Рисует корабль в  текущей позиции """
		self.screen.blit(self.image, self.rect)

	def center_ship(self):
		""" Размещает корабль в центре нижней стороне  """
		self.center = self.screen_rect.centerx
		


