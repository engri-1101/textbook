from bokeh.models.widgets import Div
from bokeh.models import CustomJS

#<editor-fold cpu_selected_change_code:
cpu_selected_change_code = """
if(parseInt(cpu_selected.text) == 1){
    if(parseInt(chances_valid.text) == 1){
        if(parseInt(counter_made.text) == 1){
            b_start_automate.visible = true;
        }
        else{
            b_start_automate.visible = false;
        }
    }
    else{
        b_start_automate.visible = false;
    }
}
else{
    b_start_automate.visible = false;
}
if(parseInt(counter_made.text) != 1){
    if(parseInt(chances_valid.text) == 1){
        b_make_counter.visible = true;
    }
    else{
        b_make_counter.visible = false;
    }
}
else{
    b_make_counter.visible = false;
}
"""
#</editor-fold>

#<editor-fold create():
def create(game_parts):
    cpu_selected = Div(text = "0", visible = False)
    game_parts.divs['cpu_selected'] = cpu_selected
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    args_dict = dict(b_start_automate = game_parts.buttons['b_start_automate'],
                     b_make_counter = game_parts.buttons['b_make_counter'],
                     cpu_selected = game_parts.divs['cpu_selected'],
                     counter_made = game_parts.divs['counter_made'],
                     chances_valid = game_parts.divs['chances_valid'])
    game_parts.divs['cpu_selected'].js_on_change('text',
                                                 CustomJS(code = cpu_selected_change_code,
                                                          args = args_dict))
#</editor-fold>
