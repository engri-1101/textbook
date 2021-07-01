from bokeh.models import ColumnDataSource

#<editor-fold create():
def create(game_parts, footedness_left_text = "Left",
           footedness_right_text = "Right", aim_direction_left_text = "Left",
           aim_direction_middle_text = "Middle",
           aim_direction_right_text = "Right",
           ll_base_chance = 0, lm_base_chance = 0, lr_base_chance = 0,
           rl_base_chance = 0, rm_base_chance = 0, rr_base_chance = 0):
    data = dict(footedness = [footedness_left_text,  footedness_left_text,
                              footedness_left_text,  footedness_right_text,
                              footedness_right_text, footedness_right_text],
                aim_direction = [aim_direction_left_text,
                                 aim_direction_middle_text,
                                 aim_direction_right_text,
                                 aim_direction_left_text,
                                 aim_direction_middle_text,
                                 aim_direction_right_text],
                chances = [ll_base_chance, lm_base_chance, lr_base_chance,
                           rl_base_chance, rm_base_chance, rr_base_chance])

    automation_table_source = ColumnDataSource(data)
    game_parts.sources['automation_table'] = automation_table_source
#</editor-fold>
