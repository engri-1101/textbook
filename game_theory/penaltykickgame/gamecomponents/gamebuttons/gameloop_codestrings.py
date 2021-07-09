#This file contains the JavaScript code strings that are used for the main game
#loop.

#Any JavaScript Function defined in the strings with a name starting with the
#'_' character is a helper function.


#TODO: continue improving code efficiency.
#<editor-fold Functions:
  #<editor-fold iterationText():
iterationText = """
function iterationText(){
  //Set Game Text Lines:
  txt.data['text'] = [ ('Rounds played: ' + rounds_played),
                       ('Total score: ' + game_score), '',
                       ((goal == 1) ? 'GOAL!' : 'Blocked') ];

  txt.change.emit();
}
"""
  #</editor-fold>
  #<editor-fold rollKickerAction():
rollKickerAction = """
function rollKickerAction(){
  //Copy chances into array, then modify array to act as roll thresholds:
  let a_vals = [0].concat(chances.slice());
  a_vals.slice(1).forEach((v, i) => a_vals[i+1] += a_vals[i]);

  //Determine actions to take based off roll comparison to thresholds:
  let index = 5;
  const roll = Math.random();
  a_vals.slice(0, 6).forEach((v) => {if(roll < v){index -= 1;}});
  return [((index < 3) ? 'Left' : 'Right'), directions[(index % 3)]];
}
"""
  #</editor-fold>
  #<editor-fold fictitiousPlay():
fictitiousPlay = """
//Handle Goalie Decision
function fictitiousPlay(){
  //Set decision making values to use according to kicker_foot:
  const freqs = ((v_fl) ? freq.slice(0, 3) : freq.slice(3, 6));

  //Calculate goalie perceived risks:
  const tsr = freqs.reduce(f_sum);
  const e_fs = ((tsr != 0) ? freqs.map(x => x / tsr) : new Array(3).fill(1/3));
  const risks = new Array(3).fill(0);
  directions.forEach((v1, i) => (
    directions.forEach((v2, j) => risks[i] += e_fs[j] * side_dict[v2 + v1])
  ));

  //return goalie action and perceived risks:
  return [directions[risks.indexOf(Math.min(...risks))], ...risks];
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

  //set button visibilities:
  [true, true, v_fict, true].forEach((v, i) => b_figs[i].visible = v);

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
  //Set function values:
  const score_roll = Math.random();
  const score_chance = side_dict[kicker_kick + goalie_action];
  const rounds_played = (parseInt(nround.text) + 1);
  const round_score = ((score_roll <= score_chance) ? +1 : -1);

  //Update columns:
  const scoring_chance = dist_data['striker_score_chance'];
  const scoring_roll = dist_data['striker_score_roll'];
  scoring_chance.fill(0);
  scoring_roll.fill(0);
  scoring_chance[a_i_kfkk] = score_chance;
  scoring_roll[a_i_kfkk] = score_roll.toPrecision(6);

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
  const v_ga_e_kk = (goalie_action == kicker_kick);
  const v_miss = (goal == -1);
  const g_pos = { 'Left' : [37, 43], 'Middle' : [47, 53], 'Right' : [57, 63] };
  const b_pos = (
    ((v_miss) && (!v_ga_e_kk)) ?
    {'Left' : [30, 30], 'Middle' : [30, 70], 'Right' : [70, 70]} : g_pos
  );
  const ball_roll = Math.round(Math.random());

  ball.x = b_pos[kicker_kick][ball_roll];
  ball.y = 63;
  if(v_ga_e_kk){
    _moveGoalie((v_miss) ? ball.x : g_pos[goalie_action][[1, 0][ball_roll]]);
  }else { _moveGoalie(g_pos[goalie_action][Math.round(Math.random())]); }
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
  //Reset column then set perceived risk for rows corresponding to kicker foot:
  const risks = dist_data['goalie_perceived_risks'];

  risks.fill(0);
  [goalie_pr_L.toPrecision(6), goalie_pr_M.toPrecision(6),
   goalie_pr_R.toPrecision(6)].forEach((v, i) => risks[adjust_kfr + i] = v);
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
  //return calculated index (adjust for kicker foot and kicker kick indexes):
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
  //Get total heights of kfkk bars:
  const heights = new Array(6).fill(0);
  sections.forEach((v1) => fig_1_data[v1].forEach((v2, i) => heights[i] += v2));

  //Set y max to 1.1 * the height of the tallest kfkk bar (rounded):
  stats_fig_1.y_range.end = Math.round(Math.max(...heights) * 1.1);
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
  //Plot Values:
  fig_2_data['ys'][rounds_played] = game_score;
  fig_2_data['chance_ys'][rounds_played] = ((2 * scored_chance) - 1);
}
"""
  #</editor-fold>
  #<editor-fold _fig2Adjust():
_fig2Adjust = """
function _fig2Adjust(fig_2_data){
  //Adjust chance_ys:
  const chance_ys = fig_2_data['chance_ys'];
  chance_ys.slice(1).forEach((v, i) => chance_ys[i+1] += chance_ys[i]);

  //Get max and min of figure points:
  const ys = fig_2_data['ys'];
  let min_val = Math.min(... ys);
  let max_val = Math.max(... ys, ...chance_ys);

  //Adjust figure display:
  const buffer = Math.round((Math.abs(max_val) + Math.abs(min_val)) * 0.1);
  max_val += buffer;
  min_val -= buffer;
  stats_fig_2.y_range.end   = max_val;
  stats_fig_2.y_range.start = min_val;
  stats_fig_2.x_range.start -= 0.5;
  stats_fig_2.x_range.end   += 0.5;

  //Resize hit boxes:
  fig_2_data['height'] = new Array(iters_to_run + 1).fill(
    Math.max(Math.abs(max_val), Math.abs(min_val)) * 2
  );
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
  #<editor-fold _fig3Iteration():
_fig3Iteration = """
function _fig3Iteration(ys){
  //For each foot: get the striker action frequencies, then calculate
  //empirical frequencies. Using empirical frequencies, calculate risks for each
  //possible goalie action for that foot, then modify corresponding datapoint in
  //graph source:
  ['Left', 'Right'].forEach((f_v, f_i) => {
    const foot_freq = freq.slice((3 * f_i), (3 * (f_i + 1)));
    const foot_tsr = foot_freq.reduce(f_sum);
    const foot_chances = new Array(3).fill(1/3);
    foot_freq.forEach((v, i) => {
      if(foot_tsr != 0) { foot_chances[i] = (v / foot_tsr); }
    });
    directions.forEach((v1, i1) => directions.forEach((v2, i2) => {
      ys[(i1 + (3 * f_i))][rounds_played] += (
        foot_chances[i2] * score_probs[f_v][v2 + v1]
      );
    }));
  });
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
  let hbhs = new Array(6);
  let risks = new Array(6);
  let vals = [];
  for(let i = 0; i <= iters_to_run; i++){
    //For every iteration, for every risk value in the iteration, push it to the
    //values list for calculating min and max vals, send to risks list to get
    //iteration risks:
    ys.forEach((v, y_i) => {
      risks[y_i] = v[i];
      vals.push(v[i]);
    });

    risks.sort((a, b) => a - b); //Sort risks in ascending order to setup

    //for each entry in risks, sets a hitbox height by defining its upper edge
    //to be equal to the ((y value of the hitbox's correspoonding risk point +
    //that of the one above it) divided by 2) then subtracting the heights of
    //all lower hitboxes:
    risks.forEach((v, r_i, a) => {
      let val = ((r_i == 5) ? 1 : ((v + a[r_i + 1]) / 2));
      hbhs.slice(0, r_i).forEach((v) => val -= v);
      hbhs[r_i] = val;
      hbs[r_i][i] = val;
    });
  }

  //Adjust graph based off of stored values:
  const min_val = Math.round(Math.min(...vals) * 100) / 100;
  const max_val = Math.round(Math.max(...vals) * 100) / 100;
  const buffer = Math.round((max_val - min_val) * 100) / 1000;
  stats_fig_3.y_range.end   = Math.min(max_val + buffer, 1);
  stats_fig_3.y_range.start = Math.max(min_val - buffer, 0);
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
  const index = rounds_played - 1;
  fig_4_data['ys'][index] = scored_chance;
  fig_4_data['feet'][index] = kicker_foot;
  fig_4_data['directions'][index] = kicker_kick;
  fig_4_data['actions'][index] = goalie_action;

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
                        + _fig3Iteration + _fig3Adjust + updateFig3 + updateFig4)
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
let goalie_pr_L;
let goalie_pr_M;
let goalie_pr_R;

let goalie_action = '';

let kicker_foot = '';
let kicker_kick = '';

let goal = 0;
let game_score = 0;
let rounds_played = 0;

let scored_chance = 0;

[kicker_foot, kicker_kick] = rollKickerAction();

const v_fl = (kicker_foot == 'Left');
const side_dict = ((v_fl) ? l_dict : r_dict);
let adjust_kfr = ((!v_fl) ? 3 : 0);

if(v_fict){
  [goalie_action, goalie_pr_L,
   goalie_pr_M, goalie_pr_R] = fictitiousPlay();
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
