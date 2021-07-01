from bokeh.models import Button, CustomJS

#<editor-fold Callback Code String:
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

#<editor-fold create():
def create(game_parts, label = "Automate", button_type = "success",
           sizing_mode = "scale_width", width_policy = "fit",
           disabled = False, visible = True):
    b_automate = Button(label = label, button_type = button_type,
                        sizing_mode = sizing_mode, width_policy = width_policy,
                        disabled = disabled, visible = visible)
    game_parts.buttons['b_automate'] = b_automate
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    args_dict = dict(b_automate = game_parts.buttons['b_automate'],
                     iterations_slider = game_parts.sliders['iterations_slider'],
                     strategy_dropdown = game_parts.dropdowns['strategy_dropdown'],
                     automation_table = game_parts.tables['automation_table'],
                     txt = game_parts.texts['scr_text'],
                     ll_aim_text_input = game_parts.textinputs['ll_aim_text_input'],
                     lm_aim_text_input = game_parts.textinputs['lm_aim_text_input'],
                     lr_aim_text_input = game_parts.textinputs['lr_aim_text_input'],
                     rl_aim_text_input = game_parts.textinputs['rl_aim_text_input'],
                     rm_aim_text_input = game_parts.textinputs['rm_aim_text_input'],
                     rr_aim_text_input = game_parts.textinputs['rr_aim_text_input'])
    b_automate_click = CustomJS(args = args_dict,
                                code = b_automate_code)
    game_parts.buttons['b_automate'].js_on_click(b_automate_click)
#</editor-fold>
