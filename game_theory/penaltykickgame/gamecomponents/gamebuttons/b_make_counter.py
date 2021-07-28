from bokeh.models import Button, ColumnDataSource, CustomJS

#<editor-fold Callback Code String:
makeCounterCode = """
const chances = automationTableSrc.data['chances'];

//Hides the automation table as it is un-needed:
automationTable.visible = false;
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
    b_make_counter = Button(label = config.label,
                            button_type = config.button_type,
                            sizing_mode = config.sizing_mode,
                            width_policy = config.width_policy,
                            disabled = config.disabled,
                            visible = config.visible)
    game_parts.buttons['make_counter'] = b_make_counter
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    goalie_counter_source = ColumnDataSource(data = dict(Left = [0, 0, 0],
                                                         Right = [0, 0, 0]))
    game_parts.sources['goalie_counter'] = goalie_counter_source
    aimTextInputs = [game_parts.textinputs['ll_aim'],
                     game_parts.textinputs['lm_aim'],
                     game_parts.textinputs['lr_aim'],
                     game_parts.textinputs['rl_aim'],
                     game_parts.textinputs['rm_aim'],
                     game_parts.textinputs['rr_aim']]

    args_dict = dict(startAutomateButton = game_parts.buttons['start'],
                     makeCounterButton = game_parts.buttons['make_counter'],
                     automationTable = game_parts.tables['automation'],
                     automationTableSrc = game_parts.sources['automation_table'],
                     counterMadeDiv = game_parts.divs['counter_made'],
                     goalieCounterSrc = game_parts.sources['goalie_counter'],
                     aimTextInputs = aimTextInputs)

    b_make_counter_click = CustomJS(args = args_dict, code = makeCounterCode)

    game_parts.buttons['make_counter'].js_on_click(b_make_counter_click)
#</editor-fold>
