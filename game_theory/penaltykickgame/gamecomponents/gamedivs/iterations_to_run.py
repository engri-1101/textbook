from bokeh.models.widgets import Div

#<editor-fold create():
def create(game_parts, config):
    iterations_to_run = Div(text = config.text, visible = config.visible)
    game_parts.divs['iterations_to_run'] = iterations_to_run
#</editor-fold>
