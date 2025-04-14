#python -m unittest discover -s tests

import unittest
from orbat_gen.classes import Unit, EquipmentType


class TestUnitModel(unittest.TestCase):

    def setUp(self):
        self.unit = Unit("Alpha", "XXX")
        self.sub_unit = Unit("Bravo", "XX")
        self.equipment = EquipmentType("Rifle")

    def test_unit_creation(self):
        self.assertEqual(self.unit.name, "Alpha")
        self.assertEqual(self.unit.ech, "XXX")
        self.assertEqual(len(self.unit.sub), 0)

    def test_add_supunit(self):
        self.sub_unit.set_sup(self.unit)
        self.assertIn(self.sub_unit, self.unit.sub)
        self.assertEqual(self.sub_unit.sup, self.unit)

    def test_add_equipment(self):
        self.unit.add_equipment(self.equipment, 1)
        self.assertIn(self.equipment, self.unit.equipments)
        self.assertEqual(self.unit.equipments[self.equipment], 1)

    def test_add_multiple_equipment(self):
        self.unit.add_equipment(self.equipment, nb=3)
        self.assertEqual(self.unit.equipments[self.equipment], 3)

    def test_eq_and_hash(self):
        unit_copy = Unit("Alpha", "XXX")
        self.assertEqual(self.unit, unit_copy)
        self.assertEqual(hash(self.unit), hash(unit_copy))


if __name__ == '__main__':
    unittest.main()
