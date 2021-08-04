from bokeh.models import ColumnDataSource
#<editor-fold create():
def create(game_parts, config):
    data = {"x" : config.xs, "y" : config.ys, "text" : config.text_lines}
    text = ColumnDataSource(data)
    game_parts.texts["scr_text"] = text
#</editor-fold>
