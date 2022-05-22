from bokeh.models import Button, ColumnDataSource, CustomJS

#<editor-fold make counter on click Callback Code String:
# Code for creating the keeper's counter to the player's input mixed strategy
# for the kicker. Does this by first grabbing their input chances for each pure
# strategy, hiding the aim TextInputs to prevent them from being changed,
# calculating the expected risk of being scored on for each possible goalie
# action, determining the lowest risk action, then updating the counter source
# to indicate that the lowest risk action should be taken. Following that, the
# make counter button is hidden, and the counter necessity tracking div is
# updated to indicate that a counter is no longer needed.
makeCounterCode = """
const chances = automationTableSrc.data['chances'];

//Hides the automation table as it is un-needed:
aimTextInputs.forEach(
  (v) => v.visible = false
);

const rDict = {
  'LeftLeft'   : 0.55, 'LeftMiddle'   : 0.65, 'LeftRight'   : 0.93,
  'MiddleLeft' : 0.74, 'MiddleMiddle' : 0.60, 'MiddleRight' : 0.72,
  'RightLeft'  : 0.95, 'RightMiddle'  : 0.73, 'RightRight'  : 0.70
};
const lDict = {
  'LeftLeft'   : 0.67, 'LeftMiddle'   : 0.70, 'LeftRight'   : 0.96,
  'MiddleLeft' : 0.74, 'MiddleMiddle' : 0.60, 'MiddleRight' : 0.72,
  'RightLeft'  : 0.87, 'RightMiddle'  : 0.65, 'RightRight'  : 0.61
};
const scoreProbDicts = {
  'Right' : rDict,
  'Left'  : lDict
};

const directions = ['Left', 'Middle', 'Right'];

['Left', 'Right'].forEach(
  (foot, footIndex) => {
    const aimChances = chances.slice(3 * footIndex, 3 * (footIndex + 1));

    const scoreChancesDict = scoreProbDicts[foot];
    const risks = [0, 0, 0];

    directions.forEach(
      (v, i) => {
        directions.forEach(
          (v2, i2) => risks[i] += (aimChances[i2] * scoreChancesDict[v2 + v])
        )
      }
    );

    const stratToTake = risks.indexOf(Math.min(...risks));
    goalieCounterSrc.data[foot][stratToTake] = 1;
  }
);

goalieCounterSrc.change.emit();

makeCounterButton.visible = false;

counterMadeDiv.text = '1';
"""
#</editor-fold>

#<editor-fold create():
def create(game_parts, config):
    """Creates the make counter button, and adds it to the passed _GameParts
    object being used to collect the game components.


    Arguments:
    game_parts -- The _GameParts object being used to collect the
      game components.
    config -- The config object being used to configure the button.
    """
    button = Button(
        label=config.label, button_type=config.button_type,
        sizing_mode=config.sizing_mode, width_policy=config.width_policy,
        disabled=config.disabled, visible=config.visible
    )
    game_parts.buttons["make_counter"] = button
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    """Sets up the make counter button to be able to run its on click
    Javascript code. Also creates and adds the goalie counter source to the
    _GameParts object containing the game components.


    Argument:
    game_parts -- The _GameParts object containing the game components.
    """
    text_inputs = game_parts.textinputs
    srcs = game_parts.sources
    buttons = game_parts.buttons
    b_make_counter = buttons["make_counter"]
    goalie_counter_src = ColumnDataSource(
        data = {"Left" : [0, 0, 0], "Right" : [0, 0, 0]}
    )
    srcs["goalie_counter"] = goalie_counter_src

    aim_text_inputs = [
        text_inputs["ll_aim"], text_inputs["lm_aim"], text_inputs["lr_aim"],
        text_inputs["rl_aim"], text_inputs["rm_aim"], text_inputs["rr_aim"]
    ]

    args_dict = {
        "makeCounterButton" : b_make_counter,
        "automationTableSrc" : srcs["automation_table"],
        "counterMadeDiv" : game_parts.divs["counter_made"],
        "goalieCounterSrc" : goalie_counter_src,
        "aimTextInputs" : aim_text_inputs
    }

    b_make_counter_click = CustomJS(args=args_dict, code=makeCounterCode)
    b_make_counter.js_on_click(b_make_counter_click)
#</editor-fold>
