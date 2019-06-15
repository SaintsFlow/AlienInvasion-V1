class Settings():
    """Setting for Alien Invasion"""

    def __init__(self):
        """ Game Settings """
        # Screen parametr

        self.screen_width = 1340
        self.screen_height = 900
        self.bg_color = (230, 230, 230)

        # Ship setting
        self.ship_speed_factor = 1
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed_factor = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 5

        # Alien settings
        self.alien_speed_factor = 1

        # Fleet settings
        # self.fleet_drop_speed = 5 sets the speed of fleet droping down
        self.fleet_drop_speed = 5

        # Темп ускорения игры
        self.speedup_scale = 1.1
		# Темп роста стоимости пришельца 
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
        # fleet_direction = 1 means that fleet is moving right if set -1 will move left
        self.fleet_direction = 1

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 2
        # fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1
		# Подсчет очков
        self.alien_points = 20



    def increase_speed(self):
        """Увеличивает настройки скорости."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
