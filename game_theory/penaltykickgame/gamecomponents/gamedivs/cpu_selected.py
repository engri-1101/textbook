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
    cpu_selected = Div(text = "0", visible = False)
    game_parts.divs['cpu_selected'] = cpu_selected
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    args_dict = dict(startAutomateButton = game_parts.buttons['start'],
                     makeCounterButton = game_parts.buttons['make_counter'],
                     cpuSelectedDiv = game_parts.divs['cpu_selected'],
                     counterMadeDiv = game_parts.divs['counter_made'],
                     chancesValidDiv = game_parts.divs['chances_valid'])

    cpu_selected_change = CustomJS(code = cpuSelectedOnChange, args = args_dict)

    game_parts.divs['cpu_selected'].js_on_change('text', cpu_selected_change)
#</editor-fold>
