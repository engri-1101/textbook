from bokeh.models.widgets import Div

#<editor-fold create():
def create(game_parts, config):
    kicker_foot = Div(text = config.text, visible = config.visible)
    game_parts.divs['kicker_foot'] = kicker_foot
#</editor-fold>
