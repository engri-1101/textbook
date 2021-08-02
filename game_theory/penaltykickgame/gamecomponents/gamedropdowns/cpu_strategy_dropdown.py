from bokeh.models import Dropdown, CustomJS

#<editor-fold strategy_dropdown_callback Code String:
stratDropdownOnChange= """
//Set the label of the dropdown (the text displayed) to the selected item:
stratDropdown.label = this.item;

//Set the text of the strategy_to_use div to the selected item:
stratToUseDiv.text = this.item;

//Sets the aim sliders to be visible:
aimTextInputs.forEach(
  (v) => v.visible = true
)

//Sets the automation_table to be visible:
automationTable.visible = true;

//Sets cpuSelectedDiv to indicate that a cpu strat has been selected:
cpuSelectedDiv.text = '1';

//Checks whether the selected item is Goalie_Cheats:
const counterNeeded = (this.item === 'Goalie_Cheats');

//update the tracking div for needing a goalie cheats counter:
counterMadeDiv.text = ((counterNeeded) ? '0' : '1');

//Hides the select a cpu strategy tip:
selectCpuTip.visible = false;
"""
#</editor-fold>

#<editor-fold create():
#Needs:
#    from bokeh.models import DropDown
def create(game_parts, config):
    strategy_dropdown = Dropdown(
        label = config.label, menu = config.items,
        button_type = config.button_type, disabled = config.disabled,
        visible = config.visible
    )
    game_parts.dropdowns['cpu_strategy'] = strategy_dropdown
#</editor-fold>

#<editor-fold setup():
#Needs:
#    from bokeh.models import CustomJS
def setup(game_parts):
    aimTextInputs = [game_parts.textinputs['ll_aim'],
                     game_parts.textinputs['lm_aim'],
                     game_parts.textinputs['lr_aim'],
                     game_parts.textinputs['rl_aim'],
                     game_parts.textinputs['rm_aim'],
                     game_parts.textinputs['rr_aim']]
    args_dict = dict(
        stratDropdown = game_parts.dropdowns['cpu_strategy'],
        stratToUseDiv = game_parts.divs['strategy_to_use'],
        aimTextInputs = aimTextInputs,
        automationTable = game_parts.tables['automation'],
        cpuSelectedDiv = game_parts.divs['cpu_selected'],
        makeCounterButton = game_parts.buttons['make_counter'],
        counterMadeDiv = game_parts.divs['counter_made'],
        selectCpuTip = game_parts.divs['select_cpu_tip']
    )

    stratDropdownChange = CustomJS(
        args = args_dict, code = stratDropdownOnChange
    )
    game_parts.dropdowns['cpu_strategy'].js_on_event(
        "menu_item_click", stratDropdownChange
    )
#</editor-fold>
