class UnitConfig :
    echelons = {'++': ('command',),
                'XXXXX': ('army group',),
                'XXXX': ('army', 'combined arms army', 'CAA', 'armee', 'armee interarme'),
                'XXX': ('army corps', 'corps', 'AC'),
                'XX': ('division', 'DIV'),
                'X': ('brigade', 'BDE', 'BRI'),
                'III': ('regiment', 'RGT', 'REG'),
                'II': ('battalion', 'bataillon', 'BN', 'BON', 'BION', 'BAT'),
                'I': ('company', 'battery', 'compagnie', 'batterie', 'CIE', 'COY', 'BTY'),
                'ooo': ('platoon', 'section', 'SCT', 'SION', 'PLT'),
                }

    sidc_csv = 'datas/sidc.csv'

class EquipConfig :
    eqp_csv = "./datas/EquipmentType.csv"

class PowerpointConfig :
    images_path = './datas/SYMB_PNG/'
    title_top = 20
    title_left = 130
    txt_w = txt_h = 20  # default size
    pos_unite_parent_left = 173
    pos_unite_parent_top = 71
    table_type_left = 280
    table_type_top = 77
    pos_unite_child_top = 200
    pos_unite_child_left = 20
    val_dec_right = 105
    val_dec_bot = 100
    title_size = 28
    drap_left = 20
    drap_top = title_top
    drap_high = 50
    val_dec_tbl = 16
    dec_child_bot = 120
    jump: int = 6  # number of units on the same line
    default_coeff = {'++': 1.3,
                     'XXXXXX': 1.3,
                     'XXXXX': 1.3,
                     'XXXX': 1.3,
                     'XXX': 1.2,
                     'XX': 1.1,
                     'X': 1,
                     'III': 1,
                     'II': 0.9,
                     'I': 0.9,
                     'ooo': 0.9,
                     'oo': 0.9
                     }