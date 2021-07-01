from bokeh.models import TableColumn, DataTable

#<editor-fold create():
def create(game_parts, footedness_title = "Striker Footedness",
           aim_direction_title = "Striker Aim Direction",
           chances_title = "Chance", width = 600, height = 280,
           autosize_mode = "force_fit", visible = False):

    footedness_column = TableColumn(field = "footedness",
                                    title = footedness_title)
    aim_direction_column = TableColumn(field = "aim_direction",
                                       title = aim_direction_title)
    chances_column = TableColumn(field = "chances",
                                 title = chances_title)

    columns = [footedness_column, aim_direction_column, chances_column]

    automation_table = DataTable(source = game_parts.sources['automation_table_source'],
                                 columns = columns, width = width,
                                 height = height, autosize_mode = autosize_mode,
                                 visible = visible)
    game_parts.tables['automation_table'] = automation_table
#</editor-fold>
