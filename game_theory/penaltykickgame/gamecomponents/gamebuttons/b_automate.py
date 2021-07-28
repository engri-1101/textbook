from bokeh.models import Button, CustomJS

#<editor-fold Callback Code String:
automateCode = """
//Change visibilities of game items:
automateButton.visible = false;
autoAdvButton.visible = true;
advSpdSlider.visible = true;
llAimTextInput.visible = true;
lmAimTextInput.visible = true;
lrAimTextInput.visible = true;
rlAimTextInput.visible = true;
rmAimTextInput.visible = true;
rrAimTextInput.visible = true;
iterationsSlider.visible = true;
strategyDropdown.visible = true;
automationTable.visible = true;
chancesNE1Tip.visible = true;
selectCpuTip.visible = true;
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
    args_dict = dict(automateButton = game_parts.buttons['automate'],
                     autoAdvButton = game_parts.buttons['auto_advance'],
                     iterationsSlider = game_parts.sliders['iterations'],
                     strategyDropdown = game_parts.dropdowns['cpu_strategy'],
                     automationTable = game_parts.tables['automation'],
                     llAimTextInput = game_parts.textinputs['ll_aim'],
                     lmAimTextInput = game_parts.textinputs['lm_aim'],
                     lrAimTextInput = game_parts.textinputs['lr_aim'],
                     rlAimTextInput = game_parts.textinputs['rl_aim'],
                     rmAimTextInput = game_parts.textinputs['rm_aim'],
                     rrAimTextInput = game_parts.textinputs['rr_aim'],
                     chancesNE1Tip = game_parts.divs['chances_ne_1_tip'],
                     selectCpuTip = game_parts.divs['select_cpu_tip'],
                     advSpdSlider = game_parts.sliders['auto_advance_speed'])
    b_automate_click = CustomJS(args = args_dict,
                                code = automateCode)
    game_parts.buttons['automate'].js_on_click(b_automate_click)
#</editor-fold>
