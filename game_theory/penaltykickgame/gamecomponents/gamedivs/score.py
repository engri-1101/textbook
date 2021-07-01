from bokeh.models.widgets import Div

#<editor-fold create():
def create(game_parts, text = "0", visible = False):
    score = Div(text = text, visible = visible)
    game_parts.divs['score'] = score
#</editor-fold>
