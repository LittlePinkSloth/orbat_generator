from pandas import read_csv
from .config import UnitConfig

class WrongFormat(Exception) :
    def __str__(self):
        return "The file cannot be used."

class EquipmentType :
    def __init__(self, name : str, category : str = None) :
        """
        Stores all type of equipment from the ORBAT in.
        :param name: the common name of the equipment
        :param category: describe the combat role of the equipement. For example : AD (Air Defense), MBT... Should be acronym.
        """
        self.name = name
        self.category = category

    def __str__(self):
        return self.name + ' : ' + self.category

    def __repr__(self):
        return self.name + ' : ' + self.category

    def __hash__(self):
        """
        Defines an hash to the object.
        :return: object's name to garanty the object's hash
        """
        return hash(self.name)

    def __eq__(self, other):
        """
        Defines how 2 objects of the class can be considered as equals.
        :param other: the class of any object to compare
        :return: True if both objects are the same class and the same name, else false
        """
        return isinstance(other, EquipmentType) and self.name == other.name





class Unit :
    def __init__(self, name : str, ech : str):
        self.name = name
        self.number = self.init_number()
        self.ech = self.init_ech(ech)
        self.equipments = {}
        self.sup = None
        self.sub = []
        self.sidc = self.init_sidc()

    def __str__(self):
        sep = ' / '
        sup = 'None'
        try :
            sup = self.sup.name
        except AttributeError :
            pass

        return self.name + sep + self.ech + sep + 'sup : ' + sup + sep + 'nb sub : ' + str(len(self.sub)) + sep + 'nb diff equipment : ' + str(len(self.equipments))

    def __repr__(self):
        return f"Unit({self.name}, echelon={self.ech})"

    def __hash__(self):
        """
        Defines an hash to the object.
        :return: object's name to garanty the object's hash
        """
        return hash(self.name)

    def __eq__(self, other):
        """
        Defines how 2 objects of the class can be considered as equals.
        :param other: the class of any object to compare
        :return: True if both objects are the same class and the same name, else false
        """
        return isinstance(other, Unit) and self.name == other.name

    def init_sidc(self):
        """
        Set the sidc number to the unit. If no SIDC correspond, set a default sidc.
        :return: sidc code
        """

        try :
            sidcs = read_csv(UnitConfig.sidc_csv, sep=';')
            n = len(sidcs.columns)
            if n < 2: raise WrongFormat
            sidcs.columns = [str(i) for i in range(len(sidcs.columns))]
            for i in range(n-1) :
                for typ, line in zip(sidcs[str(i)], range(len(sidcs))) :
                    if typ.lower() in self.name.lower() :
                        return sidcs[str(n-1)][line]
            #si on arrive jusqu'ici, c'est que le sidc n'a pas été trouvé : on met celui par défaut
            return 'SHGPU-----'
        except (FileNotFoundError, WrongFormat) as e :
            print(e, 'Default sidc set.', sep='\n')
            return 'SHGPU-----'
        except Exception as e:
            print(e.__class__.__name__, e, sep=' : ')
            print(e, 'Default sidc set.', sep='\n')
            return 'SHGPU-----'


    def init_number(self):
        """
        Extracts the unit number from the unit name.
        :return: unit number or None
        """
        splited = self.name.split()
        for part in splited :
            if part.isdigit() :
                return part

        return None

    @staticmethod
    def init_ech(ech : str) :
        """
        Replace a litteral echelon with its symbole (ex : brigade is X, army corps is XXX)
        :param ech: litteral echelon, or symbole, or acronym echelon (ie DIV, CAA..)
        :return: symbol echelon
        """
        if ech in UnitConfig.echelons.keys() : return ech
        for key, echelon in UnitConfig.echelons.items() :
            if ech.lower() in [ech.lower() for ech in echelon] :
                return key

    def add_equipment(self, equip : EquipmentType, nb : int = 0):
        """
        Method that adds an equipment in the unit equipment list in the equipment is not yet in the list.
        :param equip: equipment to add in the unit inventory : class EquipmentType
        :param nb: dotation of the unit in this specific equipments
        :return: nothing. Just att the equipment in the list, or does nothing
        """
        if equip not in self.equipments :
            self.equipments[equip] = nb
        else :
            self.equipments[equip] += nb

    def add_sub(self, sub):
        """Methods that ads a subordinate unit to the current unit sub list, if not already in."""
        if sub not in self.sub :
            self.sub.append(sub)

    def set_sup(self, sup):
        """Methods that set up the unit's superior unit.
        Once done, add the current unit to its superior's (newly setted) sub list."""
        self.sup = sup
        sup.add_sub(self)

    def count_category(self, cat_set : set|list|tuple) -> dict:
        """Methods that sums all the material in different equipement categories and return the results as a dictionnary
        :param cat_set: iterable that contains the category you want to sum the number of equipments.
        :return: a dictionnary {category : sum}
        """
        dico = {cat : 0 for cat in cat_set}
        for eq, nb in self.equipments.items() :
            if eq.category in dico.keys() : dico[eq.category] += nb
        return dico



