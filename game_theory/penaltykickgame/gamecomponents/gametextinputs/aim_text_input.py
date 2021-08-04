from bokeh.models import TextInput, CustomJS

JS_FLOAT_BUFFER = "0.0000001" # THIS VARIABLE SHOULD BE TREATED AS A CONSTANT.
# JAVASCRIPT HAS SOME ISSUES WITH FLOATS, SO CHECKING FOR EQUALITY BETWEEN
# NUMBERS AND THE SUMS (OR OTHER OPERATIONS) OF OTHER NUMBERS IS NOT SAFE.
# IN ORDER TO WORK AROUND THIS ISSUE, INSTEAD OF CHECKING FOR EQUALITY, CHECK
# THAT THE VALUE IS WITHIN A RANGE OF THE EXPECTED OUTCOME.

#<editor-fold aim_inputs on change callback Code String:
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
    aim_text_input = TextInput(
        value=config.value, title=(name + config.title_addition),
        visible=config.visible
    )
    game_parts.textinputs[name + "_aim"] = aim_text_input
#</editor-fold>

#<editor-fold setup():
def setup(name, game_parts):
    text_inputs = game_parts.textinputs
    divs = game_parts.divs
    aim_text_inputs = [
        text_inputs["ll_aim"], text_inputs["lm_aim"], text_inputs["lr_aim"],
        text_inputs["rl_aim"], text_inputs["rm_aim"], text_inputs["rr_aim"]
    ]

    args_dict = {
        "tableSrc" : game_parts.sources["automation_table"],
        "aimTextInputs" : aim_text_inputs,
        "chancesValidDiv" : divs["chances_valid"],
        "startAutomateButton" : game_parts.buttons["start"],
        "chancesGT1Tip" : divs["chances_gt_1_tip"],
        "chancesLT0Tip" : divs["chances_lt_0_tip"],
        "chancesNE1Tip" : divs["chances_ne_1_tip"]
    }

    aim_text_inputs_change = CustomJS(
        args=args_dict, code=aimTextInputsOnChange
    )
    key = (name + "_aim")
    text_inputs[key].js_on_change("value", aim_text_inputs_change)
#</editor-fold>
