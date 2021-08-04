from bokeh.models import ColumnDataSource

#<editor-fold create():
def create(game_parts, config, initial_stats):
    f_left = config.footedness_left_text
    f_right = config.footedness_right_text
    ad_left = config.aim_direction_left_text
    ad_middle = config.aim_direction_middle_text
    ad_right = config.aim_direction_right_text
    footedness = [f_left, f_left, f_left, f_right, f_right, f_right]
    aim_direction = [
        ad_left, ad_middle, ad_right, ad_left, ad_middle, ad_right
    ]

    data = {
        "footedness" : footedness,
        "aim_direction" : aim_direction,
        "freq" : initial_stats["freq"],
        "decisions" : initial_stats["decisions"],
        "goalie_perceived_risks" : initial_stats["perceived_risks"],
        "striker_score_chance" : initial_stats["score_chance"],
        "striker_score_roll" : initial_stats["score_roll"]
    }

    table_src = ColumnDataSource(data)
    game_parts.sources["distribution_table"] = table_src
#</editor-fold>
