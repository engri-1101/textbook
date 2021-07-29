from bokeh.models import ColumnDataSource
#<editor-fold create():
def create(game_parts, config):
    scr_text = ColumnDataSource({'x' : config.xs,
                                 'y' : config.ys,
                                 'text' : config.text_lines})
    game_parts.texts['scr_text'] = scr_text
#</editor-fold>
