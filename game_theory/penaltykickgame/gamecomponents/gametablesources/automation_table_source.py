from bokeh.models import ColumnDataSource

#<editor-fold create():
def create(game_parts, config, base_chances):
    f_left = config.footedness_left_text
    f_right = config.footedness_right_text
    ad_left = config.aim_direction_left_text
    ad_middle = config.aim_direction_middle_text
    ad_right = config.aim_direction_right_text
    footedness = [f_left, f_left, f_left, f_right, f_right, f_right]
    aim_direction = [
        ad_left, ad_middle, ad_right, ad_left, ad_middle, ad_right
    ]
    chances = [
        base_chances[0], base_chances[1], base_chances[2], base_chances[3],
        base_chances[4], base_chances[5]
    ]

    data = {
        "footedness" : footedness,
        "aim_direction" : aim_direction,
        "chances" : chances
    }

    table_src = ColumnDataSource(data)
    game_parts.sources["automation_table"] = table_src
#</editor-fold>
