from unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        """
        Запуск игры.
        """
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):
        """
        Результат боя в зависимости от здоровья игроков.
        """
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = 'Ничья.'
            return self._end_game()
        elif self.player.hp <= 0:
            self.battle_result = 'Вы проиграли.'
            return self._end_game()
        elif self.enemy.hp <= 0:
            self.battle_result = 'Вы победили.'
            return self._end_game()

    def _stamina_regeneration(self):
        """
        Восстановление выносливости.
        """
        self.player.add_stamina(self.STAMINA_PER_ROUND)
        self.enemy.add_stamina(self.STAMINA_PER_ROUND)

    def next_turn(self):
        """
        Следующий ход в зависимости от здоровья игроков.
        """
        result = self._check_players_hp()
        if result:
            return result
        self._stamina_regeneration()
        return self.enemy.hit(self.player)

    def _end_game(self):
        """
        Конец боя.
        """
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self):
        """
        Удар.
        """
        result = self.player.hit(self.enemy)
        self.next_turn()
        return result

    def player_use_skill(self):
        """
        Применение умения.
        """
        result = self.player.use_skill(self.enemy)
        self.next_turn()
        return result
