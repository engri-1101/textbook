from bokeh.models.widgets import Div
from bokeh.models import CustomJS

#<editor-fold cpu_selected_change_code:
inAnIterOnChange = """
const val = (this.text !== 'false');
autoNextButton.disabled = val;
startAutomateButton.disabled = val;
"""
#</editor-fold>

#<editor-fold create():
def create(game_parts):
    in_an_iter = Div(text = "false", visible = False)
    game_parts.divs['in_an_iter'] = in_an_iter
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    args_dict = dict(
        autoNextButton = game_parts.buttons['next'],
        startAutomateButton = game_parts.buttons['start']
    )
    in_an_iter_change = CustomJS(args = args_dict, code = inAnIterOnChange)
    game_parts.divs['in_an_iter'].js_on_change('text', in_an_iter_change)
#</editor-fold>
