from bokeh.models import Button, ColumnDataSource, CustomJS

#<editor-fold Callback Code String:
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
goalie_counter_source.data['leftStrat'][0] = goalie_ll_coeff;
goalie_counter_source.data['leftStrat'][1] = goalie_lm_coeff;
goalie_counter_source.data['leftStrat'][2] = goalie_lr_coeff;
goalie_counter_source.data['rightStrat'][0] = goalie_rl_coeff;
goalie_counter_source.data['rightStrat'][1] = goalie_rm_coeff;
goalie_counter_source.data['rightStrat'][2] = goalie_rr_coeff;

goalie_counter_source.change.emit();

b_make_counter.visible = false;

counter_made.text = "1";
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
    goalie_counter_source = ColumnDataSource(data = dict(leftStrat = [1, 0, 0],
                                                         rightStrat = [1, 0, 0]))
    game_parts.sources['goalie_counter'] = goalie_counter_source

    args_dict = dict(b_start_automate = game_parts.buttons['start'],
                     b_make_counter = game_parts.buttons['make_counter'],
                     automation_table = game_parts.tables['automation'],
                     automation_table_source = game_parts.sources['automation_table'],
                     counter_made = game_parts.divs['counter_made'],
                     goalie_counter_source = game_parts.sources['goalie_counter'],
                     ll_aim_text_input = game_parts.textinputs['ll_aim'],
                     lm_aim_text_input = game_parts.textinputs['lm_aim'],
                     lr_aim_text_input = game_parts.textinputs['lr_aim'],
                     rl_aim_text_input = game_parts.textinputs['rl_aim'],
                     rm_aim_text_input = game_parts.textinputs['rm_aim'],
                     rr_aim_text_input = game_parts.textinputs['rr_aim'])

    b_make_counter_click = CustomJS(args = args_dict,
                                    code = b_make_counter_click_code)
    game_parts.buttons['make_counter'].js_on_click(b_make_counter_click)
#</editor-fold>
