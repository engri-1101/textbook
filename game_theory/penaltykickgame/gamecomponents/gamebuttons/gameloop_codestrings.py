#This file contains the JavaScript code strings that are used for the main game
#loop.

#Any JavaScript Function defined in the strings with a name starting with the
#'_' character is a helper function.


#TODO: continue improving code efficiency.
#<editor-fold Functions:
  #<editor-fold iterationText():
iterationText = """
function iterationText(){
  //set lines of game text to reflect game state:
  const game_text = txt.data['text'];

  game_text[0] = 'Rounds played: ' + rounds_played;
  game_text[1] = 'Total score: ' + game_score;
  game_text[3] = ((goal == 1) ? 'GOAL!' : 'Blocked');

  txt.change.emit();
}
"""
  #</editor-fold>
  #<editor-fold rollKickerAction():
rollKickerAction = """
function rollKickerAction(){
  //Set constants for determining rolled action:
  const feet =  ['Right', 'Right', 'Left', 'Left', 'Left'];
  const kicks = ['Middle', 'Left', 'Right', 'Middle', 'Left'];

  //Set chance checking array:
  const action_chances = new Array(5);
  action_chances[4] = chances[0];
  for (let i = 1; i < 5; i++){
    action_chances[4 - i] = action_chances[5 - i] + chances[i];
  }

  //Select and return action:
  let vals = ['Right', 'Right'];
  const action_roll = Math.random();
  for(let i = 0; i < 5; i++){
    vals = ((action_roll <= action_chances[i]) ? [feet[i], kicks[i]] : vals);
  }
  return vals;
}
"""
  #</editor-fold>
  #<editor-fold fictitiousPlay():
fictitiousPlay = """
//Handle Goalie Decision
function fictitiousPlay(){
  //Set decision making values to use according to kicker_foot:
  const freqs = ((v_fl) ? freq.slice(0, 3) : freq.slice(3, 6)).map(x => x);
  const sfprobsdict = ((v_fl) ? l_dict : r_dict); //grab correct probs dict

  //Create array of empirical frequencies of striker choices:
  const tsr = freqs.reduce(f_sum); //Set total sample rolls
  const e_fs = ((tsr != 0) ? freqs.map(x => x / tsr) : [1/3, 1/3, 1/3]);

  //Set goalie perceived risks:
  const risks = new Array(3).fill(0);
  for (let i = 0; i < 3; i++){
    for (let j = 0; j < 3; j++){
      risks[i] += (e_fs[j] * sfprobsdict[directions[j] + directions[i]]);
    }
  }

  //set action to direction with minimum risk:
  const action = directions[risks.indexOf(Math.min(...risks))];

  return [action, ...risks];
}
"""
  #</editor-fold>
  #<editor-fold optimalMixedStrategy():
#Runs the optimal mixed strategy found in the lab.
optimalMixedStrategy = """
function optimalMixedStrategy(){
  //selects and returns an action based off of optimal mixed strategy chances:
  return (
    (Math.random() >= {'Left' : 0.8, 'Right' : 0.7419}[kicker_foot]) ?
    kicker_foot : 'Middle'
  );
}
"""
  #</editor-fold>
  #<editor-fold randomChoice():
#Runs random choices, a strategy for the goalie where they pick their actions
#at random.
randomChoice = """
function randomChoice(){
  //Selects and returns an action from directions at an equal chance:
  return directions[Math.round(Math.random() * 3 - 0.5)];
}
"""
  #</editor-fold>
  #<editor-fold goalieCheats():
#This codestring runs the goalie cheats strategy, a strategy where the goalie
#Uses the optimal pure strategy to counter the player's mixed strategy.
goalieCheats = """
function goalieCheats(){
  //return the action of the pure strategy corresponding to the kicker foot:
  return directions[counter_source.data[
    {'Left' : 'chances_l', 'Right' : 'chances_r'}[kicker_foot]
  ].indexOf(1)];
}
"""
  #</editor-fold>
  #<editor-fold _handleFigureVisibility():
_handleFigureVisibility = """
function _handleFigureVisibility(){
  b_auto_next.visible = false;
  game_figure.visible = false;
  distribution_table.visible = false;

  b_fig_1.visible = true;
  b_fig_2.visible = true;
  b_fig_3.visible = v_fict;
  b_fig_4.visible = true;

  stats_fig_1.visible = true;
  stats_fig_2.visible = false;
  stats_fig_3.visible = false;
  stats_fig_4.visible = false;
}
"""
  #</editor-fold>
  #<editor-fold iterationScoring():
iterationScoring = """
function scoring(){
  //store column references:
  const scoring_chance = dist_data['striker_score_chance'];
  const scoring_roll = dist_data['striker_score_roll'];

  //set function values:
  const score_roll = Math.random();
  const score_chance = score_probs[kicker_foot][kicker_kick + goalie_action];
  const rounds_played = (parseInt(nround.text) + 1);

  //Calculate iteration score:
  let round_score = ((score_roll <= score_chance) ? +1 : -1);

  //Update round scoring stats:
  scoring_chance.fill(0);
  scoring_roll.fill(0);
  scoring_chance[a_i_kfkk] = score_chance;
  scoring_roll[a_i_kfkk] = score_roll.toString().substring(0, 8);

  //Update text:
  nround.text = rounds_played.toString();
  const current_game_score = parseInt(score.text) + round_score;
  score.text = current_game_score.toString();

  return [round_score, current_game_score, rounds_played, score_chance];
}
"""
  #</editor-fold>
  #<editor-fold _moveGoalie():
_moveGoalie = """
function _moveGoalie(x_loc){
  //Move both components of the goalie:
  goalie_body.x = x_loc;
  goalie_head.x = x_loc;
}
"""
  #</editor-fold>
  #<editor-fold animateIteration():
animateIteration = """
function animateIteration(){
  //Set positions and store ball roll for handling cases:
  const positions = {'Left' : [37,43], 'Middle' : [47,53], 'Right' : [57,63]};
  const ball_roll = Math.round(Math.random());

  //move to default positions:
  ball.x = positions[kicker_kick][ball_roll];
  ball.y = 63;
  _moveGoalie(positions[goalie_action][Math.round(Math.random())]);

  if(goalie_action == kicker_kick){
    //If blocked move goalie to ball, otherwise move to other position:
    _moveGoalie(ball.x);
    if(goal == 1){ _moveGoalie(positions[goalie_action][[1, 0][ball_roll]]); }
  } else if(goal == -1){
    //Move ball out of goal:
    ball.x = (
      {'Left' : 30, 'Middle' : [30,70][ball_roll], 'Right' : 70}[kicker_kick]
    );
  }
}
"""
  #</editor-fold>
  #<editor-fold _selectFromKFGA():
_selectFromKFGA = """
function _selectFromKFGA(){
  //return calculated value (adjust for kicker foot and goalie action indexes):
  return (adjust_kfr + d_i_ga);
}
"""
  #</editor-fold>
  #<editor-fold _updateDecisionTableRisks():
_updateDecisionTableRisks = """
function _updateDecisionTableRisks(){
  //Function Values:
  const perceived_risks = dist_data['goalie_perceived_risks'];
  const index = adjust_kfr;

  //Update Table Column:
  perceived_risks.fill(0);
  perceived_risks[index] =     danger_goalie_left.toString().substring(0, 8);
  perceived_risks[index + 1] = danger_goalie_middle.toString().substring(0, 8);
  perceived_risks[index + 2] = danger_goalie_right.toString().substring(0, 8);
}
"""
  #</editor-fold>
  #<editor-fold goalieDecisionTracking():
goalieDecisionTracking = """
function goalieDecisionTracking(){

  //Increase corresponding trackers to KFKK and KFGA:
  freq[a_i_kfkk] += 1;
  dist_data['decisions'][_selectFromKFGA()] += 1;

  //Update table perceived risks if fictitious play:
  if(v_fict){ _updateDecisionTableRisks(); }

  //Update table by finalizing changes to source:
  distribution_source.change.emit();
}
"""
  #</editor-fold>
  #<editor-fold _selectFromKFKK():
_selectFromKFKK = """
function _selectFromKFKK(){
  //return calculated value (adjust for kicker foot and kicker kick indexes):
  return adjust_kfr + directions.indexOf(kicker_kick);
}
"""
  #</editor-fold>
  #<editor-fold _fig1Iteration():
_fig1Iteration = """
function _fig1Iteration(fig_1_data, sections){
  //Increase section value of iteration result by 1:
  fig_1_data[sections[((goal == 1) ? 0 : d_i_ga + 1)]][a_i_kfkk] += 1;
}
"""
  #</editor-fold>
  #<editor-fold _fig1Adjust():
_fig1Adjust = """
function _fig1Adjust(fig_1_data, sections){
  //iterate through the 6 bars to find the max value:
  let max = 0;
  for(let i = 0; i < 6; i++){
    max = Math.max(sections.map(a => fig_1_data[a][i]).reduce(f_sum), max);
  }

  //Adjust the figure bounds according to max value:
  stats_fig_1.y_range.end = Math.round(max * 1.1);
}
"""
  #</editor-fold>
  #<editor-fold updateFig1():
updateFig1 = """
function updateFig1(){
  //create constants for referencing:
  const fig_1_data = stats_fig_1_source.data;
  const sections = ['scored_y', 'blockedl_y', 'blockedm_y', 'blockedr_y'];

  //Update the figure for the iteration:
  _fig1Iteration(fig_1_data, sections);

  //Make final adjustments if it is the final iteration:
  if(v_last_round){ _fig1Adjust(fig_1_data, sections); }

  //Update the figure by finalizing the changes to the data source:
  stats_fig_1_source.change.emit();
}
"""
  #</editor-fold>
  #<editor-fold _fig2Iteration():
_fig2Iteration = """
function _fig2Iteration(fig_2_data){
  //plot score on graph:
  fig_2_data['ys'][rounds_played] = game_score;

  //Store reference to column:
  const chance_ys = fig_2_data['chance_ys'];

  //Average expected score = round before + 2 times the score chance -1:
  chance_ys[rounds_played] = (chance_ys[rounds_played - 1] + (
    2 * scored_chance - 1
  ));
}
"""
  #</editor-fold>
  #<editor-fold _fig2Adjust():
_fig2Adjust = """
function _fig2Adjust(fig_2_data){
  //Set initial max and min for resizing graph
  let min_val = 0;
  let max_val = 0;

  //Iterate through data for game iterations:
  const ys = fig_2_data['ys'];
  for(let i = 0; i <= iters_to_run; i++){
    //store data point value:
    const val = ys[i];

    //Adjust min and max as needed:
    min_val = Math.min(min_val, val);
    max_val = Math.max(max_val, val);
  }

  //Calulate amount to add as a buffer to size of graph:
  const buffer = Math.round((Math.abs(max_val) + Math.abs(min_val)) * 1/8) + 1;

  //Adjust max and min by buffer:
  max_val += buffer;
  min_val -= buffer;

  //Resize Graph:
  stats_fig_2.y_range.end   = max_val;
  stats_fig_2.y_range.start = min_val;

  stats_fig_2.x_range.start -= 0.5;
  stats_fig_2.x_range.end   += 0.5;

  //Resize hit boxes:
  fig_2_data['height'] = new Array(iters_to_run + 1).fill(Math.max(
    Math.abs(max_val), Math.abs(min_val)
  ) * 2);
}
"""
  #</editor-fold>
  #<editor-fold updateFig2():
updateFig2 = """
function updateFig2(){
  //Store reference to fig 2 data:
  const fig_2_data = stats_fig_2_source.data;

  //Update the figure for the iteration:
  _fig2Iteration(fig_2_data);

  //Adjust the figure as needed if it is the last iteration:
  if(v_last_round) { _fig2Adjust(fig_2_data); }

  //Update the source to finalize the changes to the figure:
  stats_fig_2_source.change.emit();
}
"""
  #</editor-fold>
  #<editor-fold _fig3CalcPointVal():
_fig3CalcPointVal = """
function _fig3CalcPointVal(chances_list, selected_probs, ga){
  //Risk value is sum of the chance of each striker action * the score chance
  //if the goalie takes the position ga:
  let value = 0;
  for (let j = 0; j < 3; j++){
    value += (chances_list[j] * selected_probs[directions[j] + ga]);
  }
  return value;
}
"""
  #</editor-fold>
  #<editor-fold _fig3Iteration():
_fig3Iteration = """
function _fig3Iteration(ys){
  //Calculate total sample rolls for each side:
  const tsr_l = freq.slice(0, 3).reduce(f_sum);
  const tsr_r = freq.slice(3, 6).reduce(f_sum);

  //Calculate the predicted chances of the striker taking each position:
  const p_chances = new Array(6);
  for (let i = 0; i < 6; i++){
    const tsr = ((i < 3) ? tsr_l : tsr_r);
    p_chances[i] = ((tsr != 0 ? (freq[i] / tsr) : 1/3));
  }

  //Calculate and change predicted risk values:
  for (let i = 0; i < 6; i++){
    ys[i][rounds_played] = ((i < 3) ? _fig3CalcPointVal(
      p_chances.slice(0, 3), l_dict, directions[i]
    ) : _fig3CalcPointVal(p_chances.slice(3, 6), r_dict, directions[i - 3]));
  }
}
"""
  #</editor-fold>
  #<editor-fold _fig3Adjust():
_fig3Adjust = """
function _fig3Adjust(fig_3_data, ys){
  //store fig_3_data hb columns for iteration and reference:
  const hbs = [fig_3_data['hb1'], fig_3_data['hb2'], fig_3_data['hb3'],
               fig_3_data['hb4'], fig_3_data['hb5'], fig_3_data['hb6']];

  //Adjustment loop:
  let fig_3_min_val = 1;
  let fig_3_max_val = 0;
  let hbhs = new Array(6);
  let risks = new Array(6);

  for(let i = 0; i <= iters_to_run; i++){
    //update min and max, store iteration values:
    for (let y_i = 0; y_i < 6; y_i++){
      const val = ys[y_i][i];
      fig_3_max_val = Math.max(fig_3_max_val, val);
      fig_3_min_val = Math.min(fig_3_min_val, val);
      risks[y_i] = val;
    }

    //Sort goalie perceived risk values in descending order:
    risks.sort((a, b) => b - a);

    //Resize hitboxes according to previously calculated values:
    for (let hb_i = 0; hb_i < 6; hb_i++){
      let val = ((hb_i == 5) ? 1 : ((risks[5 - hb_i] + risks[4 - hb_i]) / 2));
      for (let prev_hb = 0; prev_hb < hb_i; prev_hb++){
        val -= hbhs[prev_hb];
      }
      hbhs[hb_i] = val;
      hbs[hb_i][i] = val;
    }
  }

  //Adjust graph based off of stored values:
  const buffer = Math.max(Math.round(fig_3_max_val - fig_3_min_val) / 10, 0.05);
  fig_3_max_val = Math.round(fig_3_max_val * 10) / 10;
  fig_3_min_val = Math.round(fig_3_min_val * 10) / 10;
  stats_fig_3.y_range.end   = Math.min(fig_3_max_val + buffer, 1);
  stats_fig_3.y_range.start = Math.max(fig_3_min_val - buffer, 0);
  stats_fig_3.x_range.start -= 0.5;
  stats_fig_3.x_range.end   += 0.5;
}
"""
  #</editor-fold>
  #<editor-fold updateFig3():
updateFig3 = """
function updateFig3(){
  //Store values for reference:
  let fig_3_data = stats_fig_3_source.data;
  const ys = [fig_3_data['ll_ys'], fig_3_data['lm_ys'], fig_3_data['lr_ys'],
              fig_3_data['rl_ys'], fig_3_data['rm_ys'], fig_3_data['rr_ys']];

  //Update plot points:
  _fig3Iteration(ys);

  //Make final adjustments to graph on last iteration:
  if(v_last_round){ _fig3Adjust(fig_3_data, ys); }

  //Finalize changes:
  stats_fig_3_source.change.emit();
}
"""
  #</editor-fold>
  #<editor-fold updateFig4():
updateFig4 = """
function updateFig4(){
  const fig_4_data = stats_fig_4_source.data;
  const ys = fig_4_data['ys'];
  const feet = fig_4_data['feet'];
  const fig_directions = fig_4_data['directions'];
  const actions = fig_4_data['actions'];

  ys[rounds_played] = scored_chance;
  feet[rounds_played] = kicker_foot;
  fig_directions[rounds_played] = kicker_kick;
  actions[rounds_played] = goalie_action;

  if(v_last_round){
    fig_4_data['xs'].shift();
    fig_4_data['highlight_alphas'].shift();
    fig_4_data['avgs_placeholder'].shift();
    ys.shift();
    feet.shift();
    fig_directions.shift();
    actions.shift();

    stats_fig_4.x_range.start -= 0.5;
    stats_fig_4.x_range.end += 0.5;
  }

  stats_fig_4_source.change.emit();
}
"""
  #</editor-fold>

function_definitions = (iterationText + rollKickerAction + fictitiousPlay
                        + optimalMixedStrategy + randomChoice + goalieCheats
                        + _handleFigureVisibility + iterationScoring
                        + _moveGoalie + animateIteration + _selectFromKFGA
                        + _updateDecisionTableRisks + goalieDecisionTracking
                        + _selectFromKFKK + _fig1Iteration + _fig1Adjust
                        + updateFig1 + _fig2Iteration + _fig2Adjust + updateFig2
                        + _fig3CalcPointVal + _fig3Iteration + _fig3Adjust
                        + updateFig3 + updateFig4)
#</editor-fold>

#<editor-fold Game Iteration:
game_iteration = """
const r_dict = {'LeftLeft'   : 0.55, 'LeftMiddle'   : 0.65, 'LeftRight'   : 0.93,
                'MiddleLeft' : 0.74, 'MiddleMiddle' : 0.60, 'MiddleRight' : 0.72,
                'RightLeft'  : 0.95, 'RightMiddle'  : 0.73, 'RightRight'  : 0.70}
const l_dict = {'LeftLeft'   : 0.67, 'LeftMiddle'   : 0.70, 'LeftRight'   : 0.96,
                'MiddleLeft' : 0.74, 'MiddleMiddle' : 0.60, 'MiddleRight' : 0.72,
                'RightLeft'  : 0.87, 'RightMiddle'  : 0.65, 'RightRight'  : 0.61}
const score_probs = {'Right' : r_dict, 'Left' :  l_dict};

const chances = chances_source.data['chances'];
const dist_data = distribution_source.data;
const freq = dist_data['freq'];
const iters_to_run = parseInt(iterations_to_run.text);

const game_strat = strategy_to_use.text;

const v_fict = ((game_strat == 'Fictitious_Play'));
const directions = ['Left', 'Middle', 'Right'];

const f_sum = ((a, b) => a + b);
let danger_goalie_left = 0;
let danger_goalie_middle = 0;
let danger_goalie_right = 0;

let goalie_action = '';

let kicker_foot = '';
let kicker_kick = '';

let goal = 0;
let game_score = 0;
let rounds_played = 0;

let scored_chance = 0;

[kicker_foot, kicker_kick] = rollKickerAction();

const v_fl = (kicker_foot == 'Left');
let adjust_kfr = ((!v_fl) ? 3 : 0);

if(v_fict){
  [goalie_action, danger_goalie_left,
   danger_goalie_middle, danger_goalie_right] = fictitiousPlay();
} else{
  goalie_action = {'Mixed_Strategy' : optimalMixedStrategy,
                   'Random' : randomChoice,
                   'Goalie_Cheats' : goalieCheats}[game_strat]();
}
const d_i_ga = directions.indexOf(goalie_action); //DirectionsIndexGoalieAction
const a_i_kfkk = _selectFromKFKK(); //Actions index KFKK

[goal, game_score, rounds_played, scored_chance] = scoring();
const v_last_round = (rounds_played >= iters_to_run);

animateIteration();

goalieDecisionTracking();

updateFig1();
updateFig2();
if(v_fict){ updateFig3(); }
updateFig4();

if(v_last_round){ _handleFigureVisibility(); }

iterationText();
"""
#</editor-fold>

game_iteration += function_definitions

#<editor-fold start button Initial Gui Display:
#This code string changes the visibility values of various game gui elements
#in order to change the user view from that used in the earlier menu like
#screens to one used for the game screens.
initial_gui_display = """
b_start_automate.visible = false;
b_auto_next.visible = true;
ll_aim_text_input.visible = false;
lm_aim_text_input.visible = false;
lr_aim_text_input.visible = false;
rl_aim_text_input.visible = false;
rm_aim_text_input.visible = false;
rr_aim_text_input.visible = false;
iterations_slider.visible = false;
strategy_dropdown.visible = false;
automation_table.visible = false;
distribution_table.visible = true;
"""
#</editor-fold>

b_automate_start_code = (initial_gui_display
                         + game_iteration)
