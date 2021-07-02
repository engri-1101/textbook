from bokeh.models.widgets import Div

#<editor-fold create():
def create(game_parts, config):
    nround = Div(text = config.text, visible = config.visible)
    game_parts.divs['nround'] = nround
#</editor-fold>
