from bokeh.models import ColumnDataSource

#<editor-fold create():
def create(game_parts, footedness_left_text = "Left",
           footedness_right_text = "Right", aim_direction_left_text = "Left",
           aim_direction_middle_text = "Middle",
           aim_direction_right_text = "Right"):
    distribution_data = dict(footedness = [footedness_left_text,
                                           footedness_left_text,
                                           footedness_left_text,
                                           footedness_right_text,
                                           footedness_right_text,
                                           footedness_right_text],
                             aim_direction = [aim_direction_left_text,
                                              aim_direction_middle_text,
                                              aim_direction_right_text,
                                              aim_direction_left_text,
                                              aim_direction_middle_text,
                                              aim_direction_right_text],
                             freq = [0, 0, 0, 0, 0, 0],
                             decisions = [0, 0, 0, 0, 0, 0],
                             goalie_perceived_risks = [0, 0, 0, 0, 0, 0],
                             striker_score_chance = [0, 0, 0, 0, 0, 0],
                             striker_score_roll = [0, 0, 0, 0, 0, 0])

    distribution_table_source = ColumnDataSource(distribution_data)

    game_parts.sources['distribution_table'] = distribution_table_source
#</editor-fold>
