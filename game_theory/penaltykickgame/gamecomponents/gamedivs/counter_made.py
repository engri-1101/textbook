from bokeh.models.widgets import Div
from bokeh.models import CustomJS

#<editor-fold counter_made_change_code:
counterMadeOnChange = """
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
    div = Div(text="1", visible=False)
    game_parts.divs["counter_made"] = div
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

    counter_made_change = CustomJS(code=counterMadeOnChange, args=args_dict)

    divs["counter_made"].js_on_change("text", counter_made_change)
#</editor-fold>
