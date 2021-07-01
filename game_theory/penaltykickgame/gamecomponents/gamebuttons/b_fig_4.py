from bokeh.models import Button, CustomJS

#<editor-fold b_fig_4 callback Code String:
b_fig_4_click_code = """
b_fig_1.disabled = false;
b_fig_2.disabled = false;
b_fig_3.disabled = false;
b_fig_4.disabled = true;
stats_fig_1.visible = false;
stats_fig_2.visible = false;
stats_fig_3.visible = false;
stats_fig_4.visible = true;
"""
#</editor-fold>

#<editor-fold create():
def create(game_parts, label = "Figure 4", button_type = "success",
           sizing_mode = "scale_width", width_policy = "fit",
           disabled = False, visible = False):
    b_fig_4 = Button(label = label, button_type = button_type,
                        sizing_mode = sizing_mode, width_policy = width_policy,
                        disabled = disabled, visible = visible)
    game_parts.buttons['fig_4'] = b_fig_4
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    args_dict = dict(b_fig_1 = game_parts.buttons['fig_1'],
                     b_fig_2 = game_parts.buttons['fig_2'],
                     b_fig_3 = game_parts.buttons['fig_3'],
                     b_fig_4 = game_parts.buttons['fig_4'],
                     stats_fig_1 = game_parts.figures['stats_1'],
                     stats_fig_2 = game_parts.figures['stats_2'],
                     stats_fig_3 = game_parts.figures['stats_3'],
                     stats_fig_4 = game_parts.figures['stats_4'])
    b_fig_4_click = CustomJS(args = args_dict,
                             code = b_fig_4_click_code)
    game_parts.buttons['fig_4'].js_on_click(b_fig_4_click)
#</editor-fold>
