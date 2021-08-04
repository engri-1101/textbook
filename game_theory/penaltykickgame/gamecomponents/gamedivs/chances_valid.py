from bokeh.models.widgets import Div
from bokeh.models import CustomJS

#<editor-fold chances_valid on change callback code string:
chancesValidOnChange = """
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
    game_parts.divs["chances_valid"] = div
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    buttons = game_parts.buttons
    divs = game_parts.divs
    args_dict = {
        "startAutomateButton" : buttons["start"],
        "makeCounterButton" : buttons["make_counter"],
        "cpuSelectedDiv" : divs["cpu_selected"],
        "counterMadeDiv" : divs["counter_made"],
        "chancesValidDiv" : divs["chances_valid"]
    }

    chances_valid_change = CustomJS(code=chancesValidOnChange, args=args_dict)

    divs["chances_valid"].js_on_change("text", chances_valid_change)
#</editor-fold>
