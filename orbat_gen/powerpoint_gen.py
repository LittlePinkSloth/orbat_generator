from pptx.slide import Slide
import os
from .units_gen import *
from pprint import pprint
from pptx import *
from pptx.util import *
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from .config import PowerpointConfig

def set_size(coeff : float = 1.0) -> tuple :
    """
    Determines the height of the unit app6 and the text size
    :param coeff: the weight of unit echelon (example, div > bde > rgt...)
    :return: a tuple containing all dimensions : (img height, text echelon size, text unit nb size)
    """
    height = 60.0 * coeff
    text_size = 20
    paragraphe1_size = 2 / 3 * height
    return height, text_size, paragraphe1_size

def insert_app6(slide : Slide, unit : Unit, pos_left : float, pos_top : float) -> None:
    """
    Inserts unit's app6 symbole on a ppt slide at the specified position.
    :param slide: ppt slide where to add the app6 symbole
    :param unit: from class Unit
    :param pos_left: absolute distance from left
    :param pos_top: obsolute distance from top
    :return: None
    """

    coeff = PowerpointConfig.default_coeff.get(unit.ech)
    if not coeff : coeff = 1

    symb_ech = unit.ech

    #size settings
    text_height = text_width = Pt(60)  #default value
    img_hauteur, text_size, p_hauteur = set_size(coeff)


    #position settings
    top = Pt(pos_top)
    left = Pt(pos_left)

    #text area creation
    txbox = slide.shapes.add_textbox(left, top, text_width, text_height)
    unit_text = txbox.text_frame
    #paragraph settings
    unit_text.add_paragraph()
    unit_text.add_paragraph()
    unit_text.paragraphs[0].text = "       " + symb_ech
    unit_text.paragraphs[1].text = ""  #img place
    unit_text.paragraphs[2].text = unit.number if unit.number else unit.name

    #txt settings
    unit_text.paragraphs[0].font.size = unit_text.paragraphs[2].font.size = Pt(text_size)
    unit_text.paragraphs[1].font.size = Pt(p_hauteur)  #img place

    #img position settings
    img_top = Pt(pos_top + 27)
    img_left = Pt(pos_left + 14)

    #img choice
    unit_sidc = unit.sidc
    img_path = PowerpointConfig.images_path + unit_sidc + '.png'
    if os.path.exists(img_path):
        pass
    else:
        img_path =  PowerpointConfig.images_path + 'SHGPU-----.png'

    #add img
    pic = slide.shapes.add_picture(img_path, img_left, img_top, height=Pt(img_hauteur))

    #entities txt+img grouping
    list_shape = [txbox, pic]
    slide.shapes.add_group_shape(shapes=list_shape)

def format_cell(cell, text: str, font_size = 6, bold=False, font_color=RGBColor(0, 0, 0), fill_color=RGBColor(200, 200, 200)) -> None :
    """
    Apply consistent formatting to a PPT table cell.
    :param cell: ppt table cell to format
    :param text: text to insert in the cell
    :param font_size: size of the text
    :param bold: if bold or not
    :param font_color: color of the txt in RGBColor(r, g, b)
    :param fill_color: color of the cell background in RGBColor(r, g, b)
    :return: None
    """

    txt_frame = cell.text_frame
    txt_frame.clear()  #Clear any existing content
    txt_frame.text = text

    for paragraph in txt_frame.paragraphs:
        for run in paragraph.runs:
            run.font.size = Pt(font_size)
            run.font.bold = bold
            run.font.color.rgb = font_color

    cell.fill.solid()
    cell.fill.fore_color.rgb = fill_color

def insert_unit_eqp(slide : Slide, unit : Unit, ptleft : int = 20, pttop : int = 20, pttablewidth : int = 160) -> None :
    """
    Inserts an unit's equipments table on a ppt slide at a given position.
    :param slide: the ppt slide
    :param unit: object of Unit class
    :param ptleft: position to left slide border
    :param pttop: position to top slide border
    :param pttablewidth: width of the table to insert
    :return: None
    """

    #position settings
    left, top, table_width, cy = Pt(ptleft), Pt(pttop), Pt(pttablewidth), Pt(5)

    #table creation
    nb_row = len(unit.equipments)
    if nb_row == 0 : return
    shape = slide.shapes.add_table(nb_row, 2, left, top, table_width, cy)
    table = shape.table

    #table size settings
    table.columns[1].width = Pt(25)
    font_size = 6

    for i, (eqp_type, qty) in enumerate(unit.equipments.items()):
        format_cell(table.cell(i, 0), eqp_type.name, font_size, font_color=RGBColor(0, 0, 0), fill_color=RGBColor(200, 200, 200))
        format_cell(table.cell(i, 1), str(qty), font_size, font_color=RGBColor(0, 0, 0), fill_color=RGBColor(200, 200, 200))

# fonction qui permet d'ajouter un tableau de type de matos
def insert_unit_summary(slide : Slide, unit : Unit, categories : list, ptleft : int =20, pttop : int =20, pttablewidth : int = 360) -> None:
    """
    Inserts an unit's summary table on a ppt slide at a given position.
    :param slide: the ppt slide
    :param unit: object of Unit class
    :param categories: the equipment categories you want to sum up. It's better to not go above 7 categories.
    :param ptleft: position to left slide border
    :param pttop: position to top slide border
    :param pttablewidth: width of the table to insert
    :return: None
    """
    #table settings
    left, top, table_width, cy = Pt(ptleft), Pt(pttop), Pt(pttablewidth), Pt(5)
    nb_col = len(categories)
    shape = slide.shapes.add_table(2, nb_col, left, top, table_width, cy)
    table = shape.table
    for i in range(nb_col):
        table.columns[i].width = Pt(int(pttablewidth/nb_col)) #cell width setting

    font_size = 16
    sum_categories = unit.count_category(categories)

    for i, (cat, nb) in enumerate(sum_categories.items()) :
        format_cell(table.cell(0, i), text =cat, font_size = font_size, font_color=RGBColor(0, 0, 0), fill_color=RGBColor(250, 250, 250) )
        format_cell(table.cell(1, i), text=str(nb), font_size=font_size, font_color=RGBColor(0, 0, 0),
                    fill_color=RGBColor(250, 250, 250))


def format_line_style(line) -> None :
    """
    Apply consistent formatting to a PPT line shape.
    :param line: ppt object line
    :return: None
    """
    line.line.color.rgb = RGBColor(0, 0, 0)
    line.line.width = Pt(3)
    line.shadow.inherit = False

def add_line(group, x : float, y : float, dx : float, dy : float) :
    """
    Add a formatted line at a given position with the given sizes.
    :param group: the group of shapes where the new line needs to be added in
    :param x: left position
    :param y: top position
    :param dx: line width
    :param dy: line height
    :return: ppt shape line
    """
    line = group.shapes.add_shape(MSO_SHAPE.LINE_INVERSE, Pt(x), Pt(y), Pt(dx), Pt(dy))
    format_line_style(line)
    return line

def add_vertical_line(group, x_start : float, y : float, count : int, horizontal_spacing : float):
    """
    Adds the vertical bars on an horizontal hierarchical line.
    :param group: the group of shapes where the new line needs to be added in
    :param x_start: the left position of the first vertical bar
    :param y: the top position of the bars
    :param count: the number of bars to be added
    :param horizontal_spacing: the space between two bars
    :return: None
    """
    for n in range(count):
        x = x_start + n * horizontal_spacing
        add_line(group, x, y, 0, 12)

def add_lines_odb(nb: int, slide: Slide, first_unit_left_pos : float, first_unit_top_pos: float, horizontal_scpacing : float, vertical_spacing: float, n_jump: int = 6) -> None :
    """
    Insert all the hierarchical lines on a slide, based on the inserted units.
    :param nb: number of inserted units
    :param slide: ppt slide
    :param first_unit_left_pos: left position of the first inserted unit
    :param first_unit_top_pos: top position of the first inserted unit
    :param horizontal_scpacing: horizontal space between 2 units
    :param vertical_spacing: stop space between 2 units
    :param n_jump: number of units per line
    :return: None
    """
    if nb == 0:
        return

    x_start = first_unit_left_pos + 45
    y_start = first_unit_top_pos - 10
    nb_lines = (nb - 1) // n_jump
    reste = nb % n_jump

    group_shape = slide.shapes.add_group_shape()

    #the first vertical line from the parent unit to the first horizontal line
    add_vertical_line(group_shape, PowerpointConfig.pos_unite_parent_left + 47, y_start - 12, 1, horizontal_scpacing)

    for line in range(nb_lines + 1):
        y = y_start + line * vertical_spacing

        if line < nb_lines:
            #for all the lines that are not the last one
            add_line(group_shape, x_start, y, (n_jump - 1) * horizontal_scpacing, 0)
            add_line(group_shape, x_start + 0.5 * horizontal_scpacing, y, 0, vertical_spacing)
            add_vertical_line(group_shape, x_start, y, n_jump, horizontal_scpacing)

        elif line == nb_lines:
            #for the last line
            count = reste if reste else n_jump
            if reste == 1:
                #specific case with only 1 unit on a line
                if line == 0 :
                    #specific case when there is only 1 line
                    add_line(group_shape, x_start, y, int(1.35 * vertical_spacing), 0)
                else :
                    add_line(group_shape, x_start, y, int(0.45 * vertical_spacing), 0)
            add_vertical_line(group_shape, x_start, y, count, horizontal_scpacing)
            add_line(group_shape, x_start, y, (count - 1) * horizontal_scpacing, 0)

        else:
            print('Something unexpected happened in function add_lines_odb.')

def orbat_generator(dict_units, path_prs, categories : list, start_column='++', table_equip=1, deep=False, flag = False) -> None :
    """
    Creates a ppt presentation containing all the units stored in a dictionnary.
    :param dict_units: dictionnary containing all the units. Should be like dico = {'echelon' : {'unit name' : Unit}}
    :param path_prs: path to save the created presentation
    :param categories: equipment category you want to sum up
    :param start_column: the starting echelon for witch you want to create the hierarchy
    :param table_equip: take 0 for no table at all, 1 for just the summary table, 2 for all the equipment tables
    :param deep: if you want the function to be recursive
    :param flag: if you want to insert the country flag
    :return: None
    """

    pprint(f"The following units will be described : {dict_units[start_column]}")

    #PPT presentation creation
    pres = Presentation()
    blank_slide_layout = pres.slide_layouts[6]  #blank slide as default slide


    #for name, parent in dict_units[start_column].items() :
    def add_unit_slide(unit, prs) :
        slide = prs.slides.add_slide(blank_slide_layout)  #new slide for each unit

        #__ _______________________SLIDE TITLE__________________________________________________________
        slide_titre = unit.sup.name + ' / ' + unit.name if unit.sup else unit.name
        txtitre = slide.shapes.add_textbox(Pt(PowerpointConfig.title_left), Pt(PowerpointConfig.title_top), Pt(PowerpointConfig.txt_w), Pt(PowerpointConfig.txt_h))
        titre = txtitre.text_frame
        titre.paragraphs[0].text = slide_titre
        titre.paragraphs[0].font.size = Pt(PowerpointConfig.title_size)
        #____________FLAG_____________________________________________________________________________
        if flag :
            sup = unit.sup
            supname = sup.name if sup else unit.name
            while sup :
                supname = sup.name
                sup = sup.sup

            img_path = PowerpointConfig.images_path + supname + '.png'
            if os.path.exists(img_path):
                slide.shapes.add_picture(img_path, Pt(PowerpointConfig.drap_left), Pt(PowerpointConfig.drap_top), height=Pt(PowerpointConfig.drap_high))
            else:
                slide.shapes.add_picture(PowerpointConfig.images_path + 'default.png', PowerpointConfig.drap_left, PowerpointConfig.drap_top, height=Pt(PowerpointConfig.drap_high))
        # _______________________UNIT SYMB_______________________________________________________________
        insert_app6(slide, unit, pos_left = PowerpointConfig.pos_unite_parent_left, pos_top = PowerpointConfig.pos_unite_parent_top)

        #if unit sup exists
        if unit.sup :
            insert_app6(slide, unit.sup, pos_left=2 * 28.35, pos_top=1.1 * 28.35)

        # _______________________UNIT SUMMARY___________________________________________________________
        if table_equip != 0 :
            insert_unit_summary(slide, unit, categories=categories, ptleft = PowerpointConfig.table_type_left, pttop = PowerpointConfig.table_type_top)

        #_________________SUBORDINATES__________________________
        for i, child in enumerate(reversed(unit.sub), start=1) :
            nb_line = (i - 1) // PowerpointConfig.jump + 1
            pt_top = PowerpointConfig.pos_unite_child_top + (nb_line - 1) * PowerpointConfig.dec_child_bot  #new line for each 'jump' units
            pt_left = PowerpointConfig.pos_unite_child_left + (i - 1 - (nb_line - 1) * PowerpointConfig.jump) * PowerpointConfig.val_dec_right

            #add the child unit to the slide
            insert_app6(slide, child, pos_left=pt_left, pos_top=pt_top)

            #insert unit equipment table
            if table_equip == 2 and child.ech in ('II', 'I', 'ooo') :
                insert_unit_eqp(slide, child, ptleft= pt_left-PowerpointConfig.val_dec_tbl, pttop=pt_top + PowerpointConfig.val_dec_bot)

        add_lines_odb(len(unit.sub), slide, PowerpointConfig.pos_unite_child_left, PowerpointConfig.pos_unite_child_top, PowerpointConfig.val_dec_right, PowerpointConfig.dec_child_bot,
                      n_jump=PowerpointConfig.jump)

        #recursivity if deep is True
        if deep :
            for child in reversed(unit.sub) :
                if child.ech not in ['II','I','ooo','oo','o'] :
                    add_unit_slide(child, prs)

    for name, parent in dict_units[start_column].items() :
        add_unit_slide(parent, pres)

    try :
        pres.save(path_prs)
    except FileNotFoundError :
        print(f"Your directory seems to be absent. It has been created. The poweropint file is inside at {path_prs}")
        dire = path_prs.rsplit('/', maxsplit = 2)
        name_dire = dire[0] if dire[0] != '.' else dire[1]
        os.makedirs(name_dire,exist_ok=True)
        pres.save(path_prs)

