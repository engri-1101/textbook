from bokeh.models import Button, CustomJS

#<editor-fold Callback Code String:
b_automate_code = """
//Change visibilities of game items:
b_automate.visible = false;
b_auto_advance.visible = true;
auto_advance_speed_slider.visible = true;
ll_aim_text_input.visible = true;
lm_aim_text_input.visible = true;
lr_aim_text_input.visible = true;
rl_aim_text_input.visible = true;
rm_aim_text_input.visible = true;
rr_aim_text_input.visible = true;
iterations_slider.visible = true;
strategy_dropdown.visible = true;
automation_table.visible = true;
chances_ne_1_tip.visible = true;
select_cpu_tip.visible = true;
"""
#</editor-fold>

#<editor-fold create():
def create(game_parts, config):
    b_automate = Button(label = config.label, button_type = config.button_type,
                        sizing_mode = config.sizing_mode,
                        width_policy = config.width_policy,
                        disabled = config.disabled,
                        visible = config.visible)
    game_parts.buttons['automate'] = b_automate
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    args_dict = dict(b_automate = game_parts.buttons['automate'],
                     b_auto_advance = game_parts.buttons['auto_advance'],
                     iterations_slider = game_parts.sliders['iterations'],
                     strategy_dropdown = game_parts.dropdowns['cpu_strategy'],
                     automation_table = game_parts.tables['automation'],
                     txt = game_parts.texts['scr_text'],
                     ll_aim_text_input = game_parts.textinputs['ll_aim'],
                     lm_aim_text_input = game_parts.textinputs['lm_aim'],
                     lr_aim_text_input = game_parts.textinputs['lr_aim'],
                     rl_aim_text_input = game_parts.textinputs['rl_aim'],
                     rm_aim_text_input = game_parts.textinputs['rm_aim'],
                     rr_aim_text_input = game_parts.textinputs['rr_aim'],
                     chances_ne_1_tip = game_parts.divs['chances_ne_1_tip'],
                     select_cpu_tip = game_parts.divs['select_cpu_tip'],
                     auto_advance_speed_slider = game_parts.sliders['auto_advance_speed'])
    b_automate_click = CustomJS(args = args_dict,
                                code = b_automate_code)
    game_parts.buttons['automate'].js_on_click(b_automate_click)
#</editor-fold>
