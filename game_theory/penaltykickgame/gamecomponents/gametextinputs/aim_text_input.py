from bokeh.models import TextInput, CustomJS
# FILE-WIDE CONSTANT FOR DEALING WITH JAVASCRIPT ISSUES REGARDING NUMBERS:
JS_FLOAT_BUFFER = "0.0000001"

#<editor-fold aim_inputs on change callback Code String:
# Handles changes to the pure strategy selection chance for a given aim text
# input. Hides the start button, then checks the values of all text inputs. If
# all values are between 0 and 1, and they add up to 1, then the game start
# condition tracking div enforcing player chance inputs is changed to indicate
# proper completion. Also updates the automation table to contain the new aim
# chances.

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
def create(game_parts, id, config):
    """Creates a Bokeh TextInput object for inputting the selection chance of
    the kicker's pure strategy indicated by id, then adds it to the passed
    _GameParts object being used to collect the game components.


    Arguments:
    game_parts -- The _GameParts object being used to collect game components.
    id -- A string indicating the TextInput's corresponding pure strategy.
      Either "ll", "lm", "lr", "rl", "rm", or "rr".
    config -- The config object being used to configure the game's
      aim TextInputs.
    """
    names = {
        "ll" : "Left-Footed Kicker Kicking to the Left Selection Chance",
        "lm" : "Left-Footed Kicker Kicking to the Middle Selection Chance",
        "lr" : "Left-Footed Kicker Kicking to the Right Selection Chance",
        "rl" : "Right-Footed Kicker Kicking to the Left Selection Chance",
        "rm" : "Right-Footed Kicker Kicking to the Middle Selection Chance",
        "rr" : "Right-Footed Kicker Kicking to the Right Selection Chance"
    }
    name = names[id]

    aim_text_input = TextInput(
        value=config.value, title=name, visible=config.visible
    )
    game_parts.textinputs[id + "_aim"] = aim_text_input
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    """Sets up the aim TextInput objects to work in the game.


    Argument:
    game_parts -- The _GameParts object containing the game components.
    """
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
    for text_input in aim_text_inputs:
        text_input.js_on_change("value", aim_text_inputs_change)
#</editor-fold>
