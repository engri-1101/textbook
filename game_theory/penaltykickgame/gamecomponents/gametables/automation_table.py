from bokeh.models import TableColumn, DataTable

#<editor-fold create():
def create(game_parts, config):

    footedness_column = TableColumn(field = "footedness",
                                    title = config.titles[0])
    aim_direction_column = TableColumn(field = "aim_direction",
                                       title = config.titles[1])
    chances_column = TableColumn(field = "chances",
                                 title = config.titles[2])

    columns = [footedness_column, aim_direction_column, chances_column]

    automation_table = DataTable(source = game_parts.sources['automation_table'],
                                 columns = columns, width = config.width,
                                 height = config.height,
                                 autosize_mode = config.autosize_mode,
                                 visible = config.visible)
    game_parts.tables['automation'] = automation_table
#</editor-fold>
