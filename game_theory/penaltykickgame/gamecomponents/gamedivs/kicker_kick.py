from bokeh.models.widgets import Div

#<editor-fold create():
def create(game_parts, text = "", visible = False):
    kicker_kick = Div(text = text, visible = visible)
    game_parts.divs['kicker_kick'] = kicker_kick
#</editor-fold>
