from bokeh.models import TableColumn, DataTable

#<editor-fold create():
def create(game_parts, config):
    footedness = TableColumn(
        field = "footedness", title = config.titles[0],
        width = config.column_widths[0]
    )

    aim_direction = TableColumn(
        field = "aim_direction", title = config.titles[1],
        width = config.column_widths[1]
    )

    freq = TableColumn(
        field = "freq", title = config.titles[2],
        width = config.column_widths[2]
    )

    decisions = TableColumn(
        field = "decisions", title = config.titles[3],
        width = config.column_widths[3]
    )

    perceived_risks = TableColumn(
        field = "goalie_perceived_risks", title = config.titles[4],
        width = config.column_widths[4]
    )

    score_chance = TableColumn(
        field = "striker_score_chance", title = config.titles[5],
        width = config.column_widths[5]
    )

    score_roll = TableColumn(
        field = "striker_score_roll", title = config.titles[6],
        width = config.column_widths[6]
    )

    columns = [
        footedness, aim_direction, freq, decisions, perceived_risks,
        score_chance, score_roll
    ]

    table = DataTable(
        source = game_parts.sources['distribution_table'], columns = columns,
        width = config.width, height = config.height,
        autosize_mode = config.autosize_mode, sizing_mode = config.sizing_mode,
        visible = config.visible, fit_columns = config.fit_columns
    )

    game_parts.tables['distribution'] = table
#</editor-fold>
