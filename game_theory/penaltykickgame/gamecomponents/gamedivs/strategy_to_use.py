from bokeh.models.widgets import Div

#<editor-fold create():
def create(game_parts, config):
    strategy_to_use = Div(text = config.text, visible = config.visible)
    game_parts.divs['strategy_to_use'] = strategy_to_use
#</editor-fold>
