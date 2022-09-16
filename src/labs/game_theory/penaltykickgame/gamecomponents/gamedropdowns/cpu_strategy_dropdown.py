from bokeh.models import Dropdown, CustomJS

#<editor-fold strategy_dropdown on change callback Code String:
# Code for handling selections on the cpu strategy dropdown. Updates the
# dropdown label to indicate the choice before updateing the divs being used to
# track the keeper strategy, its selection status, and the need to make a counter
# strategy. Finally, it hides the tip about selecting a strategy.
stratDropdownOnChange = """
//Set the label of the dropdown (the text displayed) to the selected item:
stratDropdown.label = this.item;

//Set the text of the strategy_to_use div to the selected item:
stratToUseDiv.text = this.item;

//Sets the aim sliders to be visible:
aimTextInputs.forEach(
  (v) => v.visible = true
)

//Sets cpuSelectedDiv to indicate that a cpu strat has been selected:
cpuSelectedDiv.text = '1';

//update the tracking div for needing a goalie cheats counter:
counterMadeDiv.text = ((this.item === 'Goalie_Cheats') ? '0' : '1');

//Hides the select a cpu strategy tip:
selectCpuTip.visible = false;
"""
#</editor-fold>

#<editor-fold create():
def create(game_parts, config):
    dropdown = Dropdown(
        label=config.label, menu=config.items, button_type=config.button_type,
        disabled=config.disabled, visible=config.visible
    )
    game_parts.dropdowns["cpu_strategy"] = dropdown
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    text_inputs = game_parts.textinputs
    divs = game_parts.divs
    dropdowns = game_parts.dropdowns
    aim_text_inputs = [
        text_inputs["ll_aim"], text_inputs["lm_aim"], text_inputs["lr_aim"],
        text_inputs["rl_aim"], text_inputs["rm_aim"], text_inputs["rr_aim"]
    ]

    args_dict = {
        "stratDropdown" : dropdowns["cpu_strategy"],
        "stratToUseDiv" : divs["strategy_to_use"],
        "aimTextInputs" : aim_text_inputs,
        "cpuSelectedDiv" : divs["cpu_selected"],
        "counterMadeDiv" : divs["counter_made"],
        "selectCpuTip" : divs["select_cpu_tip"]
    }

    strat_dropdown_change = CustomJS(args=args_dict, code=stratDropdownOnChange)
    dropdowns["cpu_strategy"].js_on_event(
        "menu_item_click", strat_dropdown_change
    )
#</editor-fold>
