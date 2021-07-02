from bokeh.models import Dropdown, CustomJS

#<editor-fold strategy_dropdown_callback Code String:
strategy_dropdown_code = """
//Set the label of the dropdown (the text displayed) to the selected item:
strategy_dropdown.label = this.item;

//Set the text of the strategy_to_use div to the selected item:
strategy_to_use.text = this.item;

//Sets the aim sliders to be visible:
ll_aim_text_input.visible = true;
lm_aim_text_input.visible = true;
lr_aim_text_input.visible = true;
rl_aim_text_input.visible = true;
rm_aim_text_input.visible = true;
rr_aim_text_input.visible = true;

//Sets the automation_table to be visible:
automation_table.visible = true;

//Toggles button visibilities based off selected item:
if(this.item != "Goalie_Cheats"){
b_make_counter.visible = false;
counter_made.text = "1";
cpu_selected.text = "1";
}
else{
counter_made.text = "0";
cpu_selected.text = "1";
}
"""
#</editor-fold>

#<editor-fold create():
#Needs:
#    from bokeh.models import DropDown
def create(game_parts, config):
    strategy_dropdown = Dropdown(label = config.label, menu = config.items,
                                 button_type = config.button_type,
                                 disabled = config.disabled,
                                 visible = config.visible)
    game_parts.dropdowns['cpu_strategy'] = strategy_dropdown
#</editor-fold>

#<editor-fold setup():
#Needs:
#    from bokeh.models import CustomJS
def setup(game_parts):
    args_dict = dict(strategy_dropdown = game_parts.dropdowns['cpu_strategy'],
                     strategy_to_use = game_parts.divs['strategy_to_use'],
                     b_start_automate = game_parts.buttons['start'],
                     b_make_counter = game_parts.buttons['make_counter'],
                     automation_table = game_parts.tables['automation'],
                     cpu_selected = game_parts.divs['cpu_selected'],
                     counter_made = game_parts.divs['counter_made'],
                     ll_aim_text_input = game_parts.textinputs['ll_aim'],
                     lm_aim_text_input = game_parts.textinputs['lm_aim'],
                     lr_aim_text_input = game_parts.textinputs['lr_aim'],
                     rl_aim_text_input = game_parts.textinputs['rl_aim'],
                     rm_aim_text_input = game_parts.textinputs['rm_aim'],
                     rr_aim_text_input = game_parts.textinputs['rr_aim'])

    strategy_dropdown_callback = CustomJS(args = args_dict,
                                          code = strategy_dropdown_code)
    game_parts.dropdowns['cpu_strategy'].js_on_event("menu_item_click",
                                                          strategy_dropdown_callback)
#</editor-fold>
