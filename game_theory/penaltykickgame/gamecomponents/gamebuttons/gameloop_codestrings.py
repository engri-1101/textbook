#This file contains the JavaScript code strings that are used for the main game
#loop.

#Any JavaScript Function defined in the strings with a name starting with the
#'_' character is a helper function.


#TODO: Recode current functions for efficiency, readability and formatting.
#No long functions or repetitive code. Following that, Reorganize code strings
#so that all functions are defined first, and the game is run from a single,
#short string that makes the function calls.
#<editor-fold automate_start_code Initial Gui Display Code String:
#This code string changes the visibility values of various game gui elements
#in order to change the user view from that used in the earlier menu like
#screens to one used for the game screens.
automate_start_code_initial_gui_display = """
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

#HAS BEEN RECODED
#<editor-fold create_automate_loop_constants:
#This code string initializes the values for constants that are used accross
#multiple sections of the main game loop.
create_automate_loop_constants = """
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
"""
#</editor-fold>

#HAS BEEN RECODED!
#<editor-fold create_automate_loop_state_lets:
#This code string initializes the lets used accross the main game loop for
#tracking purposes.
create_automate_loop_state_lets = """
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
"""
#</editor-fold>

#Combine the two code strings that create values used accross the main game loop.
#Both of these must be run for every iteration of the main game loop.
automate_loop_setup = (create_automate_loop_constants
                       + create_automate_loop_state_lets)

#HAS BEEN RECODED!
#<editor-fold automate_loop_iteration_display
  #<editor-fold iterationText:
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
  #<editor-fold run iterationText:
run_iteration_text = """
iterationText();
"""
  #</editor-fold>
automate_loop_iteration_display = ((iterationText) # Functions
                                   + run_iteration_text) #actual function call
#</editor-fold>

#HAS BEEN RECODED!
#<editor-fold automate_loop_roll_kicker_action
#This code string uses the user's inputs to roll a random number to choose which
#strategy the kicker will use for the iteration.
rollKickerAction = """
function rollKickerAction(){
  //Set constants for determining rolled action:
  const action_chances = new Array(5);
  for (let i = 0; i < 5; i++){
    action_chances[4 - i] = ((i > 0) ? action_chances[5 - i] : 0) + chances[i];
  }
  const feet =  ['Right', 'Right', 'Left', 'Left', 'Left'];
  const kicks = ['Middle', 'Left', 'Right', 'Middle', 'Left'];

  //Set default values:
  let foot = 'Right';
  let kick = 'Right';

  //Roll action:
  let action_roll = Math.random();

  //Update values:
  for(let i = 0; i < 5; i++){
    const val = action_roll <= action_chances[i];
    foot = ((val) ? feet[i] : foot);
    kick = ((val) ? kicks[i] : kick);
  }

  return [foot, kick];
}
"""
run_rollKickerAction = """
[kicker_foot, kicker_kick] = rollKickerAction();
"""

automate_loop_roll_kicker_action = ((rollKickerAction) #Functions
                                    + run_rollKickerAction) #Actual function call
#</editor-fold>

#HAS BEEN RECODED!
#<editor-fold fictitious play:
fictitiousPlay = """
//Handle Goalie Decision
function fictitiousPlay(){
  //Set decision making values to use according to kicker_foot:
  const v_f = (kicker_foot == 'Left');
  const freqs = ((v_f) ? freq.slice(0, 3) : freq.slice(3, 6)).map(x => x);
  const sfprobsdict = ((v_f) ? l_dict : r_dict); //grab correct probs dict

  const tsr = freqs.reduce((a, b) => a + b); //Set total sample rolls

  //Map empirical frequencies of striker choices:
  const c_ads = ((tsr != 0) ? freqs.map(x => x/tsr) : [1/3, 1/3, 1/3]);

  //Set goalie perceived risks:
  const directions = ['Left', 'Middle', 'Right'];
  const risks = new Array(3).fill(0);
  for (let i = 0; i < 3; i++){
    for (let j = 0; j < 3; j++){
      risks[i] += (c_ads[j] * sfprobsdict[directions[j] + directions[i]]);
    }
  }

  //set action to direction with minimum risk:
  const action = directions[risks.indexOf(Math.min(...risks))];

  return [action, ...risks];
}
"""
run_fictitious_play = """
[goalie_action, danger_goalie_left,
 danger_goalie_middle, danger_goalie_right] = fictitiousPlay();
"""
do_fictitious_play = ((fictitiousPlay) # function
                      + run_fictitious_play) # actual function call
#</editor-fold>

#HAS BEEN RECODED!
#<editor-fold run_optimal_mixed_strategy
#Runs the optimal mixed strategy found in the lab.
optimalMixedStrategy = """
function optimalMixedStrategy(){
  //Obtain necessary chance of taking actions:
  const roll_reqs = {'Left' : 0.8, 'Right' : 0.7419}[kicker_foot];

  //calculate and return value:
  return ((Math.random() >= roll_reqs) ? kicker_foot : 'Middle');
}
"""
run_optimal_mixed_strategy = """
goalie_action = optimalMixedStrategy();
"""

do_optimal_mixed_strategy = ((optimalMixedStrategy) #Function
                             + run_optimal_mixed_strategy) # actual function call
#</editor-fold>

#HAS BEEN RECODED!
#<editor-fold run_random_choices
#Runs random choices, a strategy for the goalie where they pick their actions
#at random.
randomChoice = """
function randomChoice(){
  //Selects and returns an index in the below list at an equal chance:
  return ['Left', 'Middle', 'Right'][Math.round(Math.random() * 3 - 0.5)];
}
"""
run_random_choice = """
goalie_action = randomChoice();
"""
do_random_choices = ((randomChoice) #Function
                     + run_random_choice) # actual function call
#</editor-fold>

#HAS BEEN RECODED!
#<editor-fold run_goalie_cheats
#This codestring runs the goalie cheats strategy, a strategy where the goalie
#Uses the optimal pure strategy to counter the player's mixed strategy.
goalieCheats = """
function goalieCheats(){
  //store reference to data to check:
  const data = counter_source.data;

  //Store the pure strategy to use:
  const counter = {'Left' : data['chances_l'],
                   'Right' : data['chances_r']}[kicker_foot];

  //return the action dictated by the pure strategy:
  return ['Left', 'Middle', 'Right'][counter.indexOf(1)];
}
"""
run_goalie_cheats = """
goalie_action = goalieCheats();
"""
do_goalie_cheats = ((goalieCheats) #Function
                    + run_goalie_cheats) #Actual function call
#</editor-fold>

#runs the strategy designated
automate_loop_handle_goalie_decision = """
if(strategy_to_use.text == 'Fictitious_Play'){
  """ + do_fictitious_play + """
} else if(strategy_to_use.text == 'Mixed_Strategy'){
  """ + do_optimal_mixed_strategy + """
} else if(strategy_to_use.text == 'Random'){
  """ + do_random_choices + """
} else if(strategy_to_use.text == 'Goalie_Cheats'){
  """ + do_goalie_cheats + """
}
"""

#HAS BEEN RECODED!
#<editor-fold automate_loop_handle_scoring
#This code string handles the scoring of the game, and updates a couple things
#accordingly.
  #<editor-fold handle figure visibility:
_handleFigureVisibility = """
function _handleFigureVisibility(){
  b_auto_next.visible = false;
  game_figure.visible = false;
  distribution_table.visible = false;

  b_fig_1.visible = true;
  b_fig_2.visible = true;
  b_fig_3.visible = (strategy_to_use.text == 'Fictitious_Play');
  b_fig_4.visible = true;

  stats_fig_1.visible = true;
  stats_fig_2.visible = false;
  stats_fig_3.visible = false;
  stats_fig_4.visible = false;
}
"""
  #</editor-fold>
  #<editor-fold fig 4 adjustments helper:
_fig4Adjust = """
function _fig4Adjust(fig_4_data){

  fig_4_data['xs'].shift();
  fig_4_data['ys'].shift();
  fig_4_data['feet'].shift();
  fig_4_data['directions'].shift();
  fig_4_data['actions'].shift();
  fig_4_data['highlight_alphas'].shift();
  fig_4_data['avgs_placeholder'].shift();

  stats_fig_4.x_range.start -= 0.5;
  stats_fig_4.x_range.end += 0.5;
}
"""
  #</editor-fold>
  #<editor-fold update fig 4:
updateFig4 = """
function updateFig4(rounds_played, score_chance){
  const fig_4_data = stats_fig_4_source.data;

  fig_4_data['ys'][rounds_played] = score_chance;
  fig_4_data['feet'][rounds_played] = kicker_foot;
  fig_4_data['directions'][rounds_played] = kicker_kick;
  fig_4_data['actions'][rounds_played] = goalie_action;

  if(rounds_played >= iters_to_run){ _fig4Adjust(fig_4_data); }

  stats_fig_4_source.change.emit();
}
"""
  #</editor-fold>
  #<editor-fold iteration scoring:
iterationScoring = """
function scoring(){
  //store column references:
  const scoring_chance = dist_data['striker_score_chance'];
  const scoring_roll = dist_data['striker_score_roll'];

  //set function values:
  let score_roll = Math.random();
  let score_chance = score_probs[kicker_foot][kicker_kick + goalie_action];
  let index_to_update = _selectFromKFKK();
  let rounds_played = (parseInt(nround.text) + 1);

  //Calculate iteration score:
  let round_score = ((score_roll <= score_chance) ? +1 : -1);

  //Update figure 4:
  updateFig4(rounds_played, score_chance);

  //Reset iteration scoring stats:
  scoring_chance.fill(0);
  scoring_roll.fill(0);

  //Update scoring stats:
  scoring_chance[index_to_update] = score_chance;
  scoring_roll[index_to_update] = score_roll.toString().substring(0, 8);

  //Make adjustments to figure related component visibilities:
  if(rounds_played >= iters_to_run){ _handleFigureVisibility(); }

  //Update text:
  nround.text = rounds_played.toString();
  let current_game_score = parseInt(score.text) + round_score;
  score.text = current_game_score.toString();

  return [round_score, current_game_score, rounds_played, score_chance];
}
"""
  #</editor-fold>
  #<editor-fold run iteration scoring:
run_iteration_scoring = """
[goal, game_score, rounds_played, scored_chance] = scoring();
"""
  #</editor-fold>
automate_loop_handle_scoring = ((_handleFigureVisibility + _fig4Adjust
                                 + updateFig4 + iterationScoring) #Functions
                                + run_iteration_scoring) #actual function call
#</editor-fold>

#HAS BEEN RECODED!
#<editor-fold automate_loop_animation
_moveGoalie = """
function _moveGoalie(x_loc){
  //Move both components of the goalie:
  goalie_body.x = x_loc;
  goalie_head.x = x_loc;
}
"""
animateIteration = """
function animateIteration(){
  //Set positions and store ball roll for handling cases:
  const positions = {'Left' : [37,43], 'Middle' : [47,53], 'Right' : [57,63]};
  const ball_roll = Math.round(Math.random());
  ball.y = 63;

  //move to default positions:
  ball.x = positions[kicker_kick][ball_roll];
  _moveGoalie(positions[goalie_action][Math.round(Math.random())]);

  if(goalie_action == kicker_kick){
    //If blocked move goalie to ball, otherwise move to other position:
    _moveGoalie(ball.x);
    if(goal == 1){ _moveGoalie(positions[goalie_action][[1, 0][ball_roll]]); }
  } else if(goal == -1){
    //Move ball out of goal:
    ball.x = {'Left' : 30, 'Middle' : [30,70][ball_roll],
              'Right' : 70}[kicker_kick];
  }
}
"""
run_animate_iteration = """
animateIteration();
"""
automate_loop_animation = ((_moveGoalie + animateIteration) #Functions
                           + run_animate_iteration) #actual function call
#</editor-fold>

#HAS BEEN RECODED!
#<editor-fold automate_loop_update_fictitious_decision_tracking
  #<editor-fold select from KFGA helper function:
_selectFromKFGA = """
function _selectFromKFGA(){
  //Instantiate selected (the function's return value):
  let selected = ((kicker_foot == 'Right') ? 3 : 0);

  //Adjust selected_bar according to goalie_action:
  selected += ['Left', 'Middle', 'Right'].indexOf(goalie_action);

  return selected;
}
"""
  #</editor-fold>
  #<editor-fold update risks helper function:
_updateDecisionTableRisks = """
function _updateDecisionTableRisks(){
  //Store reference to column:
  const perceived_risks = dist_data['goalie_perceived_risks'];

  //Select indexes to work with based off of kicker foot:
  let selected_pr_index = ((kicker_foot == 'Right') ? 3 : 0);

  //Set column to 0s:
  perceived_risks.fill(0);

  //Rewrite selected values to their associated risks:
  perceived_risks[selected_pr_index] =     danger_goalie_left.toString().substring(0, 8);
  perceived_risks[selected_pr_index + 1] = danger_goalie_middle.toString().substring(0, 8);
  perceived_risks[selected_pr_index + 2] = danger_goalie_right.toString().substring(0, 8);
}
"""
  #</editor-fold>
  #<editor-fold goalie decision tracking function:
goalieDecisionTracking = """
function goalieDecisionTracking(){

  //Increase corresponding tracker to KFKK:
  freq[_selectFromKFKK()] += 1;

  //Increase corresponding tracker to KFGA:
  dist_data['decisions'][_selectFromKFGA()] += 1;

  //Update table perceived risks if fictitious play:
  if(strategy_to_use.text == 'Fictitious_Play'){ _updateDecisionTableRisks(); }

  //Update table by finalizing changes to source:
  distribution_source.change.emit();
}
"""
  #</editor-fold>
  #<editor-fold run goalie decision tracking:
run_goalie_decision_tracking = """
goalieDecisionTracking();
"""
  #</editor-fold>
automate_loop_update_decision_tracking = ((_selectFromKFGA
                                           + _updateDecisionTableRisks
                                           + goalieDecisionTracking) #Functions
                                          + run_goalie_decision_tracking)# actual function call
#</editor-fold>

#HAS BEEN RECODED!
#<editor-fold update_game_stats_figure_1
#This code string updates game stats figure 1
  #<editor-fold select from KFKK helper function:
_selectFromKFKK = """
function _selectFromKFKK(){
  //Instantiate selected (the function's return value):
  let selected = ((kicker_foot == 'Right') ? 3 : 0);

  //Adjust selected according to kicker_kick:
  selected += ['Left', 'Middle', 'Right'].indexOf(kicker_kick);

  return selected;
}
"""
  #</editor-fold>
  #<editor-fold fig 1 iteration helper function:
_fig1Iteration = """
function _fig1Iteration(fig_1_data){
  //Create a dict to use for selecting data columns according to iteration outcomes:
  const section = {'Left' : 'blockedl_y', 'Middle' : 'blockedm_y',
                   'Right' : 'blockedr_y'};

  //Increase the value of the correct bar by 1:
  if(goal == 1){
    fig_1_data['scored_y'][_selectFromKFKK()] += 1;
  } else{ fig_1_data[section[goalie_action]][_selectFromKFKK()] += 1; }
}
"""
  #</editor-fold>
  #<editor-fold fig 1 adjustments helper function:
_fig1Adjust = """
function _fig1Adjust(fig_1_data){
  //Instantiate max_val with initial value:
  let max_val = 0;

  //Create an array for iterating through the data columns:
  const data_bar_sections = [fig_1_data['scored_y'], fig_1_data['blockedl_y'],
                             fig_1_data['blockedm_y'],
                             fig_1_data['blockedr_y']];

  //iterate through the 6 bars:
  for(let i = 0; i <= 5; i++){

    //calculate the total of the bar's sections:
    let possible_max = 0;
    for(let section = 0; section < 4; section++){
      possible_max += data_bar_sections[section][i];
    }

    //Update max val if needed:
    max_val = Math.max(Math.round(possible_max * 11/10), max_val);
  }

  //Adjust the figure bounds:
  stats_fig_1.y_range.end = max_val;
}
"""
  #</editor-fold>
  #<editor-fold update fig 1 function:
updateFig1 = """
function updateFig1(){
  //store figure data for reference:
  const fig_1_data = stats_fig_1_source.data;

  //Update the figure for the iteration:
  _fig1Iteration(fig_1_data);

  //Make final adjustments if it is the final iteration:
  if(parseInt(nround.text) >= iters_to_run){ _fig1Adjust(fig_1_data); }

  //Update the figure by finalizing the changes to the data source:
  stats_fig_1_source.change.emit();
}
"""
  #</editor-fold>
  #<editor-fold run update fig 1:
run_update_fig_1 = """
updateFig1();
"""
  #</editor-fold>
update_game_stats_figure_1 = ((_selectFromKFKK + _fig1Iteration + _fig1Adjust
                               + updateFig1) # Functions
                              + run_update_fig_1) # actual function call
#</editor-fold>

#HAS BEEN RECODED!
#<editor-fold update_game_stats_figure_2
#This code string updates game stats figure 2
  #<editor-fold update fig 2 iteration:
_fig2Iteration = """
function _fig2Iteration(index, fig_2_data){
  fig_2_data['ys'][index] = parseInt(score.text);
  fig_2_data['chance_ys'][index] = (fig_2_data['chance_ys'][index - 1]
                                    + (2 * scored_chance - 1));
}
"""
  #</editor-fold>
  #<editor-fold fig 2 adjustments helper function:
_fig2Adjust = """
function _fig2Adjust(fig_2_data){
  //Set initial max and min for resizing graph
  let min_val = 0;
  let max_val = 0;

  //Iterate through data for game iterations:
  for(let i = 0; i <= iters_to_run; i++){
    //store data point value:
    const val = fig_2_data['ys'][i];

    //Adjust min and max as needed:
    min_val = Math.min(min_val, val);
    max_val = Math.max(max_val, val);
  }

  //Calulate amount to add as a buffer to size of graph:
  let buffer = (Math.round((Math.abs(max_val) + Math.abs(min_val)) * 1/8)) + 1;

  //Adjust max and min by buffer:
  max_val += buffer;
  min_val -= buffer;

  //Resize Graph:
  stats_fig_2.y_range.end   = max_val;
  stats_fig_2.y_range.start = min_val;

  stats_fig_2.x_range.start -= 0.5;
  stats_fig_2.x_range.end   += 0.5;

  //Resize hit boxes:
  fig_2_data['height'] = new Array(iters_to_run
                                   + 1).fill(Math.max(Math.abs(max_val),
                                                      Math.abs(min_val)) * 2);
}
"""
  #</editor-fold>
  #<editor-fold update fig 2 function:
updateFig2 = """
function updateFig2(){
  //Store reference to fig 2 data:
  const fig_2_data = stats_fig_2_source.data;

  //Store value of iteration index:
  let index = parseInt(nround.text);

  //Update the figure for the iteration:
  _fig2Iteration(index, fig_2_data);

  //Adjust the figure as needed if it is the last iteration:
  if(index >= iters_to_run){ _fig2Adjust(fig_2_data); }

  //Update the source to finalize the changes to the figure:
  stats_fig_2_source.change.emit();
}
"""
  #</editor-fold>
  #<editor-fold run update fig 2:
run_update_fig_2 = """
updateFig2();
"""
  #</editor-fold>
update_game_stats_figure_2 = ((_fig2Iteration + _fig2Adjust + updateFig2) # Functions
                              + run_update_fig_2) # actual function call
#</editor-fold>

#HAS BEEN RECODED!
#<editor-fold update_game_stats_figure_3
#This codestring updates game stats figure 3
  #<editor-fold update fig 3 point helper function:
_fig3CalcPointVal = """
function _fig3CalcPointVal(chances_list, scoreprobs_list, ga){
  const aim_directions = ['Left', 'Middle', 'Right'];

  let value = 0;
  for (let j = 0; j < 3; j++){
    value += (chances_list[j] * scoreprobs_list[aim_directions[j] + ga]);
  }
  return value;
}
"""
  #</editor-fold>
  #<editor-fold update fig 3 iteration helper function:
_fig3Iteration = """
function _fig3Iteration(ys, index){
  //Store frequencies of striker choices:
  const freq_ll = freq[0];
  const freq_lm = freq[1];
  const freq_lr = freq[2];
  const freq_rl = freq[3];
  const freq_rm = freq[4];
  const freq_rr = freq[5];

  //Store totals of frequencies:
  const chance_l_total = freq_ll + freq_lm + freq_lr;
  const chance_r_total = freq_rl + freq_rm + freq_rr;

  //Instantiate perceived choice chances with default values:
  let chance_ll = ((chance_l_total != 0) ? (freq_ll / chance_l_total) : 1/3);
  let chance_lm = ((chance_l_total != 0) ? (freq_lm / chance_l_total) : 1/3);
  let chance_lr = ((chance_l_total != 0) ? (freq_lr / chance_l_total) : 1/3);
  let chance_rl = ((chance_r_total != 0) ? (freq_rl / chance_r_total) : 1/3);
  let chance_rm = ((chance_r_total != 0) ? (freq_rm / chance_r_total) : 1/3);
  let chance_rr = ((chance_r_total != 0) ? (freq_rr / chance_r_total) : 1/3);

  //Store values for updating points:
  const chances_l = [chance_ll, chance_lm, chance_lr];
  const chances_r = [chance_rl, chance_rm, chance_rr];
  const goalie_actions = ['Left', 'Middle', 'Right', 'Left', 'Middle', 'Right'];
  const score_probs_l = score_probs['Left'];
  const score_probs_r = score_probs['Right'];

  //Update points corresponding to left footed strikers:
  for(let i = 0; i < 3; i++){
    ys[i][index] = _fig3CalcPointVal(chances_l, score_probs_l,
                                     goalie_actions[i]);
  }
  //Update points corresponding to right footed strikers:
  for(let i = 3; i < 6; i++){
    ys[i][index] = _fig3CalcPointVal(chances_r, score_probs_r,
                                     goalie_actions[i]);
  }
}
"""
  #</editor-fold>
  #<editor-fold fig 3 Final adjustments helper function:
_fig3Adjust = """
function _fig3Adjust(fig_3_data, ys){
  //store fig_3_data hb columns for iteration and reference:
  const hbs = [fig_3_data['hb1'], fig_3_data['hb2'], fig_3_data['hb3'],
               fig_3_data['hb4'], fig_3_data['hb5'], fig_3_data['hb6']];

  //Instantiate min and max values for resizing the graph:
  let fig_3_min_val = 1;
  let fig_3_max_val = 0;

  //Instantiate constant for graph size buffer:
  const fig_3_buffer = 0.1;

  //Iterate through data for each game iteration:
  for(let i = 0; i <= iters_to_run; i++){
    //Instantiate array for storing goalie perceived risk values:
    let risks = new Array(6);

    //Iterate through the list of perceived risk column ys:
    for (let y_index = 0; y_index < 6; y_index++){
      //Store value for reference:
      const val = ys[y_index][i];

      //Adjust max and min as needed:
      fig_3_max_val = Math.max(fig_3_max_val, val);
      fig_3_min_val = Math.min(fig_3_min_val, val);

      //Store goalie perceived risk values:
      risks[y_index] = val;
    }

    //Sort goalie perceived risk values in descending order:
    risks.sort((a, b) => b - a);

    //Instantiate new array for storing hitbox height information:
    let hbhs = new Array(6);

    //Iterate through hbhs array to handle hitbox resizing:
    for (let hb_index = 0; hb_index < 6; hb_index++){

      //Set base value:
      let val = ((risks[5 - hb_index] + risks[4 - hb_index]) / 2);

      //If highest hitbox, override base value to extend hitbox to y=1:
      if(hb_index == 5){ val = 1; }

      //Make adjustment to value based off of hitbox position:
      for (let prev_hb = 0; prev_hb < hb_index; prev_hb++){
        val -= hbhs[prev_hb];
      }

      //Update hbhs array with value(for calculating the other dependent values):
      hbhs[hb_index] = val;

      //Update fig 3 source with value to actually resize the hitbox:
      hbs[hb_index][i] = val;
    }
  }
  //Round max and min values for graph neatness:
  fig_3_max_val = Math.round(fig_3_max_val * 10) / 10;
  fig_3_min_val = Math.round(fig_3_min_val * 10) / 10;

  //Adjust graph based off of stored values:
  stats_fig_3.y_range.end   = Math.min(fig_3_max_val + fig_3_buffer, 1);
  stats_fig_3.y_range.start = Math.max(fig_3_min_val - fig_3_buffer, 0);
  stats_fig_3.x_range.start -= 0.5;
  stats_fig_3.x_range.end   += 0.5;
}
"""
  #</editor-fold>
  #<editor-fold update fig 3 function:
updateFig3 = """
function updateFig3(){
  //Store figure 3 data in order to reference it more easily:
  let fig_3_data = stats_fig_3_source.data;

  //Store fig_3_data sfga perceived risk columns in order to iterate and reference:
  const ys = [fig_3_data['ll_ys'], fig_3_data['lm_ys'], fig_3_data['lr_ys'],
              fig_3_data['rl_ys'], fig_3_data['rm_ys'], fig_3_data['rr_ys']];

  //Store iteration index:
  const index = parseInt(nround.text);

  //Update plot points:
  _fig3Iteration(ys, index);

  //Make final adjustments to graph on last iteration:
  if(index == iters_to_run){ _fig3Adjust(fig_3_data, ys); }

  //Finalize changes:
  stats_fig_3_source.change.emit();
}
"""
  #</editor-fold>
  #<editor-fold run update fig 3:
run_update_fig_3 = """
if(strategy_to_use.text == 'Fictitious_Play'){
  updateFig3();
}
"""
  #</editor-fold>

update_game_stats_figure_3 = ((_fig3CalcPointVal + _fig3Iteration + _fig3Adjust
                               + updateFig3) # functions
                              + run_update_fig_3) # actual function call
#</editor-fold>

automate_loop_iteration_main = (automate_loop_roll_kicker_action
                                + automate_loop_handle_goalie_decision
                                + automate_loop_handle_scoring
                                + automate_loop_animation
                                + automate_loop_update_decision_tracking
                                + update_game_stats_figure_1
                                + update_game_stats_figure_2
                                + update_game_stats_figure_3)

automate_loop_iteration = (automate_loop_setup
                           + automate_loop_iteration_main
                           + automate_loop_iteration_display)

b_automate_start_code = (automate_start_code_initial_gui_display
                         + automate_loop_iteration)
