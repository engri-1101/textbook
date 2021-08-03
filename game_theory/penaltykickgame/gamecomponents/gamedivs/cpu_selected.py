from bokeh.models.widgets import Div
from bokeh.models import CustomJS

#<editor-fold cpu_selected_change_code:
cpuSelectedOnChange = """
const counterMadeText = counterMadeDiv.text;
const chancesValidText = chancesValidDiv.text;

const canAccessMakeCounter = (
  counterMadeText !== '1' && chancesValidText === '1'
);
const canAccessStartAutomate = (
  counterMadeText === '1' &&
  chancesValidText === '1' &&
  cpuSelectedDiv.text === '1'
);

startAutomateButton.visible = canAccessStartAutomate;
makeCounterButton.visible = canAccessMakeCounter;
"""
#</editor-fold>

#<editor-fold create():
def create(game_parts):
    div = Div(text="0", visible=False)
    game_parts.divs["cpu_selected"] = div
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    divs = game_parts.divs
    buttons = game_parts.buttons
    args_dict = dict(
        startAutomateButton = buttons["start"],
        makeCounterButton = buttons["make_counter"],
        cpuSelectedDiv = divs["cpu_selected"],
        counterMadeDiv = divs["counter_made"],
        chancesValidDiv = divs["chances_valid"]
    )

    cpu_selected_change = CustomJS(code=cpuSelectedOnChange, args=args_dict)

    divs["cpu_selected"].js_on_change("text", cpu_selected_change)
#</editor-fold>
