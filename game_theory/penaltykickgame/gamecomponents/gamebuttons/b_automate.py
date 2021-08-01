from bokeh.models import Button, CustomJS

#<editor-fold Callback Code String:
def createAutomateCode(CPU_strategy, allow_fast_forward):
    code = """
//Change visibilities of game items:
automateButton.visible = false;
llAimTextInput.visible = true;
lmAimTextInput.visible = true;
lrAimTextInput.visible = true;
rlAimTextInput.visible = true;
rmAimTextInput.visible = true;
rrAimTextInput.visible = true;
iterationsSlider.visible = true;
automationTable.visible = true;
chancesNE1Tip.visible = true;
    """
    if(CPU_strategy == None):
        code += """
strategyDropdown.visible = true;
selectCpuTip.visible = true;
        """
    if(allow_fast_forward == True):
        code += """
    autoAdvButton.visible = true;
    advSpdSlider.visible = true;
        """
    return code
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
def setup(game_parts, CPU_strategy, allow_fast_forward):
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
    automateCode = createAutomateCode(CPU_strategy, allow_fast_forward)
    b_automate_click = CustomJS(args = args_dict,
                                code = automateCode)
    game_parts.buttons['automate'].js_on_click(b_automate_click)
#</editor-fold>
