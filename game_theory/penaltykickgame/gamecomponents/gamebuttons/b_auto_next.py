from bokeh.models import Button, CustomJS

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
const chances = chances_source.data['chances'];
const dist_data = distribution_source.data;
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
    const counter_chances_l = counter_source.data['chances_l'];
    const counter_chances_r = counter_source.data['chances_r'];
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

    stats_fig_4_source.data['ys'][rounds_played] = score_chance;
    stats_fig_4_source.data['feet'][rounds_played] = kicker_foot;
    stats_fig_4_source.data['directions'][rounds_played] = kicker_kick;
    stats_fig_4_source.data['actions'][rounds_played] = goalie_action;
    stats_fig_4_source.change.emit()

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
        distribution_table.visible = false;
        stats_fig_4_source.data['xs'].shift();
        stats_fig_4_source.data['ys'].shift();
        stats_fig_4_source.data['feet'].shift();
        stats_fig_4_source.data['directions'].shift();
        stats_fig_4_source.data['actions'].shift();
        stats_fig_4_source.data['highlight_alphas'].shift();
        stats_fig_4_source.data['avgs_placeholder'].shift();
        stats_fig_4_source.change.emit();
        stats_fig_4.x_range.start -= 0.5;
        stats_fig_4.x_range.end += 0.5;
        if(strategy_to_use.text == "Fictitious_Play"){
            stats_fig_1.visible = true;
            stats_fig_2.visible = false;
            stats_fig_3.visible = false;
            stats_fig_4.visible = false;
            b_fig_1.visible = true;
            b_fig_2.visible = true;
            b_fig_3.visible = true;
            b_fig_4.visible = true;
        }
        else{
            stats_fig_1.visible = true;
            stats_fig_2.visible = false;
            stats_fig_3.visible = false;
            stats_fig_4.visible = false;
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
    distribution_source.change.emit();
}

goalieFictitiousDecisionTracking();
"""
#</editor-fold>
        #<editor-fold update_game_stats_figure_1
update_game_stats_figure_1 = """

function updateFig1(){
    const fig_1_data = stats_fig_1_source.data;
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
    stats_fig_1_source.change.emit();

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
        stats_fig_1.y_range.end = grid_max;
    }
}
updateFig1();
"""
#</editor-fold>
        #<editor-fold update_game_stats_figure_2
update_game_stats_figure_2 = """
function updateFig2(){
    const fig_2_data = stats_fig_2_source.data;

    let nround_val = parseInt(nround.text);

    fig_2_data['ys'][nround_val] = parseInt(score.text);
    fig_2_data['chance_ys'][nround_val] = fig_2_data['chance_ys'][nround_val - 1] + (2 * scored_chance - 1);
    stats_fig_2_source.change.emit();

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
        stats_fig_2.y_range.end = fig_2_max_val + buffer;
        stats_fig_2.y_range.start = fig_2_min_val - buffer;
        stats_fig_2.x_range.start -= 0.5;
        stats_fig_2.x_range.end += 0.5;

        stats_fig_2_source.change.emit();
    }
}
updateFig2();
"""
#</editor-fold>
        #<editor-fold update_game_stats_figure_3
update_game_stats_figure_3 = """
function updateFig3(){

    let fig_3_data = stats_fig_3_source.data;
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
        stats_fig_3.y_range.end = Math.min(fig_3_max_val + fig_3_buffer,
                                                   1);
        stats_fig_3.y_range.start = fig_3_min_val - fig_3_buffer;
        stats_fig_3.x_range.start -= 0.5;
        stats_fig_3.x_range.end += 0.5;
    }

    stats_fig_3_source.change.emit();
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
#</editor-fold>

#<editor-fold create():
def create(game_parts, label = "Next", button_type = "success",
           sizing_mode = "scale_width", width_policy = "fit",
           disabled = False, visible = False):
    b_auto_next = Button(label = label, button_type = button_type,
                        sizing_mode = sizing_mode, width_policy = width_policy,
                        disabled = disabled, visible = visible)
    game_parts.buttons['next'] = b_auto_next
#</editor-fold>

#<editor-fold setup():
#Needs:
#   from bokeh.models import CustomJS
def setup(game_parts):
    args_dict =  dict(chances_source = game_parts.sources['automation_table'],
                      distribution_source = game_parts.sources['distribution_table'],
                      strategy_to_use = game_parts.divs['strategy_to_use'],
                      nround = game_parts.divs['nround'],
                      iterations_to_run = game_parts.divs['iterations_to_run'],
                      txt = game_parts.texts['scr_text'],
                      b_auto_next = game_parts.buttons['next'],
                      game_figure = game_parts.figures['game_figure'],
                      distribution_table = game_parts.tables['distribution'],
                      goalie_head = game_parts.glyphs['goalie_head'],
                      goalie_body = game_parts.glyphs['goalie_body'],
                      counter_source = game_parts.sources['goalie_counter'],
                      ball = game_parts.glyphs['ball'],
                      score = game_parts.divs['score'],
                      b_fig_1 = game_parts.buttons['fig_1'],
                      b_fig_2 = game_parts.buttons['fig_2'],
                      b_fig_3 = game_parts.buttons['fig_3'],
                      b_fig_4 = game_parts.buttons['fig_4'],
                      stats_fig_1 = game_parts.figures['stats_1'],
                      stats_fig_2 = game_parts.figures['stats_2'],
                      stats_fig_3 = game_parts.figures['stats_3'],
                      stats_fig_4 = game_parts.figures['stats_4'],
                      stats_fig_1_source = game_parts.sources['stats_fig_1'],
                      stats_fig_2_source = game_parts.sources['stats_fig_2'],
                      stats_fig_3_source = game_parts.sources['stats_fig_3'],
                      stats_fig_4_source = game_parts.sources['stats_fig_4'])
    b_auto_next_click = CustomJS(args = args_dict,
                                 code = automate_loop_iteration)
    game_parts.buttons['next'].js_on_click(b_auto_next_click)
#</editor-fold>
