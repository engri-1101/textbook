from bokeh.models.widgets import Div

#<editor-fold create():
def create(game_parts, config):
    score = Div(text = config.text, visible = config.visible)
    game_parts.divs['score'] = score
#</editor-fold>
