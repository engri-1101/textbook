from bokeh.models.widgets import Div

#<editor-fold create():
def create(game_parts, text = "", visible = False):
    kicker_foot = Div(text = text, visible = visible)
    game_parts.divs['kicker_foot'] = kicker_foot
#</editor-fold>
