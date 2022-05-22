from bokeh.models.widgets import Div
from bokeh.models import CustomJS

#<editor-fold in_an_iter on change callback code string:
# Code for handling changes to the in_an_iter div. Prevents both the start and
# next buttons from being clickable if its value is not 'false'.
inAnIterOnChange = """
const val = (this.text !== 'false');
autoNextButton.disabled = val;
startAutomateButton.disabled = val;
"""
#</editor-fold>

#<editor-fold create():
def create(game_parts):
    """Creates the div used to track whether or not an iteration of the game is
    currently running, then adds it into the passed in _GameParts object being
    used to collect the game components.


    Argument:
    game_parts -- The _GameParts object being used to collect the
      game components.
    """
    div = Div(text="false", visible=False)
    game_parts.divs["in_an_iter"] = div
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    """Sets up the div being used to track whether or not an iteration is
    running to execute its on change javaScript code.


    Argument:
    game_parts -- The _GameParts object containing the game components.
    """
    buttons = game_parts.buttons

    args_dict = {
        "autoNextButton" : buttons["next"],
        "startAutomateButton" : buttons["start"]
    }

    in_an_iter_change = CustomJS(args=args_dict, code=inAnIterOnChange)

    game_parts.divs["in_an_iter"].js_on_change("text", in_an_iter_change)
#</editor-fold>
