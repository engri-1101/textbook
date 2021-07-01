from bokeh.models.widgets import Div

#<editor-fold create():
def create(game_parts, text = "Not Set", visible = False):
    strategy_to_use = Div(text = text, visible = visible)
    game_parts.divs['strategy_to_use'] = strategy_to_use
#</editor-fold>
