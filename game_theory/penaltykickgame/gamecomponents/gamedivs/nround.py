from bokeh.models.widgets import Div

#<editor-fold create():
def create(game_parts, text = "0", visible = False):
    nround = Div(text = text, visible = visible)
    game_parts.divs['nround'] = nround
#</editor-fold>
