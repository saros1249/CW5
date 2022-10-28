from __future__ import annotations

from abc import ABC, abstractmethod
from random import uniform
from typing import Optional

from classes import UnitClass


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        """
        Логика боя. Расчет урона, защиты и уменшение выносливости.
        """
        self.stamina -= self.weapon.stamina_per_hit
        unit_damage = self.weapon.damage * self.unit_class.attack

        if target.stamina < target.armor.stamina_per_turn:
            target_armor = 0
        else:
            target.stamina -= target.armor.stamina_per_turn
            target_armor = target.armor.defence * target.unit_class.armor

        self.damage = unit_damage - target_armor
        target.get_damage(self.damage)
        print(self.damage)
        return self.damage

    def get_damage(self, damage):
        """
        Уменьшение очков здоровья.
        """
        if damage > 0:
            self.hp -= damage
            return round(damage, 1)
        return 0

    def hit(self, target: BaseUnit) -> str:
        """
        Вывод результатов ударов и защиты.
        """
        if self.stamina >= self.weapon.stamina_per_hit:
            if self._count_damage(target) > 0:
                return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {self.damage} урона."
            else:
                return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        else:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

    def use_skill(self, target: BaseUnit) -> str:
        """
        Метод использования умения.
        Если умение уже использовано возвращаем строку
        'Навык использован'
        """
        if not self._is_skill_used:
            if self.unit_class.skill._is_stamina_enough:
                self._is_skill_used = True
            return self.unit_class.skill.use(user=self, target=target)
        else:
            return 'Навык уже использован'

    def add_stamina(self, stamina_point):
        '''
        Восстановление выносливости.
        '''
        stamina_growth = stamina_point * self.unit_class.stamina
        if self.stamina + stamina_growth > self.unit_class.max_stamina:
            self.stamina = self.unit_class.max_stamina
        else:
            self.stamina += stamina_growth


class PlayerUnit(BaseUnit):
    pass


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар соперника
        Содержит логику применения соперником умения.
        """

        if uniform(1, 100) in range(1, 10) and not self._is_skill_used:
            return self.use_skill(target)
        return super().hit(target)
