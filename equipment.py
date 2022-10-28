import json
from dataclasses import dataclass
from random import uniform
from typing import List

import marshmallow
import marshmallow_dataclass


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        '''
        Выбор урона оружия случайным порядком в диапазоне мин - макс урон.
        '''
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Weapon:
        '''
        Вооружение персонажа.
        '''
        return next(filter(lambda w: w.name == weapon_name, self.equipment.weapons))

    def get_armor(self, armor_name) -> Armor:
        '''
        Экипировка персонажа бронёй.
        '''
        return next(filter(lambda a: a.name == armor_name, self.equipment.armors))

    def get_weapons_names(self) -> list:
        '''
        Список доступного оружия.
        '''
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> list:
        '''
        Список доступной брони.
        '''
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        with open("./data/equipment.json", 'r', encoding='utf-8') as equipment_file:
            data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
