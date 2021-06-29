from bokeh.models import (Button, Slider, Dropdown, ColumnDataSource,
                          TableColumn, DataTable, CustomJS, TextInput)
from bokeh.models.widgets import Div
from ortools.linear_solver import pywraplp as OR
from bokeh.models.glyphs import Text
from bokeh.layouts import row, column, gridplot
from main_game_figure import game_figure_setup, Game_fig_configs
from game_stats_figure_1 import stats_figure_1_setup, Stats_fig_1_configs
from game_stats_figure_2 import stats_figure_2_setup, Stats_fig_2_configs
from game_stats_figure_3 import stats_figure_3_setup, Stats_fig_3_configs
from game_stats_figure_4 import stats_figure_4_setup, Stats_fig_4_configs

JS_FLOAT_BUFFER = "0.0000001" # THIS VARIABLE SHOULD BE TREATED AS A CONSTANT.
# JAVASCRIPT HAS SOME ISSUES WITH FLOATS, SO CHECKING FOR EQUALITY BETWEEN
# NUMBERS AND THE SUMS (OR OTHER OPERATIONS) OF OTHER NUMBERS IS NOT SAFE.
# IN ORDER TO WORK AROUND THIS ISSUE, INSTEAD OF CHECKING FOR EQUALITY, CHECK
# THAT THE VALUE IS WITHIN A RANGE OF THE EXPECTED OUTCOME.
#<editor-fold Code Strings:
    #<editor-fold b_automate Callback Code String:
b_automate_code = """
//Change visibilities of game items:
b_automate.visible = false;
ll_aim_text_input.visible = true;
lm_aim_text_input.visible = true;
lr_aim_text_input.visible = true;
rl_aim_text_input.visible = true;
rm_aim_text_input.visible = true;
rr_aim_text_input.visible = true;
iterations_slider.visible = true;
strategy_dropdown.visible = true;
automation_table.visible = true;
"""
    #</editor-fold>
    #<editor-fold automate_start_code Initial Gui Display Code String:
automate_start_code_initial_gui_display = """
//Change visibilities of game items:
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
automation_distribution_table.visible = true;
"""
    #</editor-fold>
    #<editor-fold automate_loop Code Strings:
        #<editor-fold automate_loop_setup:
create_automate_loop_constants = """
const score_probabilities = {'Right' : {'LeftLeft' : 0.55,
                                        'LeftMiddle' : 0.65,
                                        'LeftRight' : 0.93,
                                        'MiddleLeft' : 0.74,
                                        'MiddleMiddle' : 0.60,
                                        'MiddleRight' : 0.72,
                                        'RightLeft' : 0.95,
                                        'RightMiddle' : 0.73,
                                        'RightRight' : 0.70},
                             'Left' :  {'LeftLeft' : 0.67,
                                        'LeftMiddle' : 0.70,
                                        'LeftRight' : 0.96,
                                        'MiddleLeft' : 0.74,
                                        'MiddleMiddle' : 0.60,
                                        'MiddleRight' : 0.72,
                                        'RightLeft' : 0.87,
                                        'RightMiddle' : 0.65,
                                        'RightRight' : 0.61}};
const chances = ChancesColumnDataSource.data['chances'];
const dist_data = DistributionColumnDataSource.data;
const freq = dist_data['freq'];
const iters_to_run = parseInt(iterations_to_run.text);
"""

create_automate_loop_state_lets = """
let danger_goalie_left = 0;
let danger_goalie_middle = 0;
let danger_goalie_right = 0;

let goalie_action = "None";

let kicker_foot = 'none';
let kicker_kick = 'none';

let goal = 1;
let game_score = 0;
let rounds_played = 0;

let scored_chance = 0;
"""

automate_loop_setup = (create_automate_loop_constants
                       + create_automate_loop_state_lets)
        #</editor-fold>
        #<editor-fold automate_loop_iteration_display
automate_loop_iteration_display = """
const game_text = txt.data['text'];

game_text[0] = 'Rounds played: ' + rounds_played;

if (goal == 1){
    game_text[3] = 'GOAL!';
}
else{
    game_text[3] = 'Blocked';
}

game_text[1] = 'Total score: ' + game_score;

txt.change.emit();
"""
#</editor-fold>
        #<editor-fold automate_loop_roll_kicker_action
automate_loop_roll_kicker_action = """
function rollKickerAction(){
    let action_roll = Math.random();

    const LL_chance = chances[0];
    const LM_chance = LL_chance + chances[1];
    const LR_chance = LM_chance + chances[2];
    const RL_chance = LR_chance + chances[3];
    const RM_chance = RL_chance + chances[4];

    const action_LL_chance = chances[0];
    const action_LM_chance = action_LL_chance + chances[1];
    const action_LR_chance = action_LM_chance + chances[2];
    const action_RL_chance = action_LR_chance + chances[3];
    const action_RM_chance = action_RL_chance + chances[4];
    let foot;
    let kick;

    if(action_roll <= action_LL_chance){
        foot = 'Left';
        kick = 'Left';
    }
    else if(action_roll <= action_LM_chance){
        foot = 'Left';
        kick = 'Middle';
    }
    else if(action_roll <= action_LR_chance){
        foot = 'Left';
        kick = 'Right';
    }
    else if(action_roll <= action_RL_chance){
        foot = 'Right';
        kick = 'Left';
    }
    else if(action_roll <= action_RM_chance){
        foot = 'Right';
        kick = 'Middle';
    }
    else{
        foot = 'Right';
        kick = 'Right';
    }
    return [foot, kick]
}
[kicker_foot, kicker_kick] = rollKickerAction();
"""
#</editor-fold>
        #<editor-fold automate_loop_handle_goalie_decision
            #<editor-fold run_fictitious_play
run_fictitious_play = """
//Handle Goalie Decision
function runFictitiousPlay(){

    let tsr; //total_sample_rolls
    let cl; //chance left
    let cm; //chance middle
    let cr; //chance right
    let action; //action for goalie to take
    let sfprobsdict; //striker foot probabilities dictionary
    let dgl; //danger_goalie_left
    let dgm; //danger_goalie_middle
    let dgr; //danger_goalie_right
    let action_roll; //random roll

    if(kicker_foot == 'Left'){
        tsr = freq[0] + freq[1] + freq[2];
        sfprobsdict = score_probabilities['Left'];
        if(tsr == 0){
            cl = 1/3;
            cm = 1/3;
            cr = 1/3;
        }
        else{
            cl = freq[0] / tsr;
            cm = freq[1] / tsr;
            cr = freq[2] / tsr;
        }
    }
    else{
        tsr = freq[3] + freq[4] + freq[5];
        sfprobsdict = score_probabilities['Right'];
        if(tsr == 0){
            cl = 1/3;
            cm = 1/3;
            cr = 1/3;
        }
        else{
            cl = freq[3] / tsr;
            cm = freq[4] / tsr;
            cr = freq[5] / tsr;
        }
    }

    dgl = (cl * sfprobsdict['LeftLeft']
           + cm*sfprobsdict['MiddleLeft']
           + cr*sfprobsdict['RightLeft']);
    dgm = (cl * sfprobsdict['LeftMiddle']
           + cm*sfprobsdict['MiddleMiddle']
           + cr*sfprobsdict['RightMiddle']);
    dgr = (cl * sfprobsdict['LeftRight']
           + cm*sfprobsdict['MiddleRight']
           + cr*sfprobsdict['RightRight']);


    if(dgl < dgm){
        if(dgl < dgr){
            action = "Left";
        }
        else if(dgl == dgr){
            action_roll = Math.random();
            if(action_roll <= 0.5){
                action = "Left";
            }
            else{
                action = "Right";
            }
        }
        else{
            action = "Right";
        }
    }
    else if (dgl == dgm){
        action_roll = Math.random();
        if(action_roll <= 0.5){
            action = "Left";
        }
        else{
            action = "Middle";
        }
    }
    else{
        if(dgm < dgr){
            action = "Middle";
        }
        else if(dgm == dgr){
            action_roll = Math.random();
            if(action_roll <= 0.5){
                action = "Middle";
            }
            else{
                action = "Right";
            }
        }
        else{
            action = "Right";
        }
    }
    return [action, dgl, dgm, dgr]
}
[goalie_action, danger_goalie_left,
 danger_goalie_middle, danger_goalie_right] = runFictitiousPlay();
"""
#</editor-fold>
            #<editor-fold run_optimal_mixed_strategy
run_optimal_mixed_strategy = """
function runOptimalMixedStrategy(){
    let action_roll = Math.random();
    let action;
    if(kicker_foot == 'Left'){
        if(action_roll <= 0.8){
            action = "Middle"
        }
        else{
            action = "Left"
        }
    }
    else{
        if(action_roll <= 0.7419){
            action = "Middle";
        }
        else{
            action = "Right";
        }
    }
    return action;
}

goalie_action = runOptimalMixedStrategy();
"""
#</editor-fold>
            #<editor-fold run_random_choices
run_random_choices = """
function runRandom(){
    let action_roll = Math.random();
    let action;
    if(action_roll <= 1/3){
        action = "Left";
    }
    else if(action_roll <= 2/3){
        action = "Middle";
    }
    else{
        action = "Right";
    }
    return action;
}

goalie_action = runRandom();
"""
            #</editor-fold>
            #<editor-fold run_goalie_cheats
run_goalie_cheats = """
function runGoalieCheats(){
    const counter_chances_l = goalie_counter_source.data['chances_l'];
    const counter_chances_r = goalie_counter_source.data['chances_r'];
    let action;
    if(kicker_foot == 'Left'){
        if(counter_chances_l[0] == 1){
            action = "Left";
        }
        else if(counter_chances_l[1] == 1){
            action = "Middle";
        }
        else{
            action = "Right";
        }
    }
    else{
        if(counter_chances_r[0] == 1){
            action = "Left";
        }
        else if(counter_chances_r[1] == 1){
            action = "Middle";
        }
        else{
            action = "Right";
        }
    }
    return action;
}

goalie_action = runGoalieCheats();
"""
            #</editor-fold>
automate_loop_handle_goalie_decision = """
if(strategy_to_use.text == "Fictitious_Play"){
    """ + run_fictitious_play + """
}
else if(strategy_to_use.text == "Mixed_Strategy"){
    """ + run_optimal_mixed_strategy + """
}
else if(strategy_to_use.text == "Random"){
    """ + run_random_choices + """
}
else if(strategy_to_use.text == "Goalie_Cheats"){
    """ + run_goalie_cheats + """
}
"""
        #</editor-fold>
        #<editor-fold automate_loop_handle_scoring
automate_loop_handle_scoring = """
function scoring(){
    const scoring_chance = dist_data['striker_score_chance'];
    const scoring_roll = dist_data['striker_score_roll'];

    let score_roll = Math.random();
    let score_chance = score_probabilities[kicker_foot][kicker_kick+goalie_action];
    let index_to_update = 0;
    let rounds_played = (parseInt(nround.text) + 1);
    let round_score;

    game_stats_figure_4_source.data['ys'][rounds_played] = score_chance;
    game_stats_figure_4_source.data['feet'][rounds_played] = kicker_foot;
    game_stats_figure_4_source.data['directions'][rounds_played] = kicker_kick;
    game_stats_figure_4_source.data['actions'][rounds_played] = goalie_action;
    game_stats_figure_4_source.change.emit()

    if(score_roll <= score_chance){
        round_score = 1;
    }
    else{
        round_score = -1;
    }
    //Display Score Chance:

    for(var i = 0; i <= 5; i++){
        scoring_chance[i] = 0;
        scoring_roll[i] = 0;
    }

    if(kicker_foot == 'Right'){
        index_to_update += 3;
    }
    if(kicker_kick == 'Middle'){
        index_to_update += 1;
    }
    else if(kicker_kick == 'Right'){
        index_to_update += 2;
    }

    scoring_chance[index_to_update] = score_chance;
    scoring_roll[index_to_update] = score_roll.toString().substring(0, 8);

    // Update text

    if(rounds_played >= iters_to_run){
        b_auto_next.visible = false;
        game_figure.visible = false;
        automation_distribution_table.visible = false;
        game_stats_figure_4_source.data['xs'].shift();
        game_stats_figure_4_source.data['ys'].shift();
        game_stats_figure_4_source.data['feet'].shift();
        game_stats_figure_4_source.data['directions'].shift();
        game_stats_figure_4_source.data['actions'].shift();
        game_stats_figure_4_source.data['highlight_alphas'].shift();
        game_stats_figure_4_source.data['avgs_placeholder'].shift();
        game_stats_figure_4_source.change.emit();
        game_stats_figure_4.x_range.start -= 0.5;
        game_stats_figure_4.x_range.end += 0.5;
        if(strategy_to_use.text == "Fictitious_Play"){
            game_stats_figure_1.visible = true;
            game_stats_figure_2.visible = false;
            game_stats_figure_3.visible = false;
            game_stats_figure_4.visible = false;
            b_fig_1.visible = true;
            b_fig_2.visible = true;
            b_fig_3.visible = true;
            b_fig_4.visible = true;
        }
        else{
            game_stats_figure_1.visible = true;
            game_stats_figure_2.visible = false;
            game_stats_figure_3.visible = false;
            game_stats_figure_4.visible = false;
            b_fig_1.visible = true;
            b_fig_2.visible = true;
            b_fig_3.visible = false;
            b_fig_4.visible = true;
        }
    }
    nround.text = rounds_played.toString();

    let current_game_score = parseInt(score.text) + round_score;
    score.text = current_game_score.toString();

    return [round_score, current_game_score, rounds_played, score_chance];
}
[goal, game_score, rounds_played, scored_chance] = scoring();
"""
#</editor-fold>
        #<editor-fold automate_loop_animation
automate_loop_animation = """
function doAnimation(){
    let animation_roll = Math.random();
    let animation_slot = 0;

    const animation_positions = {'Left' : [37, 43],
                                 'Middle' : [47,53],
                                 'Right' : [57, 63]};

    if(animation_roll <= 0.5){
        animation_slot = 1;
    }

    ball.x = animation_positions[kicker_kick][animation_slot];
    ball.y = 63;

    if(goal == -1){
        if(goalie_action == kicker_kick){
            goalie_head.x = ball.x;
            goalie_body.x = ball.x;
        }
        else{
            if(kicker_kick == "Right"){
                ball.x = 70;
            }
            else if(kicker_kick == "Left"){
                ball.x = 30;
            }
            else{
                ball.x = [30,70][animation_slot];
            }
        }
    }
    else{
        if(goalie_action == kicker_kick){
            if(animation_slot == 1){
                goalie_head.x = animation_positions[goalie_action][0];
                goalie_body.x = animation_positions[goalie_action][0];
            }
            else{
                goalie_head.x = animation_positions[goalie_action][1];
                goalie_body.x = animation_positions[goalie_action][1];
            }
        }
        else{
            animation_slot = 1;
                if(animation_roll <= 0.5){
            }
            else{
                animation_slot = 0;
            }
            goalie_head.x = animation_positions[goalie_action][animation_slot];
            goalie_body.x = animation_positions[goalie_action][animation_slot];
        }
    }
}
doAnimation();
"""
#</editor-fold>
        #<editor-fold automate_loop_update_fictitious_decision_tracking
automate_loop_update_fictitious_decision_tracking = """
function goalieFictitiousDecisionTracking(){
    const perceived_risks = dist_data['goalie_perceived_risks'];
    let selected_freq_index = 0;
    if(kicker_foot == 'Right'){
        selected_freq_index += 3;
    }
    if(kicker_kick == 'Middle'){
        selected_freq_index += 1;
    }
    else if(kicker_kick == 'Right'){
        selected_freq_index += 2;
    }
    freq[selected_freq_index] += 1;

    let selected_decisions_index = 0;
    if(kicker_foot == 'Right'){
        selected_decisions_index += 3;
    }
    if(goalie_action == 'Middle'){
        selected_decisions_index += 1;
    }
    else if(goalie_action == 'Right'){
        selected_decisions_index += 2;
    }
    dist_data['decisions'][selected_decisions_index] += 1;

    if(strategy_to_use.text == "Fictitious_Play"){
        let selected_pr_index = 0;
        if(kicker_foot == 'Right'){
            selected_pr_index += 3;
        }
        for(var i=0; i<=5; i++){
            perceived_risks[i] = 0;
        }
        perceived_risks[selected_pr_index] = danger_goalie_left.toString().substring(0, 8);
        perceived_risks[selected_pr_index + 1] = danger_goalie_middle.toString().substring(0, 8);
        perceived_risks[selected_pr_index + 2] = danger_goalie_right.toString().substring(0, 8);
    }
    DistributionColumnDataSource.change.emit();
}

goalieFictitiousDecisionTracking();
"""
#</editor-fold>
        #<editor-fold update_game_stats_figure_1
update_game_stats_figure_1 = """

function updateFig1(){
    const fig_1_data = game_stats_figure_1_source.data;
    let selected_bar = 0;

    if (kicker_foot == 'Right'){
        selected_bar += 3;
    }

    if(kicker_kick == 'Middle'){
        selected_bar += 1;
    }
    else if(kicker_kick == 'Right'){
        selected_bar += 2;
    }

    if(goal == 1){
        fig_1_data['scored_y'][selected_bar] += 1;
    }
    else{
        if(goalie_action == "Left"){
            fig_1_data['blockedl_y'][selected_bar] += 1;
        }
        else if(goalie_action == "Middle"){
            fig_1_data['blockedm_y'][selected_bar] += 1;
        }
        else{
            fig_1_data['blockedr_y'][selected_bar] += 1;
        }
    }
    game_stats_figure_1_source.change.emit();

    if(parseInt(nround.text) >= iters_to_run){
        let grid_max = 0;
        for(let i=0; i<=5; i++){
            const possible_max = Math.round(((fig_1_data['scored_y'][i]
                                              + fig_1_data['blockedl_y'][i]
                                              + fig_1_data['blockedm_y'][i]
                                              + fig_1_data['blockedr_y'][i])
                                             * 5/4));
            if(grid_max < possible_max){
                grid_max = possible_max;
            }
        }
        game_stats_figure_1.y_range.end = grid_max;
    }
}
updateFig1();
"""
#</editor-fold>
        #<editor-fold update_game_stats_figure_2
update_game_stats_figure_2 = """
function updateFig2(){
    const fig_2_data = game_stats_figure_2_source.data;

    let nround_val = parseInt(nround.text);

    fig_2_data['ys'][nround_val] = parseInt(score.text);
    fig_2_data['chance_ys'][nround_val] = fig_2_data['chance_ys'][nround_val - 1] + (2 * scored_chance - 1);
    game_stats_figure_2_source.change.emit();

    if(nround_val >= iters_to_run){
        //Resize Graph and Hitboxes:
        let fig_2_min_val = 0;
        let fig_2_max_val = 0;

        for(let i = 0; i <= iters_to_run; i++){
            if(fig_2_min_val > fig_2_data['ys'][i]){
                fig_2_min_val = fig_2_data['ys'][i];
            }
            if(fig_2_max_val < fig_2_data['ys'][i]){
                fig_2_max_val = fig_2_data['ys'][i];
            }
        }
        //Resize Hitboxes:
        let heights = [];
        let buffer = Math.round((Math.abs(fig_2_max_val)
                                 + Math.abs(fig_2_min_val))
                                * 1/8) + 1;
        if(Math.abs(fig_2_max_val) > Math.abs(fig_2_min_val)){
            for(let i = 0; i <= iters_to_run; i++){
                heights.push(Math.abs((fig_2_max_val + buffer) * 2));
            }
        }
        else{
            for(let i = 0; i <= iters_to_run; i++){
                heights.push(Math.abs((fig_2_min_val - buffer) * 2));
            }
        }
        fig_2_data['heights'] = heights;

        //Resize Graph:
        game_stats_figure_2.y_range.end = fig_2_max_val + buffer;
        game_stats_figure_2.y_range.start = fig_2_min_val - buffer;
        game_stats_figure_2.x_range.start -= 0.5;
        game_stats_figure_2.x_range.end += 0.5;

        game_stats_figure_2_source.change.emit();
    }
}
updateFig2();
"""
#</editor-fold>
        #<editor-fold update_game_stats_figure_3
update_game_stats_figure_3 = """
function updateFig3(){

    let fig_3_data = game_stats_figure_3_source.data;
    let index = parseInt(nround.text);

    let freq_ll = freq[0];
    let freq_lm = freq[1];
    let freq_lr = freq[2];
    let freq_rl = freq[3];
    let freq_rm = freq[4];
    let freq_rr = freq[5];
    let chance_l_total = freq_ll + freq_lm + freq_lr;
    let chance_r_total = freq_rl + freq_rm + freq_rr;

    let chance_ll;
    let chance_lm;
    let chance_lr;
    let chance_rl;
    let chance_rm;
    let chance_rr;
    if(chance_l_total != 0){
        chance_ll = freq_ll / chance_l_total;
        chance_lm = freq_lm / chance_l_total;
        chance_lr = freq_lr / chance_l_total;
    }
    else{
        chance_ll = 1/3;
        chance_lm = 1/3;
        chance_lr = 1/3;
    }

    if(chance_r_total != 0){
        chance_rl = freq_rl / chance_r_total;
        chance_rm = freq_rm / chance_r_total;
        chance_rr = freq_rr / chance_r_total;
    }
    else{
        chance_rl = 1/3;
        chance_rm = 1/3;
        chance_rr = 1/3;
    }

    fig_3_data['ll_ys'][index] = ((chance_ll
                                   * score_probabilities['Left']['LeftLeft'])
                                  + (chance_lm
                                     * score_probabilities['Left']['MiddleLeft'])
                                  + (chance_lr
                                     * score_probabilities['Left']['RightLeft']));
    fig_3_data['lm_ys'][index] = ((chance_ll
                                   * score_probabilities['Left']['LeftMiddle'])
                                  + (chance_lm
                                     * score_probabilities['Left']['MiddleMiddle'])
                                  + (chance_lr
                                     * score_probabilities['Left']['RightMiddle']));
    fig_3_data['lr_ys'][index] = ((chance_ll
                                   * score_probabilities['Left']['LeftRight'])
                                  + (chance_lm
                                     * score_probabilities['Left']['MiddleRight'])
                                  + (chance_lr
                                     * score_probabilities['Left']['RightRight']));
    fig_3_data['rl_ys'][index] = ((chance_rl
                                   * score_probabilities['Right']['LeftLeft'])
                                  + (chance_rm
                                     * score_probabilities['Right']['MiddleLeft'])
                                  + (chance_rr
                                     * score_probabilities['Right']['RightLeft']));
    fig_3_data['rm_ys'][index] = ((chance_rl
                                   * score_probabilities['Right']['LeftMiddle'])
                                  + (chance_rm
                                     * score_probabilities['Right']['MiddleMiddle'])
                                  + (chance_rr
                                     * score_probabilities['Right']['RightMiddle']));
    fig_3_data['rr_ys'][index] = ((chance_rl
                                   * score_probabilities['Right']['LeftRight'])
                                  + (chance_rm
                                     * score_probabilities['Right']['MiddleRight'])
                                  + (chance_rr
                                     * score_probabilities['Right']['RightRight']));
    if(index == iters_to_run){
        for(let i = 0; i <= iters_to_run; i++){
            let fig_3_perceived_risks = [fig_3_data['ll_ys'][i],
                                         fig_3_data['lm_ys'][i],
                                         fig_3_data['lr_ys'][i],
                                         fig_3_data['rl_ys'][i],
                                         fig_3_data['rm_ys'][i],
                                         fig_3_data['rr_ys'][i]];

            let sorted_perceived_risks = fig_3_perceived_risks.sort((a, b) => b - a);
            let hbh1 = ((sorted_perceived_risks[5]
                         + sorted_perceived_risks[4]) / 2);
            let hbh2 = ((sorted_perceived_risks[4]
                         + sorted_perceived_risks[3]) / 2) - hbh1;
            let hbh3 = ((sorted_perceived_risks[3]
                         + sorted_perceived_risks[2]) / 2) - hbh2 - hbh1;
            let hbh4 = (((sorted_perceived_risks[2]
                          + sorted_perceived_risks[1]) / 2)
                        - hbh3 - hbh2 - hbh1);
            let hbh5 = (((sorted_perceived_risks[1]
                          + sorted_perceived_risks[0]) / 2)
                        - hbh4 - hbh3 - hbh2 - hbh1);
            let hbh6 = 1 - hbh1 - hbh2 - hbh3 - hbh4 - hbh5;
            fig_3_data['hb1'][i] = hbh1;
            fig_3_data['hb2'][i] = hbh2;
            fig_3_data['hb3'][i] = hbh3;
            fig_3_data['hb4'][i] = hbh4;
            fig_3_data['hb5'][i] = hbh5;
            fig_3_data['hb6'][i] = hbh6;
        }

        let fig_3_min_val = 1;
        let fig_3_max_val = 0;
        for (var i = 0; i <= iters_to_run; i++){
            if(fig_3_data['ll_ys'][i] > fig_3_max_val){
                fig_3_max_val = fig_3_data['ll_ys'][i];
            }
            if(fig_3_data['lm_ys'][i] > fig_3_max_val){
                fig_3_max_val = fig_3_data['lm_ys'][i];
            }
            if(fig_3_data['lr_ys'][i] > fig_3_max_val){
                fig_3_max_val = fig_3_data['lr_ys'][i];
            }
            if(fig_3_data['rl_ys'][i] > fig_3_max_val){
                fig_3_max_val = fig_3_data['rl_ys'][i];
            }
            if(fig_3_data['rm_ys'][i] > fig_3_max_val){
                fig_3_max_val = fig_3_data['rm_ys'][i];
            }
            if(fig_3_data['rr_ys'][i] > fig_3_max_val){
                fig_3_max_val = fig_3_data['rr_ys'][i];
            }

            if(fig_3_data['ll_ys'][i] < fig_3_min_val){
                fig_3_min_val = fig_3_data['ll_ys'][i];
            }
            if(fig_3_data['lm_ys'][i] < fig_3_min_val){
                fig_3_min_val = fig_3_data['lm_ys'][i];
            }
            if(fig_3_data['lr_ys'][i] < fig_3_min_val){
                fig_3_min_val = fig_3_data['lr_ys'][i];
            }
            if(fig_3_data['rl_ys'][i] < fig_3_min_val){
                fig_3_min_val = fig_3_data['rl_ys'][i];
            }
            if(fig_3_data['rm_ys'][i] < fig_3_min_val){
                fig_3_min_val = fig_3_data['rm_ys'][i];
            }
            if(fig_3_data['rr_ys'][i] < fig_3_min_val){
                fig_3_min_val = fig_3_data['rr_ys'][i];
            }
        }

        fig_3_max_val = Math.round(fig_3_max_val * 10) / 10;
        fig_3_min_val = Math.round(fig_3_min_val * 10) / 10;
        const fig_3_buffer = 0.1;
        game_stats_figure_3.y_range.end = Math.min(fig_3_max_val + fig_3_buffer,
                                                   1);
        game_stats_figure_3.y_range.start = fig_3_min_val - fig_3_buffer;
        game_stats_figure_3.x_range.start -= 0.5;
        game_stats_figure_3.x_range.end += 0.5;
    }

    game_stats_figure_3_source.change.emit();
}

if(strategy_to_use.text == "Fictitious_Play"){
    updateFig3();
}
"""
#</editor-fold>

automate_loop_iteration_main = (automate_loop_roll_kicker_action
                                + automate_loop_handle_goalie_decision
                                + automate_loop_handle_scoring
                                + automate_loop_animation
                                + automate_loop_update_fictitious_decision_tracking
                                + update_game_stats_figure_1
                                + update_game_stats_figure_2
                                + update_game_stats_figure_3)

automate_loop_iteration = (automate_loop_setup
                           + automate_loop_iteration_main
                           + automate_loop_iteration_display)

b_automate_start_code = (automate_start_code_initial_gui_display
                         + automate_loop_iteration)
    #</editor-fold>
    #<editor-fold iterations_slider_callback Code String:
iterations_slider_code = """

//Read iterations, and update iterations_to_run:
const iterations = cb_obj.value;
iterations_to_run.text = iterations.toString();

//Set the max of the y axis for game_stats_figure_1 to be the
//amount of iterations (It is impossible to have bars higher than that value):
game_stats_figure_1.y_range.end = iterations;

//Set the max and min of the y axis for game_stats_figure_2 to be
//+/- the amount of iterations as it is impossible to have a score higher or
//lower than that:
game_stats_figure_2.y_range.start = -iterations;
game_stats_figure_2.y_range.end = iterations;

//Sets the max of the x axis for game_stats_figure_2 and game_stats_figure_3 to
//be the amount of iterations.
game_stats_figure_2.x_range.end = iterations;
game_stats_figure_3.x_range.end = iterations;
game_stats_figure_4.x_range.end = iterations;
//Initiate arrays to update lengths and values of data in sources:
const array_length = iterations + 1;
let xs_2 = [];
let xs_3 = [];
let xs_4 = [];

let ys = new Array(array_length).fill(0);
let chance_ys = new Array(array_length).fill(0);
let ll_ys = new Array(array_length).fill(0);
let lm_ys = new Array(array_length).fill(0);
let lr_ys = new Array(array_length).fill(0);
let rl_ys = new Array(array_length).fill(0);
let rm_ys = new Array(array_length).fill(0);
let rr_ys = new Array(array_length).fill(0);
let hb1_ys = new Array(array_length).fill(0);
let hb2_ys = new Array(array_length).fill(0);
let hb3_ys = new Array(array_length).fill(0);
let hb4_ys = new Array(array_length).fill(0);
let hb5_ys = new Array(array_length).fill(0);
let hb6_ys = new Array(array_length).fill(0);
let heights = new Array(array_length).fill(iterations * 2);
let fig2_highlight_alphas = new Array(array_length).fill(0);
let fig3_highlight_alphas = new Array(array_length).fill(0);
let fig3_alphas_zeroes = new Array(array_length).fill(0);
let ys_4 = new Array(array_length).fill(0);
let feet_4 = new Array(array_length).fill(null);
let directions_4 = new Array(array_length).fill(null);
let actions_4 = new Array(array_length).fill(null);
let highlight_alphas_4 = new Array(array_length).fill(0);
let avgs_placeholder = new Array(array_length).fill(0);

//Update previously created arrays with their correct values:
for (let i = 0; i <= iterations; i++){
    xs_2.push(i);
    xs_3.push(i);
    xs_4.push(i);
}

//Write the correct initial values for the arrays that need it:
ll_ys[0] = 1/3 * (0.67 + 0.74 + 0.87);
lm_ys[0] = 1/3 * (0.70 + 0.60 + 0.65);
lr_ys[0] = 1/3 * (0.96 + 0.72 + 0.61);
rl_ys[0] = 1/3 * (0.55 + 0.74 + 0.95);
rm_ys[0] = 1/3 * (0.65 + 0.60 + 0.73);
rr_ys[0] = 1/3 * (0.93 + 0.72 + 0.70);

//Update game_stats_figure_2_source.data with its new arrays:
const fig_2_data = game_stats_figure_2_source.data;
fig_2_data['xs'] = xs_2;
fig_2_data['ys'] = ys;
fig_2_data['chance_ys'] = chance_ys;
fig_2_data['heights'] = heights;
fig_2_data['highlight_alphas'] = fig2_highlight_alphas;
game_stats_figure_2_source.change.emit();

//Update game_stats_figure_3_source.data with its new arrays:
const fig_3_data = game_stats_figure_3_source.data;
fig_3_data['xs'] = xs_3;
fig_3_data['ll_ys'] = ll_ys;
fig_3_data['lm_ys'] = lm_ys;
fig_3_data['lr_ys'] = lr_ys;
fig_3_data['rl_ys'] = rl_ys;
fig_3_data['rm_ys'] = rm_ys;
fig_3_data['rr_ys'] = rr_ys;
fig_3_data['highlight_alphas'] = fig3_highlight_alphas;
fig_3_data['alphas_zeroes'] = fig3_alphas_zeroes;
fig_3_data['hb1'] = hb1_ys;
fig_3_data['hb2'] = hb2_ys;
fig_3_data['hb3'] = hb3_ys;
fig_3_data['hb4'] = hb4_ys;
fig_3_data['hb5'] = hb5_ys;
fig_3_data['hb6'] = hb6_ys;
game_stats_figure_3_source.change.emit();

game_stats_figure_4_source.data['xs'] = xs_4;
game_stats_figure_4_source.data['ys'] = ys_4;
game_stats_figure_4_source.data['feet'] = feet_4;
game_stats_figure_4_source.data['directions'] = directions_4;
game_stats_figure_4_source.data['actions'] = actions_4;
game_stats_figure_4_source.data['highlight_alphas'] = highlight_alphas_4;
game_stats_figure_4_source.data['avgs_placeholder'] = avgs_placeholder;
game_stats_figure_4_source.change.emit();
"""
    #</editor-fold>
    #<editor-fold strategy_dropdown_callback Code String:
strategy_dropdown_code = """
//Set the label of the dropdown (the text displayed) to the selected item:
strategy_dropdown.label = this.item;

//Set the text of the strategy_to_use div to the selected item:
strategy_to_use.text = this.item;

//Sets the aim sliders to be visible:
ll_aim_text_input.visible = true;
lm_aim_text_input.visible = true;
lr_aim_text_input.visible = true;
rl_aim_text_input.visible = true;
rm_aim_text_input.visible = true;
rr_aim_text_input.visible = true;

//Sets the automation_table to be visible:
automation_table.visible = true;

//Toggles button visibilities based off selected item:
if(this.item != "Goalie_Cheats"){
    b_make_counter.visible = false;
    counter_made.text = "1";
    cpu_selected.text = "1";
}
else{
    counter_made.text = "0";
    cpu_selected.text = "1";
}
"""
    #</editor-fold>
    #<editor-fold b_make_counter callback Code String:
b_make_counter_click_code = """
const chances = automation_table_source.data['chances'];

//Hides the automation_table as it is un-needed:
automation_table.visible = false;

ll_aim_text_input.visible = false;
lm_aim_text_input.visible = false;
lr_aim_text_input.visible = false;
rl_aim_text_input.visible = false;
rm_aim_text_input.visible = false;
rr_aim_text_input.visible = false;

//Take chance values:
const ll_chance = chances[0];
const lm_chance = chances[1];
const lr_chance = chances[2];
const rl_chance = chances[3];
const rm_chance = chances[4];
const rr_chance = chances[5];

//Left side decision making:
const goalie_ll = ll_chance * 0.67 + lm_chance * 0.74 + lr_chance * 0.87;
const goalie_lm = ll_chance * 0.70 + lm_chance * 0.60 + lr_chance * 0.65;
const goalie_lr = ll_chance * 0.96 + lm_chance * 0.72 + lr_chance * 0.61;
let goalie_ll_coeff = 1;
let goalie_lm_coeff = 0;
let goalie_lr_coeff = 0;
let goalie_l_obj = goalie_ll * goalie_ll_coeff;

//Get optimal pure counter strategy. This works because the average risk for
//each position is constant (The chance of scoring given a striker shot
//direction and goalie decision is constant, and the striker's chance of aiming
//in each way is also constant, so the average risk for each position cannot
//change), so the optimal mixed strategy for the goalie is just to constantly
//go to the location with the lowest risk (LP would be the minimum of each of
//the decision variables multiplied by their risk, subject to the decision
//variables adding up to 1, which would just end up with the lowest risk
//position being chosen).

if(goalie_ll > goalie_lm){
    goalie_ll_coeff = 0;
    goalie_lm_coeff = 1;
    goalie_l_obj = goalie_lm * goalie_lm_coeff;

    if(goalie_lm > goalie_lr){
        goalie_lm_coeff = 0;
        goalie_lr_coeff = 1;
        goalie_l_obj = goalie_lr * goalie_lr_coeff;
    }
}
else if(goalie_ll > goalie_lr){
    goalie_ll_coeff = 0;
    goalie_lr_coeff = 1;
    goalie_l_obj = goalie_lr * goalie_lr_coeff;
}

//else do nothing.

//Right side decision making:
const goalie_rl = rl_chance * 0.55 + rm_chance * 0.74 + rr_chance * 0.95;
const goalie_rm = rl_chance * 0.65 + rm_chance * 0.60 + rr_chance * 0.73;
const goalie_rr = rl_chance * 0.93 + rm_chance * 0.72 + rr_chance * 0.70;
let goalie_rl_coeff = 1;
let goalie_rm_coeff = 0;
let goalie_rr_coeff = 0;
let goalie_r_obj = goalie_rl * goalie_rl_coeff;

if(goalie_rl > goalie_rm){
    goalie_rl_coeff = 0;
    goalie_rm_coeff = 1;
    goalie_r_obj = goalie_rm * goalie_rm_coeff;

    if(goalie_rm > goalie_rr){
        goalie_rm_coeff = 0;
        goalie_rr_coeff = 1;
        goalie_r_obj = goalie_rr * goalie_rr_coeff;
    }
}
else if(goalie_rl > goalie_rr){
    goalie_rl_coeff = 0;
    goalie_rr_coeff = 1;
    goalie_r_obj = goalie_rr * goalie_rr_coeff;
}
//else do nothing.

//Set Goalie chances:
goalie_counter_source.data['chances_l'][0] = goalie_ll_coeff;
goalie_counter_source.data['chances_l'][1] = goalie_lm_coeff;
goalie_counter_source.data['chances_l'][2] = goalie_lr_coeff;
goalie_counter_source.data['chances_r'][0] = goalie_rl_coeff;
goalie_counter_source.data['chances_r'][1] = goalie_rm_coeff;
goalie_counter_source.data['chances_r'][2] = goalie_rr_coeff;

goalie_counter_source.change.emit();

b_make_counter.visible = false;

counter_made.text = "1";
"""
    #</editor-fold>
    #<editor-fold aim_inputs_callback Code String:
aim_inputs_callback_code = """
//Get the chances array to modify:
const chances = table_source.data['chances'];

//Hide start button:
b_start_automate.visible = false;
chances_valid.text = "0";

//Check if inputs are valid:
let is_valid;

let ll_val = parseFloat(ll_aim_text_input.value);
let lm_val = parseFloat(lm_aim_text_input.value);
let lr_val = parseFloat(lr_aim_text_input.value);
let rl_val = parseFloat(rl_aim_text_input.value);
let rm_val = parseFloat(rm_aim_text_input.value);
let rr_val = parseFloat(rr_aim_text_input.value);

if(ll_val > 1){ is_valid = false; }
if(lm_val > 1){ is_valid = false; }
if(lr_val > 1){ is_valid = false; }
if(rl_val > 1){ is_valid = false; }
if(rm_val > 1){ is_valid = false; }
if(rr_val > 1){ is_valid = false; }

if(ll_val < 0){ is_valid = false; }
if(lm_val < 0){ is_valid = false; }
if(lr_val < 0){ is_valid = false; }
if(rl_val < 0){ is_valid = false; }
if(rm_val < 0){ is_valid = false; }
if(rr_val < 0){ is_valid = false; }

const total = (ll_val + lm_val + lr_val + rl_val + rm_val + rr_val)
if(total >= 1 - """ + JS_FLOAT_BUFFER + """
    && total <= 1 + """ + JS_FLOAT_BUFFER + """){
    is_valid = true;
}
else{
    is_valid = false;
}

chances[0] = ll_val;
chances[1] = lm_val;
chances[2] = lr_val;
chances[3] = rl_val;
chances[4] = rm_val;
chances[5] = rr_val;
table_source.change.emit();

if(is_valid){
    chances_valid.text = "1";
}
else{
    chances_valid.text = "0";
}
return;
"""
    #</editor-fold>
    #<editor-fold b_fig_1 callback Code String:
b_fig_1_click_code = """
b_fig_1.disabled = true;
b_fig_2.disabled = false;
b_fig_3.disabled = false;
b_fig_4.disabled = false;
game_stats_figure_1.visible = true;
game_stats_figure_2.visible = false;
game_stats_figure_3.visible = false;
game_stats_figure_4.visible = false;
"""
    #</editor-fold>
    #<editor-fold b_fig_2 callback Code String:
b_fig_2_click_code = """
b_fig_1.disabled = false;
b_fig_2.disabled = true;
b_fig_3.disabled = false;
b_fig_4.disabled = false;
game_stats_figure_1.visible = false;
game_stats_figure_2.visible = true;
game_stats_figure_3.visible = false;
game_stats_figure_4.visible = false;
"""
    #</editor-fold>
    #<editor-fold b_fig_3 callback Code String:
b_fig_3_click_code = """
b_fig_1.disabled = false;
b_fig_2.disabled = false;
b_fig_3.disabled = true;
b_fig_4.disabled = false;
game_stats_figure_1.visible = false;
game_stats_figure_2.visible = false;
game_stats_figure_3.visible = true;
game_stats_figure_4.visible = false;
"""
    #</editor-fold>
    #<editor-fold b_fig_4 callback Code String:
b_fig_4_click_code = """
b_fig_1.disabled = false;
b_fig_2.disabled = false;
b_fig_3.disabled = false;
b_fig_4.disabled = true;
game_stats_figure_1.visible = false;
game_stats_figure_2.visible = false;
game_stats_figure_3.visible = false;
game_stats_figure_4.visible = true;
"""
    #</editor-fold>
    #<editor-fold cpu_selected_change_code:
cpu_selected_change_code = """
if(parseInt(cpu_selected.text) == 1){
    if(parseInt(chances_valid.text) == 1){
        if(parseInt(counter_made.text) == 1){
            b_start_automate.visible = true;
        }
        else{
            b_start_automate.visible = false;
        }
    }
    else{
        b_start_automate.visible = false;
    }
}
else{
    b_start_automate.visible = false;
}
if(parseInt(counter_made.text) != 1){
    if(parseInt(chances_valid.text) == 1){
        b_make_counter.visible = true;
    }
    else{
        b_make_counter.visible = false;
    }
}
else{
    b_make_counter.visible = false;
}
"""
    #</editor-fold>
    #<editor-fold chances_valid_change_code:
chances_valid_change_code = """
if(parseInt(cpu_selected.text) == 1){
    if(parseInt(chances_valid.text) == 1){
        if(parseInt(counter_made.text) == 1){
            b_start_automate.visible = true;
        }
        else{
            b_start_automate.visible = false;
        }
    }
    else{
        b_start_automate.visible = false;
    }
}
else{
    b_start_automate.visible = false;
}
if(parseInt(counter_made.text) != 1){
    if(parseInt(chances_valid.text) == 1){
        b_make_counter.visible = true;
    }
    else{
        b_make_counter.visible = false;
    }
}
else{
    b_make_counter.visible = false;
}
"""
    #</editor-fold>
    #<editor-fold counter_made_change_code:
counter_made_change_code = """
if(parseInt(cpu_selected.text) == 1){
    if(parseInt(chances_valid.text) == 1){
        if(parseInt(counter_made.text) == 1){
            b_start_automate.visible = true;
        }
        else{
            b_start_automate.visible = false;
        }
    }
    else{
        b_start_automate.visible = false;
    }
}
else{
    b_start_automate.visible = false;
}
if(parseInt(counter_made.text) != 1){
    if(parseInt(chances_valid.text) == 1){
        b_make_counter.visible = true;
    }
    else{
        b_make_counter.visible = false;
    }
}
else{
    b_make_counter.visible = false;
}
"""
    #</editor-fold>
#</editor-fold>

#<editor-fold create_buttons():
#Needs:
#   from bokeh.models import Button
def create_buttons(configs):

    b_automate = Button(label = configs.b_automate_label,
                        button_type = configs.b_automate_button_type,
                        sizing_mode = configs.b_automate_sizing_mode,
                        width_policy = configs.b_automate_width_policy,
                        disabled = configs.b_automate_disabled,
                        visible = configs.b_automate_visibility)

    b_start_automate = Button(label = configs.b_start_automate_label,
                              button_type = configs.b_start_automate_button_type,
                              sizing_mode = configs.b_start_automate_sizing_mode,
                              width_policy = configs.b_start_automate_width_policy,
                              disabled = configs.b_start_automate_disabled,
                              visible = configs.b_start_automate_visibility)

    b_auto_next = Button(label = configs.b_auto_next_label,
                         button_type = configs.b_auto_next_button_type,
                         sizing_mode = configs.b_auto_next_sizing_mode,
                         width_policy = configs.b_auto_next_width_policy,
                         disabled = configs.b_auto_next_disabled,
                         visible = configs.b_auto_next_visibility)

    b_make_counter = Button(label = configs.b_make_counter_label,
                            button_type = configs.b_make_counter_button_type,
                            sizing_mode = configs.b_make_counter_sizing_mode,
                            width_policy = configs.b_make_counter_width_policy,
                            disabled = configs.b_make_counter_disabled,
                            visible = configs.b_make_counter_visibility)
    b_fig_1 = Button(label = configs.b_fig_1_label,
                     button_type = configs.b_fig_1_button_type,
                     sizing_mode = configs.b_fig_1_sizing_mode,
                     width_policy = configs.b_fig_1_width_policy,
                     disabled = configs.b_fig_1_disabled,
                     visible = configs.b_fig_1_visibility)

    b_fig_2 = Button(label = configs.b_fig_2_label,
                     button_type = configs.b_fig_2_button_type,
                     sizing_mode = configs.b_fig_2_sizing_mode,
                     width_policy = configs.b_fig_2_width_policy,
                     disabled = configs.b_fig_2_disabled,
                     visible = configs.b_fig_2_visibility)

    b_fig_3 = Button(label = configs.b_fig_3_label,
                     button_type = configs.b_fig_3_button_type,
                     sizing_mode = configs.b_fig_3_sizing_mode,
                     width_policy = configs.b_fig_3_width_policy,
                     disabled = configs.b_fig_3_disabled,
                     visible = configs.b_fig_3_visibility)
    b_fig_4 = Button(label = configs.b_fig_4_label,
                     button_type = configs.b_fig_4_button_type,
                     sizing_mode = configs.b_fig_4_sizing_mode,
                     width_policy = configs.b_fig_4_width_policy,
                     disabled = configs.b_fig_4_disabled,
                     visible = configs.b_fig_4_visibility)

    return (b_automate, b_start_automate, b_auto_next, b_make_counter,
            b_fig_1, b_fig_2, b_fig_3, b_fig_4)
#</editor-fold>
#<editor-fold create_sliders():
#Needs:
#   from bokeh.models import Slider
def create_sliders(configs):
    iterations_slider = Slider(start = configs.iterations_slider_start,
                               end = configs.iterations_slider_end,
                               value = configs.iterations_slider_value,
                               step = configs.iterations_slider_step,
                               title = configs.iterations_slider_title,
                               disabled = configs.iterations_slider_disabled,
                               visible = configs.iterations_slider_visibility)

    return (iterations_slider)
#</editor-fold>
#<editor-fold create_gamestate_divs():
#Needs:
#   from bokeh.models.widgets import Div
def create_gamestate_divs(configs):

    iterations_to_run = Div(text = configs.iterations_to_run_start_text,
                            visible = configs.iterations_to_run_visibility)

    strategy_to_use = Div(text = configs.strategy_to_use_start_text,
                          visible = configs.strategy_to_use_visibility)

    nround = Div(text = configs.nround_text,
                 visible = configs.nround_visibility)
    score = Div(text = configs.score_text,
                visible = configs.score_visibility)
    kicker_foot = Div(text = configs.kicker_foot_text,
                      visible = configs.kicker_foot_visibility)
    kicker_kick = Div(text = configs.kicker_kick_text,
                      visible = configs.kicker_kick_visibility)
    cpu_selected = Div(text = "0", visible = False)
    chances_valid = Div(text = "0", visible = False)
    counter_made = Div(text = "1", visible = False)

    return (iterations_to_run, strategy_to_use,
            nround, score, kicker_foot, kicker_kick,
            cpu_selected, chances_valid, counter_made)
#</editor-fold>
#<editor-fold create_strategy_dropdown():
#Needs:
#    from bokeh.models import DropDown
def create_strategy_dropdown(configs):
    #CPU Strategy to Use Dropdown:
    menu = [(configs.fictitious_play_text, configs.fictitious_play_text),
            (configs.mixed_strategy_text, configs.mixed_strategy_text),
            (configs.true_random_text, configs.true_random_text),
            (configs.goalie_cheats_text, configs.goalie_cheats_text)]
    strategy_dropdown = Dropdown(label = configs.dropdown_label, menu = menu,
                                 button_type = configs.dropdown_button_type,
                                 disabled = configs.dropdown_disabled,
                                 visible = configs.dropdown_visibility)
    return strategy_dropdown
#</editor-fold>
#<editor-fold create_distribution_table_source():
#Needs:
#   from bokeh.models import ColumnDataSource
def create_distribution_table_source(configs):
    #Make Automation Distribution Tracking Table:
    distribution_data = dict(footedness = [configs.footedness_left_text,
                                           configs.footedness_left_text,
                                           configs.footedness_left_text,
                                           configs.footedness_right_text,
                                           configs.footedness_right_text,
                                           configs.footedness_right_text],
                             aim_direction = [configs.aim_direction_left_text,
                                              configs.aim_direction_middle_text,
                                              configs.aim_direction_right_text,
                                              configs.aim_direction_left_text,
                                              configs.aim_direction_middle_text,
                                              configs.aim_direction_right_text],
                             freq = [0, 0, 0, 0, 0, 0],
                             decisions = [0, 0, 0, 0, 0, 0],
                             goalie_perceived_risks = [0, 0, 0, 0, 0, 0],
                             striker_score_chance = [0, 0, 0, 0, 0, 0],
                             striker_score_roll = [0, 0, 0, 0, 0, 0])

    distribution_table_source = ColumnDataSource(distribution_data)

    return distribution_table_source
#</editor-fold>
#<editor-fold create_distribution_table():
#Needs:
#   from bokeh.models import TableColumn, DataTable
def create_distribution_table(source, configs):

    footedness_column = TableColumn(field = "footedness",
                                    title = configs.footedness_column_title,
                                    width = configs.footedness_column_width)
    aim_direction_column = TableColumn(field = "aim_direction",
                                       title = configs.aim_direction_column_title,
                                       width = configs.aim_direction_column_width)
    freq_column = TableColumn(field = "freq",
                              title = configs.freq_column_title,
                              width = configs.freq_column_width)
    decisions_column = TableColumn(field = "decisions",
                                   title = configs.decisions_column_title,
                                   width = configs.decisions_column_width)
    perceived_risks_column =  TableColumn(field = "goalie_perceived_risks",
                                          title = configs.perceived_risks_column_title,
                                          width = configs.perceived_risks_column_width)
    score_chance_column = TableColumn(field = "striker_score_chance",
                                      title = configs.score_chance_column_title,
                                      width = configs.score_chance_column_width)
    score_roll_column = TableColumn(field = "striker_score_roll",
                                    title = configs.score_roll_column_title,
                                    width = configs.score_roll_column_width)
    distribution_columns = [footedness_column, aim_direction_column,
                            freq_column, decisions_column,
                            perceived_risks_column, score_chance_column,
                            score_roll_column]

    automation_distribution_table = DataTable(source = source,
                                              columns = distribution_columns,
                                              width = configs.table_width,
                                              height = configs.table_height,
                                              autosize_mode = configs.table_autosize_mode,
                                              sizing_mode = configs.table_sizing_mode,
                                              visible = configs.table_visibility,
                                              fit_columns = configs.table_fit_columns)
    return automation_distribution_table
#</editor-fold>
#<editor-fold create_automation_table_source():
#Needs:
#   from bokeh.models import ColumnDataSource
def create_automation_table_source(configs):

    data = dict(footedness = [configs.footedness_left_text,
                              configs.footedness_left_text,
                              configs.footedness_left_text,
                              configs.footedness_right_text,
                              configs.footedness_right_text,
                              configs.footedness_right_text],
                aim_direction = [configs.aim_direction_left_text,
                                 configs.aim_direction_middle_text,
                                 configs.aim_direction_right_text,
                                 configs.aim_direction_left_text,
                                 configs.aim_direction_middle_text,
                                 configs.aim_direction_right_text],
                chances = [configs.ll_base_chance, configs.lm_base_chance,
                           configs.lr_base_chance, configs.rl_base_chance,
                           configs.rm_base_chance, configs.rr_base_chance])

    automation_table_source = ColumnDataSource(data)
    return automation_table_source
#</editor-fold>
#<editor-fold create_automation_table():
#Needs:
#   from bokeh.models import TableColumn, DataTable
def create_automation_table(source, configs):

    footedness_column = TableColumn(field = "footedness",
                                    title = configs.footedness_column_title)
    aim_direction_column = TableColumn(field = "aim_direction",
                                       title = configs.aim_direction_column_title)
    chances_column = TableColumn(field = "chances",
                                 title = configs.chances_column_title)

    columns = [footedness_column, aim_direction_column, chances_column]

    automation_table = DataTable(source = source, columns = columns,
                                 width = configs.table_width,
                                 height = configs.table_height,
                                 autosize_mode = configs.table_autosize_mode,
                                 visible = configs.table_visibility)
    return automation_table
#</editor-fold>
#<editor-fold create_scr_text():
#Needs:
#    from bokeh.models import ColumnDataSource
def create_scr_text(configs):

    scr_text = ColumnDataSource({'x' : configs.scr_text_xs,
                                 'y' : configs.scr_text_ys,
                                 'text' : [configs.scr_text_ln_1,
                                           configs.scr_text_ln_2,
                                           configs.scr_text_ln_3,
                                           configs.scr_text_ln_4,
                                           configs.scr_text_ln_5]})

    return scr_text;
#</editor-fold>
#<editor-fold create_labels():
#Needs:
#    from bokeh.models.glyphs import Text
def create_labels(configs):
    labels = Text(x = "x", y = "y", text = 'text',
                  text_color = configs.labels_text_color,
                  text_font_size = configs.labels_text_font_size,
                  x_offset = configs.labels_text_x_offset,
                  y_offset = configs.labels_text_y_offset,
                  text_baseline = configs.labels_text_baseline,
                  text_align = configs.labels_text_align)
    return labels;
#</editor-fold>
#<editor-fold create_aim_TextInputs():
def create_aim_TextInputs():
    ll_aim_text_input = TextInput(value = str(0), title = "ll_aim_chance", visible = False)
    lm_aim_text_input = TextInput(value = str(0), title = "lm_aim_chance", visible = False)
    lr_aim_text_input = TextInput(value = str(0), title = "lr_aim_chance", visible = False)
    rl_aim_text_input = TextInput(value = str(0), title = "rl_aim_chance", visible = False)
    rm_aim_text_input = TextInput(value = str(0), title = "rm_aim_chance", visible = False)
    rr_aim_text_input = TextInput(value = str(0), title = "rr_aim_chance", visible = False)
    return (ll_aim_text_input, lm_aim_text_input, lr_aim_text_input,
            rl_aim_text_input, rm_aim_text_input, rr_aim_text_input)
#</editor-fold>
#<editor-fold b_automate_setup():
#Needs:
#   from bokeh.models import CustomJS
def b_automate_setup(b_automate, args_dict):
    b_automate_click = CustomJS(args = args_dict,
                                code = b_automate_code)
    b_automate.js_on_click(b_automate_click)
#</editor-fold>
#<editor-fold b_start_automate_setup():
#Needs:
#   from bokeh.models import CustomJS
def b_start_automate_setup(b_start_automate, args_dict):
    b_start_automate_click = CustomJS(args = args_dict,
                                      code = b_automate_start_code)
    b_start_automate.js_on_click(b_start_automate_click)
#</editor-fold>
#<editor-fold b_auto_next_setup():
#Needs:
#   from bokeh.models import CustomJS
def b_auto_next_setup(b_auto_next, args_dict):
    b_auto_next_click = CustomJS(args = args_dict,
                                 code = automate_loop_iteration)
    b_auto_next.js_on_click(b_auto_next_click)
#</editor-fold>
#<editor-fold b_make_counter_setup():
#Needs:
#    from bokeh.models import ColumnDataSource, CustomJS
def b_make_counter_setup(b_make_counter, args_dict):
    goalie_counter_source = ColumnDataSource(data = dict(chances_l = [1, 0, 0],
                                                         chances_r = [1, 0, 0]))
    args_dict['goalie_counter_source'] = goalie_counter_source
    b_make_counter_click = CustomJS(args = args_dict,
                                    code = b_make_counter_click_code)
    b_make_counter.js_on_click(b_make_counter_click)
    return goalie_counter_source
#</editor-fold>
#<editor-fold b_figs_setup():
#Needs:
#    from bokeh.models import CustomJS
def b_figs_setup(b_fig_1, b_fig_2, b_fig_3, b_fig_4, args_dict):
    b_fig_1_click = CustomJS(args = args_dict,
                             code = b_fig_1_click_code)
    b_fig_2_click = CustomJS(args = args_dict,
                             code = b_fig_2_click_code)
    b_fig_3_click = CustomJS(args = args_dict,
                             code = b_fig_3_click_code)
    b_fig_4_click = CustomJS(args = args_dict,
                            code = b_fig_4_click_code)
    b_fig_1.js_on_click(b_fig_1_click)
    b_fig_2.js_on_click(b_fig_2_click)
    b_fig_3.js_on_click(b_fig_3_click)
    b_fig_4.js_on_click(b_fig_4_click)
#</editor-fold>
#<editor-fold iterations_slider_setup():
#Needs:
#    from bokeh.models import CustomJS
def iterations_slider_setup(iterations_slider, args_dict):
    iterations_slider_callback = CustomJS(args = args_dict,
                                          code = iterations_slider_code)

    iterations_slider.js_on_change('value', iterations_slider_callback)
#</editor-fold>
#<editor-fold strategy_dropdown_setup():
#Needs:
#    from bokeh.models import CustomJS
def strategy_dropdown_setup(strategy_dropdown, args_dict):
    strategy_dropdown_callback = CustomJS(args = args_dict,
                                          code = strategy_dropdown_code)
    strategy_dropdown.js_on_event("menu_item_click",
                                  strategy_dropdown_callback)
#</editor-fold>
#<editor-fold aim_textInputs_setup():
#Needs:
#    from bokeh.models import CustomJS
def aim_textInputs_setup(ll_aim_text_input, lm_aim_text_input,
                         lr_aim_text_input, rl_aim_text_input,
                         rm_aim_text_input, rr_aim_text_input,
                         automation_table_source, chances_valid,
                         b_start_automate):

    args_dict = dict(table_source = automation_table_source,
                     ll_aim_text_input = ll_aim_text_input,
                     lm_aim_text_input = lm_aim_text_input,
                     lr_aim_text_input = lr_aim_text_input,
                     rl_aim_text_input = rl_aim_text_input,
                     rm_aim_text_input = rm_aim_text_input,
                     rr_aim_text_input = rr_aim_text_input,
                     chances_valid = chances_valid,
                     b_start_automate = b_start_automate)

    aim_textInputs_customjs = CustomJS(args = args_dict,
                                       code = aim_inputs_callback_code)

    ll_aim_text_input.js_on_change('value', aim_textInputs_customjs)
    lm_aim_text_input.js_on_change('value', aim_textInputs_customjs)
    lr_aim_text_input.js_on_change('value', aim_textInputs_customjs)
    rl_aim_text_input.js_on_change('value', aim_textInputs_customjs)
    rm_aim_text_input.js_on_change('value', aim_textInputs_customjs)
    rr_aim_text_input.js_on_change('value', aim_textInputs_customjs)
#</editor-fold>
#<editor-fold format_layout():
#Needs:
#    from bokeh.layouts import row, column, gridplot
def format_layout(b_automate, iterations_slider, b_auto_next,
                  strategy_dropdown, b_start_automate, b_make_counter,
                  game_stats_figure_1,
                  game_stats_figure_2, game_stats_figure_3,
                  game_stats_figure_4,
                  game_figure, automation_table, automation_distribution_table,
                  b_fig_1, b_fig_2, b_fig_3, b_fig_4, ll_aim_text_input,
                  lm_aim_text_input, lr_aim_text_input, rl_aim_text_input,
                  rm_aim_text_input, rr_aim_text_input, configs):

    automate_button_row = row(b_automate, iterations_slider, b_auto_next,
                              max_width = configs.automate_button_row_max_width,
                              sizing_mode = configs.automate_button_row_sizing_mode)

    strategy_dropdown_row = row(strategy_dropdown,
                                max_width = configs.strategy_dropdown_row_max_width,
                                sizing_mode = configs.strategy_dropdown_row_sizing_mode)

    start_automate_row = row(b_start_automate, b_make_counter,
                             max_width = configs.start_automate_row_max_width,
                             sizing_mode = configs.start_automate_row_sizing_mode)

    automate_LL_aim_row = row(ll_aim_text_input,
                              max_width = configs.automate_aim_rows_max_width,
                              sizing_mode = configs.automate_aim_rows_sizing_mode)
    automate_LM_aim_row = row(lm_aim_text_input,
                              max_width = configs.automate_aim_rows_max_width,
                              sizing_mode = configs.automate_aim_rows_sizing_mode)
    automate_LR_aim_row = row(lr_aim_text_input,
                              max_width = configs.automate_aim_rows_max_width,
                              sizing_mode = configs.automate_aim_rows_sizing_mode)
    automate_RL_aim_row = row(rl_aim_text_input,
                              max_width = configs.automate_aim_rows_max_width,
                              sizing_mode = configs.automate_aim_rows_sizing_mode)
    automate_RM_aim_row = row(rm_aim_text_input,
                              max_width = configs.automate_aim_rows_max_width,
                              sizing_mode = configs.automate_aim_rows_sizing_mode)
    automate_RR_aim_row = row(rr_aim_text_input,
                              max_width = configs.automate_aim_rows_max_width,
                              sizing_mode = configs.automate_aim_rows_sizing_mode)

    game_stats_row_1 = row(game_stats_figure_1, game_stats_figure_2,
                           max_width = configs.game_stats_row_1_max_width,
                           sizing_mode = configs.game_stats_row_1_sizing_mode)
    game_stats_row_2 = row(game_stats_figure_3, game_stats_figure_4,
                           max_width = configs.game_stats_row_2_max_width,
                           sizing_mode = configs.game_stats_row_2_sizing_mode)

    b_fig_1_row = row(b_fig_1, max_width = configs.b_fig_rows_max_width,
                      sizing_mode = configs.b_fig_rows_sizing_mode)
    b_fig_2_row = row(b_fig_2, max_width = configs.b_fig_rows_max_width,
                      sizing_mode = configs.b_fig_rows_sizing_mode)
    b_fig_3_row = row(b_fig_3, max_width = configs.b_fig_rows_max_width,
                      sizing_mode = configs.b_fig_rows_sizing_mode)
    b_fig_4_row = row(b_fig_4, max_width = configs.b_fig_rows_max_width,
                      sizing_mode = configs.b_fig_rows_sizing_mode)

    gui_column1 = column(game_figure, game_stats_row_1, game_stats_row_2,
                         max_width = configs.gui_column1_max_width,
                         sizing_mode = configs.gui_column1_sizing_mode)
    gui_column2 = column(b_fig_1_row, b_fig_2_row, b_fig_3_row, b_fig_4_row,
                         automate_button_row, strategy_dropdown_row,
                         start_automate_row, automate_LL_aim_row,
                         automate_LM_aim_row, automate_LR_aim_row,
                         automate_RL_aim_row, automate_RM_aim_row,
                         automate_RR_aim_row, automation_table,
                         automation_distribution_table,
                         min_width = configs.gui_column2_min_width,
                         max_width = configs.gui_column2_max_width,
                         sizing_mode = configs.gui_column2_sizing_mode)

    gui_row = row(gui_column1, gui_column2,
                  max_width = configs.gui_row_max_width,
                  sizing_mode = configs.gui_row_sizing_mode)

    grid1 = gridplot([[gui_row]],
                     plot_width = configs.plot_width,
                     plot_height = configs.plot_height)
    return grid1
#</editor-fold>
#<editor-fold scr_text and labels configs:
class Scr_text_and_labels_configs:
    def __init__(self, scr_text_xs = [2, 70, 2, 14, 14],
                 scr_text_ys = [86, 86, 5, 40, 32],
                 scr_text_ln_1 = 'Rounds played: 0',
                 scr_text_ln_2 = 'Total score: 0', scr_text_ln_3 = '',
                 scr_text_ln_4 = '', scr_text_ln_5 = '',
                 labels_text_color = "whitesmoke",
                 labels_text_font_size = "15pt",
                 labels_text_x_offset = 0,
                 labels_text_y_offset = +9,
                 labels_text_baseline = "ideographic",
                 labels_text_align = 'left'):
        self.scr_text_xs = scr_text_xs
        self.scr_text_ys = scr_text_ys
        self.scr_text_ln_1 = scr_text_ln_1
        self.scr_text_ln_2 = scr_text_ln_2
        self.scr_text_ln_3 = scr_text_ln_3
        self.scr_text_ln_4 = scr_text_ln_4
        self.scr_text_ln_5 = scr_text_ln_5
        self.labels_text_color = labels_text_color
        self.labels_text_font_size = labels_text_font_size
        self.labels_text_x_offset = labels_text_x_offset
        self.labels_text_y_offset = labels_text_y_offset
        self.labels_text_baseline = labels_text_baseline
        self.labels_text_align = labels_text_align
#</editor-fold>
#<editor-fold Gamestate_divs_configs:
class Gamestate_divs_configs:
    def __init__(self, iterations_to_run_start_text = "50",
                 iterations_to_run_visibility = False,
                 strategy_to_use_start_text = "Not Set",
                 strategy_to_use_visibility = False,
                 nround_text = '0', nround_visibility = False,
                 score_text = '0', score_visibility = False,
                 kicker_foot_text = '',
                 kicker_foot_visibility = False,
                 kicker_kick_text = '',
                 kicker_kick_visibility = False):
        self.iterations_to_run_start_text = iterations_to_run_start_text
        self.iterations_to_run_visibility = iterations_to_run_visibility
        self.strategy_to_use_start_text = strategy_to_use_start_text
        self.strategy_to_use_visibility = strategy_to_use_visibility
        self.nround_text = nround_text
        self.nround_visibility = nround_visibility
        self.score_text = score_text
        self.score_visibility = score_visibility
        self.kicker_foot_text = kicker_foot_text
        self.kicker_foot_visibility = kicker_foot_visibility
        self.kicker_kick_text = kicker_kick_text
        self.kicker_kick_visibility = kicker_kick_visibility
#</editor-fold>
#<editor-fold Button_configs:
class Button_configs:
    def __init__(self, b_automate_label = "Automate",
                 b_automate_button_type = "success",
                 b_automate_sizing_mode = "scale_width",
                 b_automate_width_policy = "fit",
                 b_automate_disabled = False, b_automate_visibility = True,
                 b_start_automate_label = "Start",
                 b_start_automate_button_type = "success",
                 b_start_automate_sizing_mode = "scale_width",
                 b_start_automate_width_policy = "fit",
                 b_start_automate_disabled = False,
                 b_start_automate_visibility = False,
                 b_auto_next_label = "Next",
                 b_auto_next_button_type = "success",
                 b_auto_next_sizing_mode = "scale_width",
                 b_auto_next_width_policy = "fit",
                 b_auto_next_disabled = False, b_auto_next_visibility = False,
                 b_make_counter_label = "Make Counter",
                 b_make_counter_button_type = "success",
                 b_make_counter_sizing_mode = "scale_width",
                 b_make_counter_width_policy = "fit",
                 b_make_counter_disabled = False,
                 b_make_counter_visibility = False,
                 b_fig_1_label = "Figure 1",
                 b_fig_1_button_type = "success",
                 b_fig_1_sizing_mode = "scale_width",
                 b_fig_1_width_policy = "fit",
                 b_fig_1_disabled = True,
                 b_fig_1_visibility = False,
                 b_fig_2_label = "Figure 2",
                 b_fig_2_button_type = "success",
                 b_fig_2_sizing_mode = "scale_width",
                 b_fig_2_width_policy = "fit",
                 b_fig_2_disabled = False,
                 b_fig_2_visibility = False,
                 b_fig_3_label = "Figure 3",
                 b_fig_3_button_type = "success",
                 b_fig_3_sizing_mode = "scale_width",
                 b_fig_3_width_policy = "fit",
                 b_fig_3_disabled = False,
                 b_fig_3_visibility = False,
                 b_fig_4_label = "Figure 4",
                 b_fig_4_button_type = "success",
                 b_fig_4_sizing_mode = "scale_width",
                 b_fig_4_width_policy = "fit",
                 b_fig_4_disabled = False,
                 b_fig_4_visibility = False):
        self.b_automate_label = b_automate_label
        self.b_automate_button_type = b_automate_button_type
        self.b_automate_sizing_mode = b_automate_sizing_mode
        self.b_automate_width_policy = b_automate_width_policy
        self.b_automate_disabled = b_automate_disabled
        self.b_automate_visibility = b_automate_visibility
        self.b_start_automate_label = b_start_automate_label
        self.b_start_automate_button_type = b_start_automate_button_type
        self.b_start_automate_sizing_mode = b_start_automate_sizing_mode
        self.b_start_automate_width_policy = b_start_automate_width_policy
        self.b_start_automate_disabled = b_start_automate_disabled
        self.b_start_automate_visibility = b_start_automate_visibility
        self.b_auto_next_label = b_auto_next_label
        self.b_auto_next_button_type = b_auto_next_button_type
        self.b_auto_next_sizing_mode = b_auto_next_sizing_mode
        self.b_auto_next_width_policy = b_auto_next_width_policy
        self.b_auto_next_disabled = b_auto_next_disabled
        self.b_auto_next_visibility = b_auto_next_visibility
        self.b_make_counter_label = b_make_counter_label
        self.b_make_counter_button_type = b_make_counter_button_type
        self.b_make_counter_sizing_mode = b_make_counter_sizing_mode
        self.b_make_counter_width_policy = b_make_counter_width_policy
        self.b_make_counter_disabled = b_make_counter_disabled
        self.b_make_counter_visibility = b_make_counter_visibility
        self.b_fig_1_label = b_fig_1_label
        self.b_fig_1_button_type = b_fig_1_button_type
        self.b_fig_1_sizing_mode = b_fig_1_sizing_mode
        self.b_fig_1_width_policy = b_fig_1_width_policy
        self.b_fig_1_disabled = b_fig_1_disabled
        self.b_fig_1_visibility = b_fig_1_visibility
        self.b_fig_2_label = b_fig_2_label
        self.b_fig_2_button_type = b_fig_2_button_type
        self.b_fig_2_sizing_mode = b_fig_2_sizing_mode
        self.b_fig_2_width_policy = b_fig_2_width_policy
        self.b_fig_2_disabled = b_fig_2_disabled
        self.b_fig_2_visibility = b_fig_2_visibility
        self.b_fig_3_label = b_fig_3_label
        self.b_fig_3_button_type = b_fig_3_button_type
        self.b_fig_3_sizing_mode = b_fig_3_sizing_mode
        self.b_fig_3_width_policy = b_fig_3_width_policy
        self.b_fig_3_disabled = b_fig_3_disabled
        self.b_fig_3_visibility = b_fig_3_visibility
        self.b_fig_4_label = b_fig_4_label
        self.b_fig_4_button_type = b_fig_4_button_type
        self.b_fig_4_sizing_mode = b_fig_4_sizing_mode
        self.b_fig_4_width_policy = b_fig_4_width_policy
        self.b_fig_4_disabled = b_fig_4_disabled
        self.b_fig_4_visibility = b_fig_4_visibility
#</editor-fold>
#<editor-fold Slider_configs:
class Slider_configs:
    def __init__(self,
                 iterations_slider_start = 10, iterations_slider_end = 500,
                 iterations_slider_value = 50, iterations_slider_step = 10,
                 iterations_slider_title = "Iterations To Run",
                 iterations_slider_disabled = False,
                 iterations_slider_visibility = False):
        self.iterations_slider_start = iterations_slider_start
        self.iterations_slider_end = iterations_slider_end
        self.iterations_slider_value = iterations_slider_value
        self.iterations_slider_step = iterations_slider_step
        self.iterations_slider_title = iterations_slider_title
        self.iterations_slider_disabled = iterations_slider_disabled
        self.iterations_slider_visibility = iterations_slider_visibility
#</editor-fold>
#<editor-fold Strategy_dropdown_configs:
class Strategy_dropdown_configs:
    def __init__(self, fictitious_play_text = "Fictitious_Play",
                 mixed_strategy_text = "Mixed_Strategy",
                 true_random_text = "Random",
                 goalie_cheats_text = "Goalie_Cheats",
                 dropdown_label = "CPU strategy to Use",
                 dropdown_button_type = "warning", dropdown_disabled = False,
                 dropdown_visibility = False):
        self.fictitious_play_text = fictitious_play_text
        self.mixed_strategy_text = mixed_strategy_text
        self.true_random_text = true_random_text
        self.goalie_cheats_text = goalie_cheats_text
        self.dropdown_label = dropdown_label
        self.dropdown_button_type = dropdown_button_type
        self.dropdown_disabled = dropdown_disabled
        self.dropdown_visibility = dropdown_visibility
#</editor-fold>
#<editor-fold Distribution_table_configs:
class Distribution_table_configs:
    def __init__(self, footedness_left_text = "Left",
                 footedness_right_text = "Right",
                 aim_direction_left_text = "Left",
                 aim_direction_middle_text = "Middle",
                 aim_direction_right_text = "Right",
                 footedness_column_title = "Striker Footedness",
                 footedness_column_width = 101,
                 aim_direction_column_title = "Striker Aim Direction",
                 aim_direction_column_width = 107,
                 freq_column_title = "Frequency", freq_column_width = 60,
                 decisions_column_title = "Goalie Decisions",
                 decisions_column_width = 90,
                 perceived_risks_column_title = "Goalie Perceived Risks",
                 perceived_risks_column_width = 130,
                 score_chance_column_title = "Striker's Score Chance",
                 score_chance_column_width = 120,
                 score_roll_column_title = "Striker's Score Roll",
                 score_roll_column_width = 103, table_width = 711,
                 table_height = 280, table_autosize_mode = "force_fit",
                 table_sizing_mode = "scale_width", table_visibility = False,
                 table_fit_columns = False):
        self.footedness_left_text = footedness_left_text
        self.footedness_right_text = footedness_right_text
        self.aim_direction_left_text = aim_direction_left_text
        self.aim_direction_middle_text = aim_direction_middle_text
        self.aim_direction_right_text = aim_direction_right_text

        self.footedness_column_title = footedness_column_title
        self.footedness_column_width = footedness_column_width
        self.aim_direction_column_title = aim_direction_column_title
        self.aim_direction_column_width = aim_direction_column_width
        self.freq_column_title = freq_column_title
        self.freq_column_width = freq_column_width
        self.decisions_column_title = decisions_column_title
        self.decisions_column_width = decisions_column_width
        self.perceived_risks_column_title = perceived_risks_column_title
        self.perceived_risks_column_width = perceived_risks_column_width
        self.score_chance_column_title = score_chance_column_title
        self.score_chance_column_width = score_chance_column_width
        self.score_roll_column_title = score_roll_column_title
        self.score_roll_column_width = score_roll_column_width
        self.table_width = table_width
        self.table_height = table_height
        self.table_autosize_mode = table_autosize_mode
        self.table_sizing_mode = table_sizing_mode
        self.table_visibility = table_visibility
        self.table_fit_columns = table_fit_columns
#</editor-fold>
#<editor-fold Automation_table_configs:
class Automation_table_configs:
    def __init__(self, ll_base_chance = 1/6, lm_base_chance = 1/6,
                 lr_base_chance = 1/6, rl_base_chance = 1/6,
                 rm_base_chance = 1/6, rr_base_chance = 1/6,
                 footedness_left_text = "Left",
                 footedness_right_text = "Right",
                 aim_direction_left_text = "Left",
                 aim_direction_middle_text = "Middle",
                 aim_direction_right_text = "Right",
                 footedness_column_title = "Striker Footedness",
                 aim_direction_column_title = "Striker Aim Direction",
                 chances_column_title = "Chance", table_width = 600,
                 table_height = 280,
                 table_autosize_mode = "force_fit",
                 table_visibility = False):
        self.ll_base_chance = ll_base_chance
        self.lm_base_chance = lm_base_chance
        self.lr_base_chance = lr_base_chance
        self.rl_base_chance = rl_base_chance
        self.rm_base_chance = rm_base_chance
        self.rr_base_chance = rr_base_chance
        self.footedness_left_text = footedness_left_text
        self.footedness_right_text = footedness_right_text
        self.aim_direction_left_text = aim_direction_left_text
        self.aim_direction_middle_text = aim_direction_middle_text
        self.aim_direction_right_text = aim_direction_right_text

        self.footedness_column_title = footedness_column_title
        self.aim_direction_column_title = aim_direction_column_title
        self.chances_column_title = chances_column_title
        self.table_width = table_width
        self.table_height = table_height
        self.table_autosize_mode = table_autosize_mode
        self.table_visibility = table_visibility
#</editor-fold>
#<editor-fold layout_configs:
class Layout_configs:
    def __init__(self, automate_button_row_max_width = 400,
                 automate_button_row_sizing_mode = 'stretch_width',
                 strategy_dropdown_row_max_width = 400,
                 strategy_dropdown_row_sizing_mode = 'stretch_width',
                 start_automate_row_max_width = 400,
                 start_automate_row_sizing_mode = 'stretch_width',
                 automate_aim_rows_max_width = 400,
                 automate_aim_rows_sizing_mode = 'stretch_width',
                 game_stats_row_1_max_width = 600,
                 game_stats_row_1_sizing_mode = 'stretch_width',
                 game_stats_row_2_max_width = 600,
                 game_stats_row_2_sizing_mode = 'stretch_width',
                 gui_column1_max_width = 600,
                 gui_column1_sizing_mode = 'stretch_width',
                 gui_column2_min_width = 761, gui_column2_max_width = 761,
                 gui_column2_sizing_mode = 'stretch_width',
                 gui_row_max_width = 1400,
                 gui_row_sizing_mode = 'stretch_width',
                 plot_width = 1200, plot_height = 480,
                 b_fig_rows_max_width = 400,
                 b_fig_rows_sizing_mode = 'stretch_width'):
        self.automate_button_row_max_width = automate_button_row_max_width
        self.automate_button_row_sizing_mode = automate_button_row_sizing_mode
        self.strategy_dropdown_row_max_width = strategy_dropdown_row_max_width
        self.strategy_dropdown_row_sizing_mode = strategy_dropdown_row_sizing_mode
        self.start_automate_row_max_width = start_automate_row_max_width
        self.start_automate_row_sizing_mode = start_automate_row_sizing_mode
        self.automate_aim_rows_max_width = automate_aim_rows_max_width
        self.automate_aim_rows_sizing_mode = automate_aim_rows_sizing_mode
        self.game_stats_row_1_max_width = game_stats_row_1_max_width
        self.game_stats_row_1_sizing_mode = game_stats_row_1_sizing_mode
        self.game_stats_row_2_max_width = game_stats_row_2_max_width
        self.game_stats_row_2_sizing_mode = game_stats_row_2_sizing_mode
        self.gui_column1_max_width = gui_column1_max_width
        self.gui_column1_sizing_mode = gui_column1_sizing_mode
        self.gui_column2_min_width = gui_column2_min_width
        self.gui_column2_max_width = gui_column2_max_width
        self.gui_column2_sizing_mode = gui_column2_sizing_mode
        self.gui_row_max_width = gui_row_max_width
        self.gui_row_sizing_mode = gui_row_sizing_mode
        self.plot_width = plot_width
        self.plot_height = plot_height
        self.b_fig_rows_max_width = b_fig_rows_max_width
        self.b_fig_rows_sizing_mode = b_fig_rows_sizing_mode
#</editor-fold>
#<editor-fold cpu_selected_setup():
def cpu_selected_setup(cpu_selected, args_dict):
    cpu_selected.js_on_change('text', CustomJS(code = cpu_selected_change_code,
                                               args = args_dict))
#</editor-fold>
#<editor-fold chances_valid_setup():
def chances_valid_setup(chances_valid, args_dict):
    chances_valid.js_on_change('text', CustomJS(code = chances_valid_change_code,
                                               args = args_dict))
#</editor-fold>
#<editor-fold counter_made_setup():
def counter_made_setup(counter_made, args_dict):
    counter_made.js_on_change('text', CustomJS(code = counter_made_change_code,
                                               args = args_dict))
#</editor-fold>
#<editor-fold make_game():
#Needs:
#    from main_game_figure import game_figure_setup, Game_fig_configs
#    from game_stats_figure_1 import stats_figure_1_setup, Stats_fig_1_configs
#    from game_stats_figure_2 import stats_figure_2_setup, Stats_fig_2_configs
#    from game_stats_figure_3 import stats_figure_3_setup, Stats_fig_3_configs
#<editor-fold Define defaults:
default_game_fig_configs = Game_fig_configs()
default_fig_1_configs = Stats_fig_1_configs()
default_fig_2_configs = Stats_fig_2_configs()
default_fig_3_configs = Stats_fig_3_configs()
default_fig_4_configs = Stats_fig_4_configs()
default_scr_text_and_labels_configs = Scr_text_and_labels_configs()
default_gamestate_divs_configs = Gamestate_divs_configs()
default_button_configs = Button_configs()
default_slider_configs = Slider_configs()
default_strategy_dropdown_configs = Strategy_dropdown_configs()
default_distribution_table_configs = Distribution_table_configs()
default_automation_table_configs = Automation_table_configs()
default_layout_configs = Layout_configs()
#</editor-fold>
#<editor-fold Helpers:
def __add_aim_textInputs(args_dict, aim_textInputs):
    args_dict['ll_aim_text_input'] = aim_textInputs[0]
    args_dict['lm_aim_text_input'] = aim_textInputs[1]
    args_dict['lr_aim_text_input'] = aim_textInputs[2]
    args_dict['rl_aim_text_input'] = aim_textInputs[3]
    args_dict['rm_aim_text_input'] = aim_textInputs[4]
    args_dict['rr_aim_text_input'] = aim_textInputs[5]
def __add_stat_figs(args_dict, stat_figs):
    args_dict['game_stats_figure_1'] = stat_figs[0]
    args_dict['game_stats_figure_2'] = stat_figs[1]
    args_dict['game_stats_figure_3'] = stat_figs[2]
    args_dict['game_stats_figure_4'] = stat_figs[3]
def __add_stat_fig_sources(args_dict, stat_fig_sources):
    args_dict['game_stats_figure_2_source'] = stat_fig_sources[0]
    args_dict['game_stats_figure_3_source'] = stat_fig_sources[1]
    args_dict['game_stats_figure_4_source'] = stat_fig_sources[2]
#</editor-fold>

def make_game(game_figure_configs = default_game_fig_configs,
              stats_figure_1_configs = default_fig_1_configs,
              stats_figure_2_configs = default_fig_2_configs,
              stats_figure_3_configs = default_fig_3_configs,
              stats_figure_4_configs = default_fig_4_configs,
              scrtxt_labels_configs = default_scr_text_and_labels_configs,
              divs_configs = default_gamestate_divs_configs,
              button_configs = default_button_configs,
              slider_configs = default_slider_configs,
              strategy_dropdown_configs = default_strategy_dropdown_configs,
              distribution_table_configs = default_distribution_table_configs,
              automation_table_configs = default_automation_table_configs,
              layout_configs = default_layout_configs):
    #<editor-fold create objects used in game:
        #<editor-fold figure setups:
    (game_figure, goalie_head, goalie_body,
    ball) = game_figure_setup(game_figure_configs)

    (game_stats_figure_1,
     game_stats_figure_1_source) = stats_figure_1_setup(stats_figure_1_configs)

    (game_stats_figure_2,
     game_stats_figure_2_source) = stats_figure_2_setup(stats_figure_2_configs)

    (game_stats_figure_3,
     game_stats_figure_3_source) = stats_figure_3_setup(stats_figure_3_configs)

    (game_stats_figure_4,
     game_stats_figure_4_source) = stats_figure_4_setup(stats_figure_4_configs)
        #</editor-fold>
        #<editor-fold scr_text and labels:
    scr_text = create_scr_text(scrtxt_labels_configs);
    labels = create_labels(scrtxt_labels_configs);

    game_figure.add_glyph(scr_text, labels);
        #</editor-fold>
        #<editor-fold divs:
    (iterations_to_run, strategy_to_use, nround, score, kicker_foot,
     kicker_kick, cpu_selected, chances_valid,
     counter_made) = create_gamestate_divs(divs_configs)
        #</editor-fold>
        #<editor-fold buttons:
    (b_automate, b_start_automate,
     b_auto_next, b_make_counter, b_fig_1,
     b_fig_2, b_fig_3, b_fig_4) = create_buttons(button_configs)
        #</editor-fold>
        #<editor-fold sliders:
    (iterations_slider) = create_sliders(slider_configs)
        #</editor-fold>
        #<editor-fold aim textInputs:
    (ll_aim_text_input, lm_aim_text_input, lr_aim_text_input,
     rl_aim_text_input, rm_aim_text_input,
     rr_aim_text_input) = create_aim_TextInputs()
        #</editor-fold>
        #<editor-fold strategy_dropdown:
    strategy_dropdown = create_strategy_dropdown(strategy_dropdown_configs)
        #</editor-fold>
        #<editor-fold automation_distribution_table:
    automation_distribution_table_source = create_distribution_table_source(distribution_table_configs)
    automation_distribution_table = create_distribution_table(automation_distribution_table_source,
                                                              distribution_table_configs)
        #</editor-fold>
        #<editor-fold automation_table:
    automation_table_source = create_automation_table_source(automation_table_configs)
    automation_table = create_automation_table(automation_table_source,
                                               automation_table_configs)
        #</editor-fold>
    #</editor-fold>
    #<editor-fold Setup for using helpers to add to argsdicts:
    aim_textInputs = [ll_aim_text_input, lm_aim_text_input, lr_aim_text_input,
                      rl_aim_text_input, rm_aim_text_input, rr_aim_text_input]
    stat_figs = [game_stats_figure_1, game_stats_figure_2, game_stats_figure_3,
                 game_stats_figure_4]
    stat_fig_sources = [game_stats_figure_2_source, game_stats_figure_3_source,
                        game_stats_figure_4_source]
    #</editor-fold>

    #<editor-fold setup created objects:
        #<editor-fold b_automate setup:
    args_dict = dict(b_automate = b_automate,
                     iterations_slider = iterations_slider,
                     strategy_dropdown = strategy_dropdown,
                     automation_table = automation_table, txt = scr_text)
    __add_aim_textInputs(args_dict, aim_textInputs)

    b_automate_setup(b_automate = b_automate, args_dict = args_dict)
        #</editor-fold>
        #<editor-fold b_start_automate_visibility setup:
    args_dict = dict(b_start_automate = b_start_automate,
                     b_make_counter = b_make_counter,
                     cpu_selected = cpu_selected,
                     counter_made = counter_made,
                     chances_valid = chances_valid)
    cpu_selected_setup(cpu_selected = cpu_selected,
                       args_dict = args_dict)
    chances_valid_setup(chances_valid = chances_valid,
                        args_dict = args_dict)
    counter_made_setup(counter_made = counter_made,
                       args_dict = args_dict)
        #</editor-fold>
        #<editor-fold b_make_counter setup:
    args_dict = dict(b_start_automate = b_start_automate,
                     b_make_counter = b_make_counter,
                     automation_table = automation_table,
                     automation_table_source = automation_table_source,
                     counter_made = counter_made)
    __add_aim_textInputs(args_dict, aim_textInputs)

    goalie_counter_source = b_make_counter_setup(b_make_counter, args_dict)
        #</editor-fold>
        #<editor-fold b_figs_setup:
    args_dict = dict(b_fig_1 = b_fig_1, b_fig_2 = b_fig_2, b_fig_3 = b_fig_3,
                     b_fig_4 = b_fig_4,
                     game_stats_figure_1 = game_stats_figure_1,
                     game_stats_figure_2 = game_stats_figure_2,
                     game_stats_figure_3 = game_stats_figure_3,
                     game_stats_figure_4 = game_stats_figure_4)
    b_figs_setup(b_fig_1 = b_fig_1, b_fig_2 = b_fig_2, b_fig_3 = b_fig_3,
                 b_fig_4 = b_fig_4,
                 args_dict = args_dict)
        #</editor-fold>
        #<editor-fold main game setup:
            #<editor-fold loop_dict:
    loop_dict =  dict(ChancesColumnDataSource = automation_table_source,
                      DistributionColumnDataSource = automation_distribution_table_source,
                      strategy_to_use = strategy_to_use, nround = nround,
                      iterations_to_run = iterations_to_run, txt = scr_text,
                      b_auto_next = b_auto_next, game_figure = game_figure,
                      automation_distribution_table = automation_distribution_table,
                      goalie_head = goalie_head, goalie_body = goalie_body,
                      goalie_counter_source = goalie_counter_source,
                      ball = ball, score = score, b_fig_1 = b_fig_1,
                      b_fig_2 = b_fig_2, b_fig_3 = b_fig_3, b_fig_4 = b_fig_4,
                      game_stats_figure_1_source = game_stats_figure_1_source)
    __add_stat_figs(loop_dict, stat_figs)
    __add_stat_fig_sources(loop_dict, stat_fig_sources)
            #</editor-fold>
            #<editor-fold b_start_automate setup:
    args_dict = loop_dict.copy()
    args_dict['b_start_automate'] = b_start_automate
    args_dict['iterations_slider'] = iterations_slider
    args_dict['strategy_dropdown'] = strategy_dropdown
    args_dict['automation_table'] = automation_table
    __add_aim_textInputs(args_dict, aim_textInputs)

    b_start_automate_setup(b_start_automate = b_start_automate,
                           args_dict = args_dict)
            #</editor-fold>
            #<editor-fold b_auto_next setup:
    args_dict = loop_dict

    b_auto_next_setup(b_auto_next = b_auto_next, args_dict = args_dict)
            #</editor-fold>
        #</editor-fold>
        #<editor-fold iterations_slider setup:
    args_dict = dict(iterations_to_run = iterations_to_run)
    __add_stat_figs(args_dict, stat_figs)
    __add_stat_fig_sources(args_dict, stat_fig_sources)

    iterations_slider_setup(iterations_slider = iterations_slider,
                            args_dict = args_dict)
        #</editor-fold>
        #<editor-fold aim_textInputs_setup:
    aim_textInputs_setup(ll_aim_text_input = ll_aim_text_input,
                         lm_aim_text_input = lm_aim_text_input,
                         lr_aim_text_input = lr_aim_text_input,
                         rl_aim_text_input = rl_aim_text_input,
                         rm_aim_text_input = rm_aim_text_input,
                         rr_aim_text_input = rr_aim_text_input,
                         chances_valid = chances_valid,
                         automation_table_source = automation_table_source,
                         b_start_automate = b_start_automate)
        #</editor-fold>
        #<editor-fold strategy_dropdown setup:
    args_dict = dict(strategy_dropdown = strategy_dropdown,
                     strategy_to_use = strategy_to_use,
                     b_start_automate = b_start_automate,
                     b_make_counter = b_make_counter,
                     automation_table = automation_table,
                     cpu_selected = cpu_selected, counter_made = counter_made)
    __add_aim_textInputs(args_dict, aim_textInputs)

    strategy_dropdown_setup(strategy_dropdown = strategy_dropdown,
                            args_dict = args_dict)
        #</editor-fold>
    #</editor-fold>

    #<editor-fold format game layout:
    grid1 = format_layout(b_automate = b_automate,
                          iterations_slider = iterations_slider,
                          b_auto_next = b_auto_next,
                          strategy_dropdown = strategy_dropdown,
                          b_start_automate = b_start_automate,
                          b_make_counter = b_make_counter,
                          ll_aim_text_input = ll_aim_text_input,
                          lm_aim_text_input = lm_aim_text_input,
                          lr_aim_text_input = lr_aim_text_input,
                          rl_aim_text_input = rl_aim_text_input,
                          rm_aim_text_input = rm_aim_text_input,
                          rr_aim_text_input = rr_aim_text_input,
                          game_stats_figure_1 = game_stats_figure_1,
                          game_stats_figure_2 = game_stats_figure_2,
                          game_stats_figure_3 = game_stats_figure_3,
                          game_stats_figure_4 = game_stats_figure_4,
                          game_figure = game_figure,
                          automation_table = automation_table,
                          automation_distribution_table = automation_distribution_table,
                          b_fig_1 = b_fig_1, b_fig_2 = b_fig_2,
                          b_fig_3 = b_fig_3, b_fig_4 = b_fig_4,
                          configs = layout_configs)
    #</editor-fold>

    return grid1
#</editor-fold>
