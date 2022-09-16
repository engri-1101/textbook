from bokeh.models.widgets import Div
from bokeh.models import CustomJS

#<editor-fold cpu_selected on change callback code string:
# Code for handling changes to the game start condition enforcing divs. Allows
# the player to view (and therefore click) the Start button if a counter is
# un-needed, the input pure strategy use chances are valid, and a keeper
# strategy has been set. Allows the make counter button to be clicked instead,
# if a counter is needed, but all other conditions are true:
startChecksOnChange = """
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
    """Creates the game start condition enforcing divs and adds them to the
    passed _GameParts object being used to collect the game components.


    Argument:
    game_parts -- The _GameParts object being used to collect the
      game components.
    """
    cpu = Div(text="0", visible=False)
    counter = Div(text="1", visible=False)
    chances = Div(text="0", visible=False)
    game_parts.divs["cpu_selected"] = cpu
    game_parts.divs["counter_made"] = counter
    game_parts.divs["chances_valid"] = chances
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    """Sets up the game start condition enforcing divs to use their on change
    javaScript callback.


    Argument:
    game_parts -- The _GameParts object that contains the game components.
    """
    divs = game_parts.divs
    buttons = game_parts.buttons
    args_dict = {
        "startAutomateButton" : buttons["start"],
        "makeCounterButton" : buttons["make_counter"],
        "cpuSelectedDiv" : divs["cpu_selected"],
        "counterMadeDiv" : divs["counter_made"],
        "chancesValidDiv" : divs["chances_valid"]
    }

    start_checks_change = CustomJS(code=startChecksOnChange, args=args_dict)

    divs["cpu_selected"].js_on_change("text", start_checks_change)
    divs["counter_made"].js_on_change("text", start_checks_change)
    divs["chances_valid"].js_on_change("text", start_checks_change)
#</editor-fold>
