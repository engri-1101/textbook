from bokeh.models import TableColumn, DataTable

#<editor-fold create():
def create(game_parts, config):
    columns = []

    fields = ["footedness", "aim_direction", "chances"]
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
