from bokeh.models import TableColumn, DataTable

#<editor-fold create():
def create(game_parts, config):
    """Creates the game's distribution table then adds it to the passed in
    _GameParts object being used to collect the game components.


    Arguments:
    game_parts -- The _GameParts object being used to collect the
      game components.
    config -- The config object being used to configure the distribution table.
    """
    fields = [
        "footedness", "aim_direction", "freq", "decisions",
        "goalie_perceived_risks", "striker_score_chance", "striker_score_roll"
    ]

    columns = []
    for i in range(len(fields)):
        column = TableColumn(
            field=fields[i], title=config.titles[i],
            width=config.column_widths[i]
        )
        columns.append(column)

    table = DataTable(
        source=game_parts.sources["distribution_table"], columns=columns,
        width=config.width, height=config.height,
        autosize_mode=config.autosize_mode, sizing_mode=config.sizing_mode,
        visible=config.visible, fit_columns=config.fit_columns
    )

    game_parts.tables["distribution"] = table
#</editor-fold>
