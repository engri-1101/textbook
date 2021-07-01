from bokeh.models.widgets import Div

#<editor-fold create():
def create(game_parts, text = "50", visible = False):
    iterations_to_run = Div(text = text, visible = visible)
    game_parts.divs['iterations_to_run'] = iterations_to_run
#</editor-fold>
