from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Weapon, Armor
from classes import UnitClass
from random import uniform
from typing import Optional


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
        self.stamina -= self.weapon.stamina_per_hit
        unit_damage = self.weapon.damage * self.unit_class.attack

        if target.stamina < target.armor.stamina_per_turn:
            target_armor = 0
        else:
            target.stamina -= target.armor.stamina_per_turn
            target_armor = target.armor.defence * target.unit_class.armor

        damage = round(unit_damage - target_armor)
        target.get_damage(damage)

        return damage

    def get_damage(self, damage: int) -> Optional[int]:
        if self.hp > damage:
            self.hp -= damage
            return damage
        return 0


    def hit(self, target: BaseUnit) -> str:
        if self.stamina >= self.weapon.stamina_per_hit:
            if self._count_damage(target) > 0:
                return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {self._count_damage(target)} урона."
            else:
                return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        else:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        if not self._is_skill_used:
            if self.unit_class.skill._is_stamina_enough:
                self._is_skill_used = True
            return self.unit_class.skill.use(user=self, target=target)
        else:
            return 'Навык уже использован'

    def add_stamina(self, stamina_point):
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
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """

        if uniform(1, 100) in range(1, 10) and not self._is_skill_used:
            return self.use_skill(target)
        return super().hit(target)
