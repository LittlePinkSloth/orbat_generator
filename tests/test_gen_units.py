#python -m unittest discover -s tests

import unittest
from orbat_gen.units_gen import gen_units

class TestUnitsGen(unittest.TestCase):

    def setUp(self):
        #path to file test
        self.test_file = "tests/test_units.xlsx"

    def test_gen_units_output(self):
        units_dict = gen_units(self.test_file)

        #verify if 22AA Test is in the dictionnary at the good ech
        self.assertIn("22 AA TEST", units_dict["XXXX"])

        #verify if the objects has the good class
        from orbat_gen.classes import Unit
        self.assertIsInstance(units_dict["XXXX"]["22 AA TEST"], Unit)

        print(units_dict)

    def test_empty_file(self):
        #verify if an empty file returns empty dics
        empty_file = "tests/test_empty.xlsx"
        units_dict = gen_units(empty_file)
        for echelon in units_dict:
            self.assertEqual(units_dict[echelon], {})



if __name__ == '__main__':
    unittest.main()
