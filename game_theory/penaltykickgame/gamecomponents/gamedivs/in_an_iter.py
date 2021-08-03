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
    div = Div(text="false", visible=False)
    game_parts.divs["in_an_iter"] = div
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    buttons = game_parts.buttons
    args_dict = dict(
        autoNextButton = buttons["next"],
        startAutomateButton = buttons["start"]
    )
    in_an_iter_change = CustomJS(args=args_dict, code=inAnIterOnChange)
    game_parts.divs["in_an_iter"].js_on_change("text", in_an_iter_change)
#</editor-fold>
