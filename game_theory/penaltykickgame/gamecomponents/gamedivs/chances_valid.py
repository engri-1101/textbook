from bokeh.models.widgets import Div
from bokeh.models import CustomJS

#<editor-fold chances_valid_change_code:
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
    chances_valid = Div(text = "0", visible = False)
    game_parts.divs['chances_valid'] = chances_valid
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    args_dict = dict(
        startAutomateButton = game_parts.buttons['start'],
        makeCounterButton = game_parts.buttons['make_counter'],
        cpuSelectedDiv = game_parts.divs['cpu_selected'],
        counterMadeDiv = game_parts.divs['counter_made'],
        chancesValidDiv = game_parts.divs['chances_valid']
    )

    chances_valid_change = CustomJS(
        code = chancesValidOnChange, args = args_dict
    )

    game_parts.divs['chances_valid'].js_on_change('text', chances_valid_change)
#</editor-fold>
