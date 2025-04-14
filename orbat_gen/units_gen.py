from .classes import *
from pandas import read_excel
from .config import EquipConfig, UnitConfig


def init_equipment_dict() -> (dict, set):
    """
    Initialize all the Equipments from the csv file. If one equipment is missing, please add it in the csv file.
    :return: a list of all Equipment objects and a set of all different equipment category
    """
    eq_list = {}
    categ_list = []
    try:
        equips = read_csv(EquipConfig.eqp_csv, sep=";")
        for i in range(len(equips)) :
            obj = EquipmentType(name = equips['equipment'][i], category=equips['equipment_type'][i])
            eq_list[obj.name] = obj
            categ_list.append(equips['equipment_type'][i])

    except FileNotFoundError as e:
        print(e)
        exit('Please verify the presence of the EquipmentType.csv file in the orbat_gen package.')

    set_cat = set(categ_list)
    return eq_list, set_cat

#default list and category set
equip_list, category_set = init_equipment_dict()

def gen_units(file : str, equipments : dict = equip_list) -> dict :
    """
    Build all the units and their hierarchical links from the datas contained in the file.
    :param file: path to the excel file containing datas
    :param equipments: dict containing all the item objects. By default, use the dict generated when the script launches.
    :return: dict containing all the units stored in dicts corresponding to the echelon. {echelon : {unit.name : unit}}
    """

    #specific configs for tests : have to be less specific at the end : drop column only exists in test sample...
    col_names = list(UnitConfig.echelons.keys())
    col_names.append('equipment')
    col_names.append('nb')

    datas = read_excel(file, names=col_names, nrows=10000, skiprows=1, na_filter=True, index_col=False).fillna(
        '')

    dico_full = {name: {} for name in col_names[:10]}
    #Read datas line by line :
    for index, row in datas.iterrows():
        for col_idx, col in enumerate(datas.columns[:10]):
            if row[col] == '':
                continue

            value = row[col]

            #Creates the unit if it does not exist
            if value not in dico_full[col]:
                dico_full[col][value] = Unit(value, col)

            unit = dico_full[col][value]
            #____EQUIPMENT SETTING___________________________________________
            eq, nb = '', 0
            if datas['equipment'][index] != '' and datas['nb'][index] != '' :
                eq = datas['equipment'][index]
                try :
                    nb = int(datas['nb'][index])
                except ValueError :
                    nb = 0
            equip = equipments.get(eq)
            if equip :
                unit.add_equipment(equip, nb)

            #____PARENTS SETTING_____________________________________________
            if col_idx > 0:
                for prev_col_idx in range(col_idx - 1, -1, -1):  #right to left
                    prev_col = datas.columns[prev_col_idx]
                    parent_value = row[prev_col]

                    if parent_value != '':
                        parent_unit = dico_full[prev_col].get(parent_value)

                        if parent_unit:
                            unit.set_sup(parent_unit)
                        break  #stops when a parent is found
    return dico_full
