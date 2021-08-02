from bokeh.models import ColumnDataSource
#<editor-fold create():
def create(game_parts, config):
    data = dict(
        x = config.xs,
        y = config.ys,
        text = config.text_lines
    )
    scr_text = ColumnDataSource(data)
    game_parts.texts['scr_text'] = scr_text
#</editor-fold>
