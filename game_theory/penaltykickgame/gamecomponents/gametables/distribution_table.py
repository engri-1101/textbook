from bokeh.models import TableColumn, DataTable

#<editor-fold create():
def create(game_parts, footedness_title = "Striker Footedness",
           footedness_width = 101, aim_direction_title = "Striker Aim Direction",
           aim_direction_width = 107, freq_title = "Frequency", freq_width = 60,
           decisions_title = "Goalie Decisions", decisions_width = 90,
           perceived_risks_title = "Goalie Perceived Risks",
           perceived_risks_width = 130,
           score_chance_title = "Striker's Score Chance",
           score_chance_width = 120, score_roll_title = "Striker's Score Roll",
           score_roll_width = 103, width = 711, height = 280,
           autosize_mode = "force_fit", sizing_mode = "scale_width",
           visibility = False, fit_columns = False):

    footedness = TableColumn(field = "footedness", title = footedness_title,
                             width = footedness_width)
    aim_direction = TableColumn(field = "aim_direction",
                                title = aim_direction_title,
                                width = aim_direction_width)
    freq = TableColumn(field = "freq", title = freq_title, width = freq_width)
    decisions = TableColumn(field = "decisions", title = decisions_title,
                            width = decisions_width)
    perceived_risks =  TableColumn(field = "goalie_perceived_risks",
                                   title = perceived_risks_title,
                                   width = perceived_risks_width)
    score_chance = TableColumn(field = "striker_score_chance",
                               title = score_chance_title,
                               width = score_chance_width)
    score_roll = TableColumn(field = "striker_score_roll",
                             title = score_roll_title,
                             width = score_roll_width)
    distributions = [footedness, aim_direction, freq, decisions,
                     perceived_risks, score_chance, score_roll]

    automation_distribution_table = DataTable(source = game_parts.sources['automation_distribution_table_source'],
                                              columns = distributions,
                                              width = width, height = height,
                                              autosize_mode = autosize_mode,
                                              sizing_mode = sizing_mode,
                                              visible = visibility,
                                              fit_columns = fit_columns)
    game_parts.tables['automation_distribution_table'] = automation_distribution_table
#</editor-fold>
