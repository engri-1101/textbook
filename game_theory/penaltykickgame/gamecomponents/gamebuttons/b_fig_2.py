from bokeh.models import Button, CustomJS

#<editor-fold b_fig_2 callback Code String:
b_fig_2_click_code = """
b_fig_1.disabled = false;
b_fig_2.disabled = true;
b_fig_3.disabled = false;
b_fig_4.disabled = false;
game_stats_figure_1.visible = false;
game_stats_figure_2.visible = true;
game_stats_figure_3.visible = false;
game_stats_figure_4.visible = false;
"""
#</editor-fold>

#<editor-fold create():
def create(game_parts, label = "Figure 2", button_type = "success",
           sizing_mode = "scale_width", width_policy = "fit",
           disabled = False, visible = False):
    b_fig_2 = Button(label = label, button_type = button_type,
                        sizing_mode = sizing_mode, width_policy = width_policy,
                        disabled = disabled, visible = visible)
    game_parts.buttons['fig_2'] = b_fig_2
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    args_dict = dict(b_fig_1 = game_parts.buttons['fig_1'],
                     b_fig_2 = game_parts.buttons['fig_2'],
                     b_fig_3 = game_parts.buttons['fig_3'],
                     b_fig_4 = game_parts.buttons['fig_4'],
                     game_stats_figure_1 = game_parts.figures['stats_1'],
                     game_stats_figure_2 = game_parts.figures['stats_2'],
                     game_stats_figure_3 = game_parts.figures['stats_3'],
                     game_stats_figure_4 = game_parts.figures['stats_4'])
    b_fig_2_click = CustomJS(args = args_dict,
                             code = b_fig_2_click_code)
    game_parts.buttons['fig_2'].js_on_click(b_fig_2_click)
#</editor-fold>
