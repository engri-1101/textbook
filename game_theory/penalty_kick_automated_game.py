from bokeh.models import (Button, Slider, Dropdown, ColumnDataSource,
                          TableColumn, DataTable, CustomJS)
from bokeh.models.widgets import Div

#<editor-fold Code Strings:
    #Has Been worked On?:
    #<editor-fold b_automate Callback Code String:
b_automate_code = """
//Change visibilities of game items:
b_automate.visible = false;
b_start.visible = false;
b_fl.visible = false;
b_fr.visible = false;
b_next.visible = false;
LL_aim_slider.visible = true;
LM_aim_slider.visible = true;
LR_aim_slider.visible = true;
RL_aim_slider.visible = true;
RM_aim_slider.visible = true;
RR_aim_slider.visible = true;
iterations_slider.visible = true;
strategy_dropdown.visible = true;
automation_table.visible = true;
"""
    #</editor-fold>
    #Has Been worked On?:
    #<editor-fold automate_start_code Initial Gui Display Code String:
automate_start_code_initial_gui_display = """
b_start_automate.visible = false;
b_auto_next.visible = true;

LL_aim_slider.visible = false;
LM_aim_slider.visible = false;
LR_aim_slider.visible = false;
RL_aim_slider.visible = false;
RM_aim_slider.visible = false;
RR_aim_slider.visible = false;

iterations_slider.visible = false;

strategy_dropdown.visible = false;

automation_table.visible = false;
automation_distribution_table.visible = true;
"""
    #</editor-fold>
    #Has Been worked On?:
    #<editor-fold automate_loop Code Strings:
automate_loop_iteration_var_instantiations = """
// Define probability matrix
var p = {'Right' : {'LeftLeft' : 0.55,
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

//Obtain the Shot Aim chances from the column data source
    var chances_data = ChancesColumnDataSource.data;
    var chances = chances_data['chances'];
    var LL_chance = chances[0];
    var LM_chance = LL_chance + chances[1];
    var LR_chance = LM_chance + chances[2];
    var RL_chance = LR_chance + chances[3];
    var RM_chance = RL_chance + chances[4];

//Goalie Logic Decision Making Variables
    var chance_left = 1/3;
    var chance_middle = 1/3;
    var chance_right = 1/3;

    var danger_goalie_left = 0;
    var danger_goalie_middle = 0;
    var danger_goalie_right = 0;
    var selected_dict = 0;

    var total_sample_rolls;

    var goalie_action = "None";

//Loop Randomness Variable
    var roll = 0;

//Goalie Fictitious Learning Variables
    var selected_index = 0;

    var dist_data = DistributionColumnDataSource.data;
    var freq = dist_data['freq'];
    var decisions = dist_data['decisions'];

//Data Display Variables
    var perceived_risks = dist_data['goalie_perceived_risks'];
    var scoring_chance = dist_data['striker_score_chance'];
    var scoring_roll = dist_data['striker_score_roll'];

//Striker Kick Choice Variables
    var kicker_foot = 'none';
    var kicker_kick = 'none';

//Scoring Variables
    var score_chance = 0;
    var goal = 1;

//Animation Variables
    var animation_positions = {'Left' : [37, 43],
                               'Middle' : [47,53],
                               'Right' : [57, 63]};
    var bally = 63;
"""

automate_loop_iteration_display = """
txt.data['text'][0] = 'Rounds played: ' + rounds_played;

if (goal == 1){
    txt.data['text'][3] = 'GOAL!';
}
else{
    txt.data['text'][3] = 'Blocked';
}

txt.data['text'][1] = 'Total score: ' + game_score;

txt.change.emit();

DistributionColumnDataSource.change.emit();
"""

automate_loop_roll_kicker_action = """
//Handle Automated Selection
roll = Math.random();

if(roll <= LL_chance){
    kicker_foot = 'Left';
    kicker_kick = 'Left';
}
else if(roll <= LM_chance){
    kicker_foot = 'Left';
    kicker_kick = 'Middle';
}
else if(roll <= LR_chance){
    kicker_foot = 'Left';
    kicker_kick = 'Right';
}
else if(roll <= RL_chance){
    kicker_foot = 'Right';
    kicker_kick = 'Left';
}
else if(roll <= RM_chance){
    kicker_foot = 'Right';
    kicker_kick = 'Middle';
}
else{
    kicker_foot = 'Right';
    kicker_kick = 'Right';
}
"""

run_fictitious_play = """
//Handle Goalie Decision

if(kicker_foot == 'Left'){
    total_sample_rolls = freq[0] + freq[1] + freq[2];
    selected_dict = p['Left'];

    if(total_sample_rolls == 0){
        chance_left = 1/3;
        chance_middle = 1/3;
        chance_right = 1/3;
    }
    else{
        chance_left = freq[0] / total_sample_rolls;
        chance_middle = freq[1] / total_sample_rolls;
        chance_right = freq[2] / total_sample_rolls;
    }
}
else{
    total_sample_rolls = freq[3] + freq[4] + freq[5];
    selected_dict = p['Right'];
    if(total_sample_rolls == 0){
        chance_left = 1/3;
        chance_middle = 1/3;
        chance_right = 1/3;
    }
    else{
        chance_left = freq[3] / total_sample_rolls;
        chance_middle = freq[4] / total_sample_rolls;
        chance_right = freq[5] / total_sample_rolls;
    }
}

danger_goalie_left = (chance_left * selected_dict['LeftLeft']
                      + chance_middle*selected_dict['MiddleLeft']
                      + chance_right*selected_dict['RightLeft']);
danger_goalie_middle = (chance_left * selected_dict['LeftMiddle']
                        + chance_middle*selected_dict['MiddleMiddle']
                        + chance_right*selected_dict['RightMiddle']);
danger_goalie_right = (chance_left * selected_dict['LeftRight']
                       + chance_middle*selected_dict['MiddleRight']
                       + chance_right*selected_dict['RightRight']);


if(danger_goalie_left < danger_goalie_middle){
    if(danger_goalie_left < danger_goalie_right){
        goalie_action = "Left";
    }
    else if(danger_goalie_left == danger_goalie_right){
        roll = Math.random();
        if(roll <= 0.5){
            goalie_action = "Left";
        }
        else{
            goalie_action = "Right";
        }
    }
    else{
        goalie_action = "Right";
    }
}
else if (danger_goalie_left == danger_goalie_middle){
    roll = Math.random();
    if(roll <= 0.5){
        goalie_action = "Left";
    }
    else{
        goalie_action = "Middle";
    }
}
else{
    if(danger_goalie_middle < danger_goalie_right){
        goalie_action = "Middle";
    }
    else if(danger_goalie_middle == danger_goalie_right){
        roll = Math.random();
        if(roll <= 0.5){
            goalie_action = "Middle";
        }
        else{
            goalie_action = "Right";
        }
    }
    else{
        goalie_action = "Right";
    }
}
"""

run_optimal_mixed_strategy = """
roll = Math.random();
if(kicker_foot == 'Left'){
    if(roll <= 0.8){
        goalie_action = "Middle";
    }
    else{
        goalie_action = "Left";
    }
}
else if(kicker_foot == 'Right'){
    if(roll <= 0.7419){
        goalie_action = "Middle";
    }
    else{
        goalie_action = "Right";
    }

}
"""

automate_loop_handle_goalie_decision = """
if(strategy_to_use.text == "Fictitious_Play"){
    """ + run_fictitious_play + """
}
else{
    """ + run_optimal_mixed_strategy + """
}
"""

automate_loop_handle_scoring = """
//Handle Score Chance:

roll = Math.random();
score_chance = p[kicker_foot][kicker_kick+goalie_action];
if(roll <= score_chance){
    goal = 1;
}
else{
    goal = -1;
}
//Display Score Chance:

for(var i=0; i<=5; i++){
    scoring_chance[i] = 0;
    scoring_roll[i] = 0;
}

selected_index = 0;
if(kicker_foot == 'Right'){
    selected_index += 3;
}
if(kicker_kick == 'Middle'){
    selected_index += 1;
}
else if(kicker_kick == 'Right'){
    selected_index += 2;
}

scoring_chance[selected_index] = score_chance;
scoring_roll[selected_index] = roll.toString().substring(0, 8);

// Update text

var rounds_played = (parseInt(nround.text) + 1);
if(rounds_played >= parseInt(iterations_to_run.text)){
    b_auto_next.visible = false;
    game_figure.visible = false;
    automation_distribution_table.visible = false;

    if(strategy_to_use.text == "Fictitious_Play"){
        game_stats_figure_1.visible = true;
        game_stats_figure_2.visible = true;
        game_stats_figure_3.visible = true;
    }
    else{
        game_stats_figure_1.visible = true;
        game_stats_figure_2.visible = true;
        game_stats_figure_3.visible = false;
    }

}
nround.text = rounds_played.toString();

var game_score = parseInt(score.text) + goal;
score.text = game_score.toString();
"""

automate_loop_animation = """
//Animate Scenario:

var animation_roll = 0;
var animation_slot = 0;
animation_roll = Math.random()

if(animation_roll <= 0.5){
    animation_slot = 1;
}

ball.x = animation_positions[kicker_kick][animation_slot];
ball.y = bally;

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
        if(animation_roll <= 0.5){
            animation_slot = 1;
        }
        else{
            animation_slot = 0;
        }
        goalie_head.x = animation_positions[goalie_action][animation_slot];
        goalie_body.x = animation_positions[goalie_action][animation_slot];
    }
}
"""

automate_loop_update_fictitious_decision_tracking = """
//Update Goalie Frequency Tracking:

selected_index = 0;
if(kicker_foot == 'Right'){
    selected_index += 3;
}
if(kicker_kick == 'Middle'){
    selected_index += 1;
}
else if(kicker_kick == 'Right'){
    selected_index += 2;
}

freq[selected_index] += 1;

//Update Goalie Decision Tracking:

selected_index = 0;
if(kicker_foot == 'Right'){
    selected_index += 3;
}
if(goalie_action == 'Middle'){
    selected_index += 1;
}
else if(goalie_action == 'Right'){
    selected_index += 2;
}

decisions[selected_index] += 1;

if(strategy_to_use.text == "Fictitious_Play"){

    //Update Goalie Perceived Risks:

    selected_index = 0;
    if(kicker_foot == 'Right'){
        selected_index += 3;
    }
    for(var i=0; i<=5; i++){
        perceived_risks[i] = 0;
    }
    perceived_risks[selected_index] = danger_goalie_left.toString().substring(0, 8);
    perceived_risks[selected_index + 1] = danger_goalie_middle.toString().substring(0, 8);
    perceived_risks[selected_index + 2] = danger_goalie_right.toString().substring(0, 8);
}
"""

select_bar = """
var selected_bar = 0;

if (kicker_foot == 'Right'){
    selected_bar += 3;
}

if(kicker_kick == 'Middle'){
    selected_bar += 1;
}
else if(kicker_kick == 'Right'){
    selected_bar += 2;
}
"""

update_bar = """
var scored_bar_height = parseInt(scored_texts[selected_bar].text);
scored_bars[selected_bar].height = scored_bar_height;
scored_bars[selected_bar].y = scored_bar_height / 2;

var blockedl_bar_height = parseInt(blockedl_texts[selected_bar].text);
blockedl_bars[selected_bar].height = blockedl_bar_height;
blockedl_bars[selected_bar].y = scored_bar_height + blockedl_bar_height/2;

var blockedm_bar_height = parseInt(blockedm_texts[selected_bar].text);
blockedm_bars[selected_bar].height = blockedm_bar_height;
blockedm_bars[selected_bar].y = scored_bar_height + blockedl_bar_height + blockedm_bar_height/2;

var blockedr_bar_height = parseInt(blockedr_texts[selected_bar].text);
blockedr_bars[selected_bar].height = blockedr_bar_height;
blockedr_bars[selected_bar].y = scored_bar_height + blockedl_bar_height + blockedm_bar_height + blockedr_bar_height/2;
"""

resize_graph = """
var new_graph_height = 0;
for (var i = 0; i <= 5; i++){
    var possible_graph_height = (Math.round((parseInt(scored_texts[i].text)
                                             + parseInt(blockedl_texts[i].text)
                                             + parseInt(blockedm_texts[i].text)
                                             + parseInt(blockedr_texts[i].text))
                                            * 5/4));
    if(possible_graph_height > new_graph_height){
       new_graph_height = possible_graph_height;
    }
    game_stats_figure_1.y_range.end = new_graph_height;
}
"""

update_figure_1_source = """
if(parseInt(nround.text) >= parseInt(iterations_to_run.text)){
    const fig_1_data = game_stats_figure_1_source.data;

    for (var i = 0; i <= 5; i++){
        var scored_y_height = parseInt(scored_texts[i].text);
        var blockedl_height = parseInt(blockedl_texts[i].text) + scored_y_height;
        var blockedm_height = parseInt(blockedm_texts[i].text) + blockedl_height;
        var blockedr_height = parseInt(blockedr_texts[i].text) + blockedm_height;

        fig_1_data['scored_y'][i*3] = scored_y_height;
        fig_1_data['scored_y'][i*3 + 1] = scored_y_height;
        fig_1_data['scored_y'][i*3 + 2] = scored_y_height;

        fig_1_data['blockedl_y'][i*3] = blockedl_height;
        fig_1_data['blockedl_y'][i*3 + 1] = blockedl_height;
        fig_1_data['blockedl_y'][i*3 + 2] = blockedl_height;

        fig_1_data['blockedm_y'][i*3] = blockedm_height;
        fig_1_data['blockedm_y'][i*3 + 1] = blockedm_height;
        fig_1_data['blockedm_y'][i*3 + 2] = blockedm_height;

        fig_1_data['blockedr_y'][i*3] = blockedr_height;
        fig_1_data['blockedr_y'][i*3 + 1] = blockedr_height;
        fig_1_data['blockedr_y'][i*3 + 2] = blockedr_height;
    }

    game_stats_figure_1_source.change.emit();
}
"""

update_game_stats_figure_1 = """
var scored_bars = [ll_scored_bar, lm_scored_bar, lr_scored_bar,
                   rl_scored_bar, rm_scored_bar, rr_scored_bar];
var scored_texts = [ll_scored, lm_scored, lr_scored,
                    rl_scored, rm_scored, rr_scored];

var blockedl_bars = [ll_blocked_left_bar, lm_blocked_left_bar, lr_blocked_left_bar,
                     rl_blocked_left_bar, rm_blocked_left_bar, rr_blocked_left_bar];
var blockedl_texts = [ll_blocked_left, lm_blocked_left, lr_blocked_left,
                      rl_blocked_left, rm_blocked_left, rr_blocked_left];

var blockedm_bars = [ll_blocked_middle_bar, lm_blocked_middle_bar, lr_blocked_middle_bar,
                     rl_blocked_middle_bar, rm_blocked_middle_bar, rr_blocked_middle_bar];
var blockedm_texts = [ll_blocked_middle, lm_blocked_middle, lr_blocked_middle,
                      rl_blocked_middle, rm_blocked_middle, rr_blocked_middle];

var blockedr_bars = [ll_blocked_right_bar, lm_blocked_right_bar, lr_blocked_right_bar,
                     rl_blocked_right_bar, rm_blocked_right_bar, rr_blocked_right_bar];
var blockedr_texts = [ll_blocked_right, lm_blocked_right, lr_blocked_right,
                      rl_blocked_right, rm_blocked_right, rr_blocked_right];
"""+select_bar+"""

if(goal == 1){
    var new_score = parseInt(scored_texts[selected_bar].text);
    new_score += 1;
    scored_texts[selected_bar].text = new_score.toString();
}
else{
    if(goalie_action == 'Left'){
        var new_blockedl = parseInt(blockedl_texts[selected_bar].text);
        new_blockedl += 1;
        blockedl_texts[selected_bar].text = new_blockedl.toString();
    }
    else if(goalie_action == 'Middle'){
        var new_blockedm = parseInt(blockedm_texts[selected_bar].text);
        new_blockedm += 1;
        blockedm_texts[selected_bar].text = new_blockedm.toString();
    }
    else{
        var new_blockedr = parseInt(blockedr_texts[selected_bar].text);
        new_blockedr += 1;
        blockedr_texts[selected_bar].text = new_blockedr.toString();
    }
}

""" + update_bar + resize_graph + update_figure_1_source

update_game_stats_figure_2 = """
const fig_2_data = game_stats_figure_2_source.data;
fig_2_data['ys'][parseInt(nround.text)] = parseInt(score.text);
game_stats_figure_2_source.change.emit();

if(parseInt(nround.text) >= parseInt(iterations_to_run.text)){
    //Resize Graph and Hitboxes:
    var fig_2_min_val = 0;
    var fig_2_max_val = 0;

    for(var i = 0; i <= parseInt(iterations_to_run.text); i++){
        if(fig_2_min_val > fig_2_data['ys'][i]){
            fig_2_min_val = fig_2_data['ys'][i];
        }
        if(fig_2_max_val < fig_2_data['ys'][i]){
            fig_2_max_val = fig_2_data['ys'][i];
        }
    }
    //Resize Hitboxes:
    var heights = [];
    var buffer = Math.round((Math.abs(fig_2_max_val) + Math.abs(fig_2_min_val)) * 1/8) + 1;
    if(Math.abs(fig_2_max_val) > Math.abs(fig_2_min_val)){
        for(var i = 0; i <= parseInt(iterations_to_run.text); i++){
            heights.push(Math.abs((fig_2_max_val + buffer) * 2));
        }
    }
    else{
        for(var i = 0; i <= parseInt(iterations_to_run.text); i++){
            heights.push(Math.abs((fig_2_min_val - buffer) * 2));
        }
    }
    fig_2_data['heights'] = heights;

    //Resize Graph:
    game_stats_figure_2.y_range.end = fig_2_max_val + buffer;
    game_stats_figure_2.y_range.start = fig_2_min_val - buffer;

    game_stats_figure_2_source.change.emit();
}
"""

resize_fig_3_hbs = """
for(var i = 0; i <= parseInt(iterations_to_run.text); i++){
    var perceived_risks = [fig_3_data['ll_ys'][i],
                           fig_3_data['lm_ys'][i],
                           fig_3_data['lr_ys'][i],
                           fig_3_data['rl_ys'][i],
                           fig_3_data['rm_ys'][i],
                           fig_3_data['rr_ys'][i]];

    var sorted_perceived_risks = perceived_risks.sort((a, b) => b - a);
    var hbh1 = (sorted_perceived_risks[5] + sorted_perceived_risks[4]) / 2;
    var hbh2 = (sorted_perceived_risks[4] + sorted_perceived_risks[3])/2 - hbh1;
    var hbh3 = (sorted_perceived_risks[3] + sorted_perceived_risks[2])/2 - hbh2 - hbh1;
    var hbh4 = (sorted_perceived_risks[2] + sorted_perceived_risks[1])/2 - hbh3 - hbh2 - hbh1;
    var hbh5 = (sorted_perceived_risks[1] + sorted_perceived_risks[0])/2 - hbh4 - hbh3 - hbh2 - hbh1;
    var hbh6 = 1 - hbh1 - hbh2 - hbh3 - hbh4 - hbh5;
    fig_3_data['hb1'][i] = hbh1;
    fig_3_data['hb2'][i] = hbh2;
    fig_3_data['hb3'][i] = hbh3;
    fig_3_data['hb4'][i] = hbh4;
    fig_3_data['hb5'][i] = hbh5;
    fig_3_data['hb6'][i] = hbh6;
}
"""

resize_fig_3 = """
var fig_3_min_val = 1;
var fig_3_max_val = 0;
for (var i = 0; i <= parseInt(iterations_to_run.text); i++){
    if(fig_3_data['ll_ys'][i] > fig_3_max_val){ fig_3_max_val = fig_3_data['ll_ys'][i];}
    if(fig_3_data['lm_ys'][i] > fig_3_max_val){ fig_3_max_val = fig_3_data['lm_ys'][i];}
    if(fig_3_data['lr_ys'][i] > fig_3_max_val){ fig_3_max_val = fig_3_data['lr_ys'][i];}
    if(fig_3_data['rl_ys'][i] > fig_3_max_val){ fig_3_max_val = fig_3_data['rl_ys'][i];}
    if(fig_3_data['rm_ys'][i] > fig_3_max_val){ fig_3_max_val = fig_3_data['rm_ys'][i];}
    if(fig_3_data['rr_ys'][i] > fig_3_max_val){ fig_3_max_val = fig_3_data['rr_ys'][i];}

    if(fig_3_data['ll_ys'][i] < fig_3_min_val){ fig_3_min_val = fig_3_data['ll_ys'][i];}
    if(fig_3_data['lm_ys'][i] < fig_3_min_val){ fig_3_min_val = fig_3_data['lm_ys'][i];}
    if(fig_3_data['lr_ys'][i] < fig_3_min_val){ fig_3_min_val = fig_3_data['lr_ys'][i];}
    if(fig_3_data['rl_ys'][i] < fig_3_min_val){ fig_3_min_val = fig_3_data['rl_ys'][i];}
    if(fig_3_data['rm_ys'][i] < fig_3_min_val){ fig_3_min_val = fig_3_data['rm_ys'][i];}
    if(fig_3_data['rr_ys'][i] < fig_3_min_val){ fig_3_min_val = fig_3_data['rr_ys'][i];}
}

fig_3_max_val = Math.round(fig_3_max_val * 10) / 10;
fig_3_min_val = Math.round(fig_3_min_val * 10) / 10;
var fig_3_buffer = 0.1;
game_stats_figure_3.y_range.end = fig_3_max_val + fig_3_buffer;
game_stats_figure_3.y_range.start = fig_3_min_val - fig_3_buffer;
"""

update_game_stats_figure_3 = """
if(strategy_to_use.text == "Fictitious_Play"){

    var fig_3_data = game_stats_figure_3_source.data;
    var index = parseInt(nround.text);

    var freq_ll = DistributionColumnDataSource.data['freq'][0];
    var freq_lm = DistributionColumnDataSource.data['freq'][1];
    var freq_lr = DistributionColumnDataSource.data['freq'][2];
    var freq_rl = DistributionColumnDataSource.data['freq'][3];
    var freq_rm = DistributionColumnDataSource.data['freq'][4];
    var freq_rr = DistributionColumnDataSource.data['freq'][5];
    var chance_l_total = freq_ll + freq_lm + freq_lr;
    var chance_r_total = freq_rl + freq_rm + freq_rr;

    if(chance_l_total != 0){
        var chance_ll = freq_ll / chance_l_total;
        var chance_lm = freq_lm / chance_l_total;
        var chance_lr = freq_lr / chance_l_total;
    }
    else{
        var chance_ll = 1/3;
        var chance_lm = 1/3;
        var chance_lr = 1/3;
    }

    if(chance_r_total != 0){
        var chance_rl = freq_rl / chance_r_total;
        var chance_rm = freq_rm / chance_r_total;
        var chance_rr = freq_rr / chance_r_total;
    }
    else{
        var chance_rl = 1/3;
        var chance_rm = 1/3;
        var chance_rr = 1/3;
    }



    var p = {'Right' : {'LeftLeft' : 0.55,
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

    fig_3_data['ll_ys'][index] = (chance_ll * p['Left']['LeftLeft']
                                  + chance_lm * p['Left']['MiddleLeft']
                                  + chance_lr * p['Left']['RightLeft']);
    fig_3_data['lm_ys'][index] = (chance_ll * p['Left']['LeftMiddle']
                                  + chance_lm * p['Left']['MiddleMiddle']
                                  + chance_lr * p['Left']['RightMiddle']);
    fig_3_data['lr_ys'][index] = (chance_ll * p['Left']['LeftRight']
                                  + chance_lm * p['Left']['MiddleRight']
                                  + chance_lr * p['Left']['RightRight']);
    fig_3_data['rl_ys'][index] = (chance_rl * p['Right']['LeftLeft']
                                  + chance_rm * p['Right']['MiddleLeft']
                                  + chance_rr * p['Right']['RightLeft']);
    fig_3_data['rm_ys'][index] = (chance_rl * p['Right']['LeftMiddle']
                                  + chance_rm * p['Right']['MiddleMiddle']
                                  + chance_rr * p['Right']['RightMiddle']);
    fig_3_data['rr_ys'][index] = (chance_rl * p['Right']['LeftRight']
                                  + chance_rm * p['Right']['MiddleRight']
                                  + chance_rr * p['Right']['RightRight']);

    if(index == parseInt(iterations_to_run.text)){
        """ + resize_fig_3_hbs + resize_fig_3 + """
    }

    game_stats_figure_3_source.change.emit();
}
"""





automate_loop_iteration_main = (automate_loop_roll_kicker_action
                                + automate_loop_handle_goalie_decision
                                + automate_loop_handle_scoring
                                + automate_loop_animation
                                + automate_loop_update_fictitious_decision_tracking
                                + update_game_stats_figure_1
                                + update_game_stats_figure_2
                                + update_game_stats_figure_3)

automate_loop_iteration=(automate_loop_iteration_var_instantiations
                         + automate_loop_iteration_main
                         + automate_loop_iteration_display)

b_automate_start_code = (automate_start_code_initial_gui_display
                         + automate_loop_iteration)
    #</editor-fold>
    #Has Been worked On?: Yes
    #<editor-fold aim_slider_callback Code String:
aim_slider_callback_code = """
//Get the chances array to modify:
const chances = ColumnDataSourceToChange.data['chances'];

//Get the current total of the sliders:
const total = (LL_aim_slider.value + LM_aim_slider.value
               + LR_aim_slider.value + RL_aim_slider.value
               + RM_aim_slider.value + RR_aim_slider.value);

//Set the chances array's values accordingly:
chances[0] = LL_aim_slider.value / total;
chances[1] = LM_aim_slider.value / total;
chances[2] = LR_aim_slider.value / total;
chances[3] = RL_aim_slider.value / total;
chances[4] = RM_aim_slider.value / total;
chances[5] = RR_aim_slider.value / total;

//Emit changes:
ColumnDataSourceToChange.change.emit();
"""
    #</editor-fold>
    #Has Been worked On?: Yes
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

//Initiate arrays to update lengths and values of data in sources:
const array_length = iterations + 1;
let xs_2 = [];
let xs_3 = [];
let ys = new Array(array_length).fill(0);
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
let highlight_alphas = new Array(array_length).fill(0);
let ll_highlight_alphas = new Array(array_length).fill(0);
let lm_highlight_alphas = new Array(array_length).fill(0);
let lr_highlight_alphas = new Array(array_length).fill(0);
let rl_highlight_alphas = new Array(array_length).fill(0);
let rm_highlight_alphas = new Array(array_length).fill(0);
let rr_highlight_alphas = new Array(array_length).fill(0);

//Update previously created arrays with their correct values:
for (let i = 0; i <= iterations; i++){
    xs_2.push(i);
    xs_3.push(i);
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
fig_2_data['heights'] = heights;
fig_2_data['highlight_alphas'] = highlight_alphas;
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
fig_3_data['ll_highlight_alphas'] = ll_highlight_alphas;
fig_3_data['lm_highlight_alphas'] = lm_highlight_alphas;
fig_3_data['lr_highlight_alphas'] = lr_highlight_alphas;
fig_3_data['rl_highlight_alphas'] = rl_highlight_alphas;
fig_3_data['rm_highlight_alphas'] = rm_highlight_alphas;
fig_3_data['rr_highlight_alphas'] = rr_highlight_alphas;
fig_3_data['hb1'] = hb1_ys;
fig_3_data['hb2'] = hb2_ys;
fig_3_data['hb3'] = hb3_ys;
fig_3_data['hb4'] = hb4_ys;
fig_3_data['hb5'] = hb5_ys;
fig_3_data['hb6'] = hb6_ys;
game_stats_figure_3_source.change.emit();
"""
    #</editor-fold>
    #Has Been worked On?: Yes
    #<editor-fold strategy_dropdown_callback Code String:
strategy_dropdown_code = """
//Set the label of the dropdown (the text displayed) to the selected item:
strategy_dropdown.label = this.item;
//Set the text of the strategy_to_use div to the selected item:
strategy_to_use.text = this.item;
//Set the start automate button to be visible:
b_start_automate.visible = true;
"""
    #</editor-fold>
#</editor-fold>

#<editor-fold create_buttons():
#Needs:
#   from bokeh.models import Button
def create_buttons(b_automate_label = "Automate",
                   b_automate_button_type = "success",
                   b_automate_sizing_mode = "scale_width",
                   b_automate_width_policy = "fit",
                   b_automate_disabled = False,
                   b_automate_visibility = True,
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
                   b_auto_next_disabled = False,
                   b_auto_next_visibility = False):

    b_automate = Button(label = b_automate_label,
                        button_type = b_automate_button_type,
                        sizing_mode = b_automate_sizing_mode,
                        width_policy = b_automate_width_policy,
                        disabled = b_automate_disabled,
                        visible = b_automate_visibility)

    b_start_automate = Button(label = b_start_automate_label,
                              button_type = b_start_automate_button_type,
                              sizing_mode = b_start_automate_sizing_mode,
                              width_policy = b_start_automate_width_policy,
                              disabled = b_start_automate_disabled,
                              visible = b_start_automate_visibility)

    b_auto_next = Button(label = b_auto_next_label,
                         button_type = b_auto_next_button_type,
                         sizing_mode = b_auto_next_sizing_mode,
                         width_policy = b_auto_next_width_policy,
                         disabled = b_auto_next_disabled,
                         visible = b_auto_next_visibility)

    return b_automate, b_start_automate, b_auto_next
#</editor-fold>
#<editor-fold create_sliders():
#Needs:
#   from bokeh.models import Slider
def create_sliders(ll_aim_slider_start = 0, ll_aim_slider_end = 1,
                   ll_aim_slider_value = 1/6, ll_aim_slider_step = 0.01,
                   ll_aim_slider_title = "LL Aim Weight",
                   ll_aim_slider_disabled = False,
                   ll_aim_slider_visibility = False,
                   lm_aim_slider_start = 0, lm_aim_slider_end = 1,
                   lm_aim_slider_value = 1/6, lm_aim_slider_step = 0.01,
                   lm_aim_slider_title = "LM Aim Weight",
                   lm_aim_slider_disabled = False,
                   lm_aim_slider_visibility = False,
                   lr_aim_slider_start = 0, lr_aim_slider_end = 1,
                   lr_aim_slider_value = 1/6, lr_aim_slider_step = 0.01,
                   lr_aim_slider_title = "LR Aim Weight",
                   lr_aim_slider_disabled = False,
                   lr_aim_slider_visibility = False,
                   rl_aim_slider_start = 0, rl_aim_slider_end = 1,
                   rl_aim_slider_value = 1/6, rl_aim_slider_step = 0.01,
                   rl_aim_slider_title = "RL Aim Weight",
                   rl_aim_slider_disabled = False,
                   rl_aim_slider_visibility = False,
                   rm_aim_slider_start = 0, rm_aim_slider_end = 1,
                   rm_aim_slider_value = 1/6, rm_aim_slider_step = 0.01,
                   rm_aim_slider_title = "RM Aim Weight",
                   rm_aim_slider_disabled = False,
                   rm_aim_slider_visibility = False,
                   rr_aim_slider_start = 0, rr_aim_slider_end = 1,
                   rr_aim_slider_value = 1/6, rr_aim_slider_step = 0.01,
                   rr_aim_slider_title = "RR Aim Weight",
                   rr_aim_slider_disabled = False,
                   rr_aim_slider_visibility = False,
                   iterations_slider_start = 10, iterations_slider_end = 500,
                   iterations_slider_value = 50,
                   iterations_slider_title = "Iterations To Run",
                   iterations_slider_disabled = False,
                   iterations_slider_visibility = False):

    ll_aim_slider = Slider(start = ll_aim_slider_start,
                           end = ll_aim_slider_end,
                           value = ll_aim_slider_value,
                           step = ll_aim_slider_step,
                           title = ll_aim_slider_title,
                           disabled = ll_aim_slider_disabled,
                           visible = ll_aim_slider_visibility)
    lm_aim_slider = Slider(start = lm_aim_slider_start,
                           end = lm_aim_slider_end,
                           value = lm_aim_slider_value,
                           step = lm_aim_slider_step,
                           title = lm_aim_slider_title,
                           disabled = lm_aim_slider_disabled,
                           visible = lm_aim_slider_visibility)
    lr_aim_slider = Slider(start = lr_aim_slider_start,
                           end = lr_aim_slider_end,
                           value = lr_aim_slider_value,
                           step = lr_aim_slider_step,
                           title = lr_aim_slider_title,
                           disabled = lr_aim_slider_disabled,
                           visible = lr_aim_slider_visibility)
    rl_aim_slider = Slider(start = rl_aim_slider_start,
                           end = rl_aim_slider_end,
                           value = rl_aim_slider_value,
                           step = rl_aim_slider_step,
                           title = rl_aim_slider_title,
                           disabled = rl_aim_slider_disabled,
                           visible = rl_aim_slider_visibility)
    rm_aim_slider = Slider(start = rm_aim_slider_start,
                           end = rm_aim_slider_end,
                           value = rm_aim_slider_value,
                           step = rm_aim_slider_step,
                           title = rm_aim_slider_title,
                           disabled = rm_aim_slider_disabled,
                           visible = rm_aim_slider_visibility)
    rr_aim_slider = Slider(start = rr_aim_slider_start,
                           end = rr_aim_slider_end,
                           value = rr_aim_slider_value,
                           step = rr_aim_slider_step,
                           title = rr_aim_slider_title,
                           disabled = rr_aim_slider_disabled,
                           visible = rr_aim_slider_visibility)

    iterations_slider = Slider(start = iterations_slider_start,
                               end = iterations_slider_end,
                               value = iterations_slider_value, step = 1,
                               title = iterations_slider_title,
                               disabled = iterations_slider_disabled,
                               visible = iterations_slider_visibility)

    return (ll_aim_slider, lm_aim_slider, lr_aim_slider,
            rl_aim_slider, rm_aim_slider, rr_aim_slider,
            iterations_slider)
#</editor-fold>
#<editor-fold create_gamestate_divs():
#Needs:
#   from bokeh.models.widgets import Div
def create_gamestate_divs(iterations_to_run_start_text = "50",
                          iterations_to_run_visibility = False,
                          strategy_to_use_start_text = "Not Set",
                          strategy_to_use_visibility = False,
                          ll_scored_start_text = "0",
                          lm_scored_start_text = "0",
                          lr_scored_start_text = "0",
                          rl_scored_start_text = "0",
                          rm_scored_start_text = "0",
                          rr_scored_start_text = "0",
                          ll_scored_visibility = False,
                          lm_scored_visibility = False,
                          lr_scored_visibility = False,
                          rl_scored_visibility = False,
                          rm_scored_visibility = False,
                          rr_scored_visibility = False,
                          ll_blocked_left_start_text = "0",
                          lm_blocked_left_start_text = "0",
                          lr_blocked_left_start_text = "0",
                          rl_blocked_left_start_text = "0",
                          rm_blocked_left_start_text = "0",
                          rr_blocked_left_start_text = "0",
                          ll_blocked_left_visibility = False,
                          lm_blocked_left_visibility = False,
                          lr_blocked_left_visibility = False,
                          rl_blocked_left_visibility = False,
                          rm_blocked_left_visibility = False,
                          rr_blocked_left_visibility = False,
                          ll_blocked_middle_start_text = "0",
                          lm_blocked_middle_start_text = "0",
                          lr_blocked_middle_start_text = "0",
                          rl_blocked_middle_start_text = "0",
                          rm_blocked_middle_start_text = "0",
                          rr_blocked_middle_start_text = "0",
                          ll_blocked_middle_visibility = False,
                          lm_blocked_middle_visibility = False,
                          lr_blocked_middle_visibility = False,
                          rl_blocked_middle_visibility = False,
                          rm_blocked_middle_visibility = False,
                          rr_blocked_middle_visibility = False,
                          ll_blocked_right_start_text = "0",
                          lm_blocked_right_start_text = "0",
                          lr_blocked_right_start_text = "0",
                          rl_blocked_right_start_text = "0",
                          rm_blocked_right_start_text = "0",
                          rr_blocked_right_start_text = "0",
                          ll_blocked_right_visibility = False,
                          lm_blocked_right_visibility = False,
                          lr_blocked_right_visibility = False,
                          rl_blocked_right_visibility = False,
                          rm_blocked_right_visibility = False,
                          rr_blocked_right_visibility = False):

    iterations_to_run = Div(text = iterations_to_run_start_text,
                            visible = iterations_to_run_visibility)

    strategy_to_use = Div(text = strategy_to_use_start_text,
                          visible = strategy_to_use_visibility)

    ll_scored = Div(text = ll_scored_start_text,
                    visible = ll_scored_visibility)
    lm_scored = Div(text = lm_scored_start_text,
                    visible = lm_scored_visibility)
    lr_scored = Div(text = lr_scored_start_text,
                    visible = lr_scored_visibility)
    rl_scored = Div(text = rl_scored_start_text,
                    visible = rl_scored_visibility)
    rm_scored = Div(text = rm_scored_start_text,
                    visible = rm_scored_visibility)
    rr_scored = Div(text = rr_scored_start_text,
                    visible = rr_scored_visibility)

    ll_blocked_left = Div(text = ll_blocked_left_start_text,
                          visible = ll_blocked_left_visibility)
    lm_blocked_left = Div(text = lm_blocked_left_start_text,
                          visible = lm_blocked_left_visibility)
    lr_blocked_left = Div(text = lr_blocked_left_start_text,
                          visible = lr_blocked_left_visibility)
    rl_blocked_left = Div(text = rl_blocked_left_start_text,
                          visible = rl_blocked_left_visibility)
    rm_blocked_left = Div(text = rm_blocked_left_start_text,
                          visible = rm_blocked_left_visibility)
    rr_blocked_left = Div(text = rr_blocked_left_start_text,
                          visible = rr_blocked_left_visibility)

    ll_blocked_middle = Div(text = ll_blocked_middle_start_text,
                            visible = ll_blocked_middle_visibility)
    lm_blocked_middle = Div(text = lm_blocked_middle_start_text,
                            visible = lm_blocked_middle_visibility)
    lr_blocked_middle = Div(text = lr_blocked_middle_start_text,
                            visible = lr_blocked_middle_visibility)
    rl_blocked_middle = Div(text = rl_blocked_middle_start_text,
                            visible = rl_blocked_middle_visibility)
    rm_blocked_middle = Div(text = rm_blocked_middle_start_text,
                            visible = rm_blocked_middle_visibility)
    rr_blocked_middle = Div(text = rr_blocked_middle_start_text,
                            visible = rr_blocked_middle_visibility)

    ll_blocked_right = Div(text = ll_blocked_right_start_text,
                           visible = ll_blocked_right_visibility)
    lm_blocked_right = Div(text = lm_blocked_right_start_text,
                           visible = lm_blocked_right_visibility)
    lr_blocked_right = Div(text = lr_blocked_right_start_text,
                           visible = lr_blocked_right_visibility)
    rl_blocked_right = Div(text = rl_blocked_right_start_text,
                           visible = rl_blocked_right_visibility)
    rm_blocked_right = Div(text = rm_blocked_right_start_text,
                           visible = rm_blocked_right_visibility)
    rr_blocked_right = Div(text = rr_blocked_right_start_text,
                           visible = rr_blocked_right_visibility)

    return (iterations_to_run, strategy_to_use,
            ll_scored, lm_scored, lr_scored,
            rl_scored, rm_scored, rr_scored,
            ll_blocked_left, lm_blocked_left, lr_blocked_left,
            rl_blocked_left, rm_blocked_left, rr_blocked_left,
            ll_blocked_middle, lm_blocked_middle, lr_blocked_middle,
            rl_blocked_middle, rm_blocked_middle, rr_blocked_middle,
            ll_blocked_right, lm_blocked_right, lr_blocked_right,
            rl_blocked_right, rm_blocked_right, rr_blocked_right)
#</editor-fold>
#<editor-fold create_strategy_dropdown():
def create_strategy_dropdown(fictitious_play_text = "Fictitious_Play",
                             mixed_strategy_text = "Mixed_Strategy",
                             dropdown_label = "CPU strategy to Use",
                             dropdown_button_type = "warning",
                             dropdown_disabled = False,
                             dropdown_visibility = False):
    #CPU Strategy to Use Dropdown:
    menu = [(fictitious_play_text, fictitious_play_text),
            (mixed_strategy_text, mixed_strategy_text)]
    strategy_dropdown = Dropdown(label = dropdown_label, menu = menu,
                                 button_type = dropdown_button_type,
                                 disabled = dropdown_disabled,
                                 visible = dropdown_visibility)
    return strategy_dropdown
#</editor-fold>
#<editor-fold create_distribution_table_source():
#Needs:
#   from bokeh.models import ColumnDataSource
def create_distribution_table_source(footedness_left_text = "Left",
                                     footedness_right_text = "Right",
                                     aim_direction_left_text = "Left",
                                     aim_direction_middle_text = "Middle",
                                     aim_direction_right_text = "Right"):
    #Make Automation Distribution Tracking Table:
    distribution_data = dict(footedness = [footedness_left_text,
                                           footedness_left_text,
                                           footedness_left_text,
                                           footedness_right_text,
                                           footedness_right_text,
                                           footedness_right_text],
                             aim_direction = [aim_direction_left_text,
                                              aim_direction_middle_text,
                                              aim_direction_right_text,
                                              aim_direction_left_text,
                                              aim_direction_middle_text,
                                              aim_direction_right_text],
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
def create_distribution_table(source,
                              footedness_column_title = "Striker Footedness",
                              footedness_column_width = 101,
                              aim_direction_column_title = "Striker Aim Direction",
                              aim_direction_column_width = 107,
                              freq_column_title = "Frequency",
                              freq_column_width = 60,
                              decisions_column_title = "Goalie Decisions",
                              decisions_column_width = 90,
                              perceived_risks_column_title = "Goalie Perceived Risks",
                              perceived_risks_column_width = 130,
                              score_chance_column_title = "Striker's Score Chance",
                              score_chance_column_width = 120,
                              score_roll_column_title = "Striker's Score Roll",
                              score_roll_column_width = 103,
                              table_width = 711,
                              table_height = 280,
                              table_autosize_mode = "force_fit",
                              table_sizing_mode = "scale_width",
                              table_visibility = False,
                              table_fit_columns = False):

    footedness_column = TableColumn(field = "footedness",
                                    title = footedness_column_title,
                                    width = footedness_column_width)
    aim_direction_column = TableColumn(field = "aim_direction",
                                       title = aim_direction_column_title,
                                       width = aim_direction_column_width)
    freq_column = TableColumn(field = "freq",
                              title = freq_column_title,
                              width = freq_column_width)
    decisions_column = TableColumn(field = "decisions",
                                   title = decisions_column_title,
                                   width = decisions_column_width)
    perceived_risks_column =  TableColumn(field = "goalie_perceived_risks",
                                          title = perceived_risks_column_title,
                                          width = perceived_risks_column_width)
    score_chance_column = TableColumn(field = "striker_score_chance",
                                      title = score_chance_column_title,
                                      width = score_chance_column_width)
    score_roll_column = TableColumn(field = "striker_score_roll",
                                    title = score_roll_column_title,
                                    width = score_roll_column_width)
    distribution_columns = [footedness_column, aim_direction_column,
                            freq_column, decisions_column,
                            perceived_risks_column, score_chance_column,
                            score_roll_column]

    automation_distribution_table = DataTable(source = source,
                                              columns = distribution_columns,
                                              width = table_width,
                                              height = table_height,
                                              autosize_mode = table_autosize_mode,
                                              sizing_mode = table_sizing_mode,
                                              visible = table_visibility,
                                              fit_columns = table_fit_columns)
    return automation_distribution_table
#</editor-fold>
#<editor-fold create_automation_table_source():
#Needs:
#   from bokeh.models import ColumnDataSource
def create_automation_table_source(ll_base_chance = 1/6,
                                   lm_base_chance = 1/6,
                                   lr_base_chance = 1/6,
                                   rl_base_chance = 1/6,
                                   rm_base_chance = 1/6,
                                   rr_base_chance = 1/6,
                                   footedness_left_text = "Left",
                                   footedness_right_text = "Right",
                                   aim_direction_left_text = "Left",
                                   aim_direction_middle_text = "Middle",
                                   aim_direction_right_text = "Right"):

    data = dict(footedness = [footedness_left_text, footedness_left_text,
                              footedness_left_text, footedness_right_text,
                              footedness_right_text, footedness_right_text],
                aim_direction = [aim_direction_left_text,
                                 aim_direction_middle_text,
                                 aim_direction_right_text,
                                 aim_direction_left_text,
                                 aim_direction_middle_text,
                                 aim_direction_right_text],
                chances = [ll_base_chance, lm_base_chance, lr_base_chance,
                           rl_base_chance, rm_base_chance, rr_base_chance])

    automation_table_source = ColumnDataSource(data)
    return automation_table_source
#</editor-fold>
#<editor-fold create_automation_table():
#Needs:
#   from bokeh.models import TableColumn, DataTable
def create_automation_table(source,
                            footedness_column_title = "Striker Footedness",
                            aim_direction_column_title = "Striker Aim Direction",
                            chances_column_title = "Chance", table_width = 600,
                            table_height = 280,
                            table_autosize_mode = "force_fit",
                            table_visibility = False):

    footedness_column = TableColumn(field = "footedness",
                                    title = footedness_column_title)
    aim_direction_column = TableColumn(field = "aim_direction",
                                       title = aim_direction_column_title)
    chances_column = TableColumn(field = "chances",
                                 title = chances_column_title)

    columns = [footedness_column, aim_direction_column, chances_column]

    automation_table = DataTable(source = source, columns = columns,
                                 width = table_width, height = table_height,
                                 autosize_mode = table_autosize_mode,
                                 visible = table_visibility)
    return automation_table
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
#<editor-fold aim_sliders_setup():
#Needs:
#   from bokeh.models import CustomJS
def aim_sliders_setup(ll_aim_slider, lm_aim_slider, lr_aim_slider,
                      rl_aim_slider, rm_aim_slider, rr_aim_slider,
                      automation_table_source):

    args_dict = dict(ColumnDataSourceToChange = automation_table_source,
                     LL_aim_slider = ll_aim_slider,
                     LM_aim_slider = lm_aim_slider,
                     LR_aim_slider = lr_aim_slider,
                     RL_aim_slider = rl_aim_slider,
                     RM_aim_slider = rm_aim_slider,
                     RR_aim_slider = rr_aim_slider)

    aim_slider_customjs = CustomJS(args = args_dict,
                                   code = aim_slider_callback_code)

    ll_aim_slider.js_on_change('value', aim_slider_customjs)
    lm_aim_slider.js_on_change('value', aim_slider_customjs)
    lr_aim_slider.js_on_change('value', aim_slider_customjs)
    rl_aim_slider.js_on_change('value', aim_slider_customjs)
    rm_aim_slider.js_on_change('value', aim_slider_customjs)
    rr_aim_slider.js_on_change('value', aim_slider_customjs)
#</editor-fold>
#<editor-fold iterations_slider_setup():
#Needs:
#   from bokeh.models import CustomJS
def iterations_slider_setup(iterations_slider, args_dict):
    iterations_slider_callback = CustomJS(args = args_dict,
                                          code = iterations_slider_code)

    iterations_slider.js_on_change('value', iterations_slider_callback)
#</editor-fold>
#<editor-fold strategy_dropdown_setup():
#Needs:
#   from bokeh.models import CustomJS
def strategy_dropdown_setup(strategy_dropdown, args_dict):
    strategy_dropdown_callback = CustomJS(args = args_dict,
                                          code = strategy_dropdown_code)
    strategy_dropdown.js_on_event("menu_item_click",
                                  strategy_dropdown_callback)
#</editor-fold>
