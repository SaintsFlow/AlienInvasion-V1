class GameStats():
    """ Отслеживание статистики """

    def __init__(self, ai_settings):
        """  Инициалитзирует статистику"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Игра запрускается в активном состоянии
        self.game_active = False
        # Рекорд
        self.high_score = 0

    def reset_stats(self):
        """ Инициализирует статистику изменяюшуюся в течение игры """
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
