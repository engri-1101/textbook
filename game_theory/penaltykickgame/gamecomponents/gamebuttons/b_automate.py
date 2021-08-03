from bokeh.models import Button, CustomJS

#<editor-fold Callback Code String:
def createAutomateCode(
    CPU_strategy, allow_fast_forward, force_fast_forward,
    force_fast_forward_spd, iterations_to_run,
):
    code = """
//Change visibilities of game items:
automateButton.visible = false;
aimTextInputs.forEach(
  (v) => v.visible = true
)
automationTable.visible = true;
chancesNE1Tip.visible = true;
"""
    if (CPU_strategy == None):
        code += """
strategyDropdown.visible = true;
selectCpuTip.visible = true;
"""

    if (allow_fast_forward == True):
        if (force_fast_forward == False):
            code += """
autoAdvButton.visible = true;
"""
        else:
            code += """
autoAdvButton.active = true;
autoAdvButton.visible = false;
"""

        if (force_fast_forward_spd != None):
            code += """
advSpdSlider.value = """ + str(force_fast_forward_spd) + """;
advSpdSlider.visible = false;
"""
        else:
            code += """
advSpdSlider.visible =  true;
"""

    if (iterations_to_run != None):
        code += """
iterationsSlider.value = """ + str(iterations_to_run) + """;
iterationsSlider.visible = false;
"""
    else:
        code += """
iterationsSlider.visible = true;
"""

    return code
#</editor-fold>

#<editor-fold create():
def create(game_parts, config):
    button = Button(
        label=config.label, button_type=config.button_type,
        sizing_mode=config.sizing_mode, width_policy=config.width_policy,
        disabled=config.disabled, visible=config.visible
    )
    game_parts.buttons["automate"] = button
#</editor-fold>

#<editor-fold setup():
def setup(
    game_parts, CPU_strategy, allow_fast_forward, force_fast_forward,
    force_fast_forward_spd, iterations_to_run
):
    buttons = game_parts.buttons
    sliders = game_parts.sliders
    divs = game_parts.divs
    text_inputs = game_parts.textinputs
    b_automate = buttons["automate"]
    aim_text_inputs = [
        text_inputs["ll_aim"], text_inputs["lm_aim"], text_inputs["lr_aim"],
        text_inputs["rl_aim"], text_inputs["rm_aim"], text_inputs["rr_aim"]
    ]
    args_dict = dict(
        automateButton = b_automate,
        autoAdvButton = buttons["auto_advance"],
        iterationsSlider = sliders["iterations"],
        strategyDropdown = game_parts.dropdowns["cpu_strategy"],
        automationTable = game_parts.tables["automation"],
        aimTextInputs = aim_text_inputs,
        chancesNE1Tip = divs["chances_ne_1_tip"],
        selectCpuTip = divs["select_cpu_tip"],
        advSpdSlider = sliders["auto_advance_speed"]
    )
    automateCode = createAutomateCode(
        CPU_strategy, allow_fast_forward, force_fast_forward,
        force_fast_forward_spd, iterations_to_run
    )
    b_automate_click = CustomJS(args=args_dict, code=automateCode)
    b_automate.js_on_click(b_automate_click)
#</editor-fold>
