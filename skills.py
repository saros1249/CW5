from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unit import BaseUnit


class SkillABC(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass


class Skill(SkillABC):
    """
    Базовый класс умения
    """

    user = None
    target = None
    name = None
    stamina = None
    damage = None

    def skill_effect(self) -> str:
        """
        Вывод результата применения умения.
        """
        self.user.stamina -= self.stamina
        self.target.get_damage(round(self.damage, 1))
        return f"{self.user.name} использует {self.name} и наносит {round(self.damage, 1)} урона сопернику."

    def _is_stamina_enough(self):
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        """
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Применение умения.
        """
        self.user = user
        self.target = target
        if self._is_stamina_enough:
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class FuryPunch(Skill):
    name = 'Свирепый пинок'
    stamina = 6
    damage = 12


class HardShot(Skill):
    name = 'Мощный укол'
    stamina = 5
    damage = 15
