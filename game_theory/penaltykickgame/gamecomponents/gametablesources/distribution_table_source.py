from bokeh.models import ColumnDataSource

#<editor-fold create():
def create(game_parts, footedness_config, initial_stats):
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
    distribution_data = dict(footedness = footedness,
                             aim_direction = aim_direction,
                             freq = initial_stats['freq'],
                             decisions = initial_stats['decisions'],
                             goalie_perceived_risks = initial_stats['perceived_risks'],
                             striker_score_chance = initial_stats['score_chance'],
                             striker_score_roll = initial_stats['score_roll'])

    distribution_table_source = ColumnDataSource(distribution_data)

    game_parts.sources['distribution_table'] = distribution_table_source
#</editor-fold>
