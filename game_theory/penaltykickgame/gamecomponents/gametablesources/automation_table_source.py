from bokeh.models import ColumnDataSource

#<editor-fold create():
def create(game_parts, footedness_config, base_chances):
    footedness = [footedness_config.footedness_left_text,
                  footedness_config.footedness_left_text,
                  footedness_config.footedness_left_text,
                  footedness_config.footedness_right_text,
                  footedness_config.footedness_right_text,
                  footedness_config.footedness_right_text]
    aim_direction = [footedness_config.aim_direction_left_text,
                     footedness_config.aim_direction_middle_text,
                     footedness_config.aim_direction_right_text,
                     footedness_config.aim_direction_left_text,
                     footedness_config.aim_direction_middle_text,
                     footedness_config.aim_direction_right_text]
    chances = [base_chances[0], base_chances[1], base_chances[2],
               base_chances[3], base_chances[4], base_chances[5]]
    data = dict(
        footedness = footedness, aim_direction = aim_direction,
        chances = chances
    )

    automation_table_source = ColumnDataSource(data)
    game_parts.sources['automation_table'] = automation_table_source
#</editor-fold>
