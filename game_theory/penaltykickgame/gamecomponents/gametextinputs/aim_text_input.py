from bokeh.models import TextInput, CustomJS

JS_FLOAT_BUFFER = "0.0000001" # THIS VARIABLE SHOULD BE TREATED AS A CONSTANT.
# JAVASCRIPT HAS SOME ISSUES WITH FLOATS, SO CHECKING FOR EQUALITY BETWEEN
# NUMBERS AND THE SUMS (OR OTHER OPERATIONS) OF OTHER NUMBERS IS NOT SAFE.
# IN ORDER TO WORK AROUND THIS ISSUE, INSTEAD OF CHECKING FOR EQUALITY, CHECK
# THAT THE VALUE IS WITHIN A RANGE OF THE EXPECTED OUTCOME.

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

#<editor-fold create():
def create(game_parts, name, config):
    aim_text_input = TextInput(value = config.value,
                               title = name + config.title_addition,
                               visible = config.visible)
    game_parts.textinputs[name + '_aim'] = aim_text_input
#</editor-fold>

#<editor-fold aim_textInputs_setup():
#Needs:
#    from bokeh.models import CustomJS
def setup(name, game_parts):
    args_dict = dict(table_source = game_parts.sources['automation_table'],
                     ll_aim_text_input = game_parts.textinputs['ll_aim'],
                     lm_aim_text_input = game_parts.textinputs['lm_aim'],
                     lr_aim_text_input = game_parts.textinputs['lr_aim'],
                     rl_aim_text_input = game_parts.textinputs['rl_aim'],
                     rm_aim_text_input = game_parts.textinputs['rm_aim'],
                     rr_aim_text_input = game_parts.textinputs['rr_aim'],
                     chances_valid = game_parts.divs['chances_valid'],
                     b_start_automate = game_parts.buttons['start']
    )
    aim_textInputs_customjs = CustomJS(args = args_dict,
                                       code = aim_inputs_callback_code)

    game_parts.textinputs[name + '_aim'].js_on_change('value',
                                                      aim_textInputs_customjs)
#</editor-fold>
