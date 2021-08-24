from bokeh.models import TableColumn, DataTable

#<editor-fold create():
def create(game_parts, config):
    """Creates the game's automation table then adds it to the passed in
    _GameParts object being used to collect the game components.


    Arguments:
    game_parts -- The _GameParts object being used to collect the
      game components.
    config -- The config object being used to configure the automation table.
    """
    fields = ["footedness", "aim_direction", "chances"]

    columns = []
    for i in range(len(fields)):
        column = TableColumn(field=fields[i], title=config.titles[i])
        columns.append(column)

    table = DataTable(
        source=game_parts.sources["automation_table"], columns=columns,
        width=config.width, height=config.height,
        autosize_mode=config.autosize_mode, visible=config.visible
    )
    game_parts.tables["automation"] = table
#</editor-fold>
