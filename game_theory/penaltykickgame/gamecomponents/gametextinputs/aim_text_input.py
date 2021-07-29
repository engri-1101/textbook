from bokeh.models import TextInput, CustomJS

JS_FLOAT_BUFFER = "0.0000001" # THIS VARIABLE SHOULD BE TREATED AS A CONSTANT.
# JAVASCRIPT HAS SOME ISSUES WITH FLOATS, SO CHECKING FOR EQUALITY BETWEEN
# NUMBERS AND THE SUMS (OR OTHER OPERATIONS) OF OTHER NUMBERS IS NOT SAFE.
# IN ORDER TO WORK AROUND THIS ISSUE, INSTEAD OF CHECKING FOR EQUALITY, CHECK
# THAT THE VALUE IS WITHIN A RANGE OF THE EXPECTED OUTCOME.

#<editor-fold aim_inputs_callback Code String:
aimTextInputsOnChange = """
//Hide start button:
startAutomateButton.visible = false;

const aimVals = aimTextInputs.map(
  (v) => parseFloat(v.value)
);

//Handle Validity Checks 1 & 2:
const isValid1 = (Math.max(...aimVals) <= 1);
const isValid2 = (Math.min(...aimVals) >= 0);

//Handle Validity check 3:
const total = aimVals.reduce((a, b) => a + b);
const isValid3 = (Math.abs(total - 1) <= """ + JS_FLOAT_BUFFER + """);

chancesGT1Tip.visible = !isValid1;
chancesLT0Tip.visible = !isValid2;
chancesNE1Tip.visible = !isValid3;

tableSrc.data['chances'] = aimVals.slice();
tableSrc.change.emit();

chancesValidDiv.text = ((isValid1 && isValid2 && isValid3) ? '1' : '0');
"""
#</editor-fold>

#<editor-fold create():
def create(game_parts, name, config):
    aim_text_input = TextInput(value = config.value,
                               title = name + config.title_addition,
                               visible = config.visible)
    game_parts.textinputs[name + '_aim'] = aim_text_input
#</editor-fold>

#<editor-fold aim_textInputs_setup():
#Needs:
#    from bokeh.models import CustomJS
def setup(name, game_parts):
    aimTextInputs = [game_parts.textinputs['ll_aim'],
                     game_parts.textinputs['lm_aim'],
                     game_parts.textinputs['lr_aim'],
                     game_parts.textinputs['rl_aim'],
                     game_parts.textinputs['rm_aim'],
                     game_parts.textinputs['rr_aim']]

    args_dict = dict(tableSrc = game_parts.sources['automation_table'],
                     aimTextInputs = aimTextInputs,
                     chancesValidDiv = game_parts.divs['chances_valid'],
                     startAutomateButton = game_parts.buttons['start'],
                     chancesGT1Tip = game_parts.divs['chances_gt_1_tip'],
                     chancesLT0Tip = game_parts.divs['chances_lt_0_tip'],
                     chancesNE1Tip = game_parts.divs['chances_ne_1_tip'])

    aim_textInputs_change = CustomJS(args = args_dict,
                                     code = aimTextInputsOnChange)
    key = (name + '_aim')
    game_parts.textinputs[key].js_on_change('value', aim_textInputs_change)
#</editor-fold>
