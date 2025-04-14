from orbat_gen.powerpoint_gen import *
from datetime import datetime

def main() :
    start = datetime.now()
    source_file = "./datas/datas.xls"
    path_prs = "./results/presFull.pptx"

    dic_units = gen_units(source_file)
    categ = ['UAV', 'MBT', 'IFV', 'AD', 'FA', 'MRL']

    orbat_generator(dic_units, path_prs, categories = categ, start_column='++', table_equip=2, deep=True, flag = True)

    print(datetime.now()-start)

if __name__ == "__main__":
    main()