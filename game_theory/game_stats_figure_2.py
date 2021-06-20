from bokeh.plotting import figure
from bokeh.models import (CustomJSHover, ColumnDataSource, HoverTool)

#<editor-fold Custom JSHover fig_2_xs Code String:
fig_2_xs_code = """
var index = special_vars.index;

for(var i = 0;
    i < game_stats_figure_2_source.data['highlight_alphas'].length;
    i++){
    game_stats_figure_2_source.data['highlight_alphas'][i] = 0;
}
game_stats_figure_2_source.data['highlight_alphas'][index] = 1;
game_stats_figure_2_source.change.emit();

return(game_stats_figure_2_source.data['xs'][index].toString())
"""
#</editor-fold>
#<editor-fold Custom JSHover fig_2_ys Code String:
fig_2_ys_code = """
var index = special_vars.index;

return(game_stats_figure_2_source.data['ys'][index].toString())
"""
#</editor-fold>
#<editor-fold Custom HoverTool Tooltip Code String:
fig_2_custom_tooltip = """
<div>
    <span style='font-size: 10px;'>Iteration:</span>
    <span style='font-size: 10px;'>@xs{custom}</span>
</div>
<div @hovershow{custom}>
    <span style='font-size: 10px;'>Score:</span>
    <span style='font-size: 10px;'>@ys{custom}</span>
</div>
"""
#</editor-fold>

def stats_figure_2_setup(figure_base_tools = "box_zoom, wheel_zoom, pan",
                         figure_toolbar_location = "below",
                         figure_toolbar_sticky = False,
                         figure_title = 'Score Over Iterations',
                         figure_width = 300, figure_height = 240,
                         figure_x_range = (0, 50), figure_y_range = (-50, 50),
                         figure_initial_visibility = False,
                         figure_title_font_size = '8pt',
                         figure_x_axis_visibility = True,
                         figure_y_axis_visibility = True,
                         figure_xgrid_line_color = None,
                         figure_ygrid_line_color = None,
                         figure_outline_line_color = None,
                         figure_background_color = "white",
                         plot_dot_size = 5, plot_dot_outline_color = "#B56464",
                         plot_dot_color = "#CE7D7D",
                         plot_highlight_dot_size = 10,
                         plot_highlight_dot_outline_color = "#6464B5",
                         plot_highlight_dot_color = "#7D7DCE"):
    #<editor-fold Figure Creation:
    game_stats_figure_2 = figure(tools = figure_base_tools,
                                 toolbar_location = figure_toolbar_location,
                                 toolbar_sticky = figure_toolbar_sticky,
                                 title = figure_title,
                                 plot_width = figure_width,
                                 plot_height = figure_height,
                                 x_range = figure_x_range,
                                 y_range = figure_y_range,
                                 visible = figure_initial_visibility)
    game_stats_figure_2.title.text_font_size = figure_title_font_size
    game_stats_figure_2.xaxis.visible = figure_x_axis_visibility
    game_stats_figure_2.yaxis.visible = figure_y_axis_visibility
    game_stats_figure_2.xgrid.grid_line_color = figure_xgrid_line_color
    game_stats_figure_2.ygrid.grid_line_color = figure_ygrid_line_color
    game_stats_figure_2.outline_line_color = figure_outline_line_color
    game_stats_figure_2.background_fill_color = figure_background_color
    #</editor-fold>
    #<editor-fold ColumnDataSource Creation:
    source_xs = []
    source_ys = []
    source_heights = []
    source_highlight_alphas = []
    #Fill the Lists
    for i in range(51):
        source_xs.append(i)
        source_ys.append(0)
        source_heights.append(100)
        source_highlight_alphas.append(0)
    source_data = dict(xs = source_xs,
                       ys = source_ys,
                       heights = source_heights,
                       highlight_alphas = source_highlight_alphas)
    game_stats_figure_2_source = ColumnDataSource(data = source_data)
    #</editor-fold>
    #<editor-fold Plot Figure Points:
    game_stats_figure_2.circle_dot('xs', 'ys',
                                   source = game_stats_figure_2_source,
                                   size = plot_dot_size,
                                   color = plot_dot_outline_color,
                                   fill_color = plot_dot_color)
    #</editor-fold>
    #<editor-fold Plot Figure Highlight Points:
    game_stats_figure_2.circle_dot('xs', 'ys',
                                   source = game_stats_figure_2_source,
                                   size = plot_highlight_dot_size,
                                   color = plot_highlight_dot_outline_color,
                                   fill_color = plot_highlight_dot_color,
                                   alpha = 'highlight_alphas')
    #</editor-fold>
    #<editor-fold Plot Invisible Hitboxes:
    game_stats_figure_2.rect(x = 'xs', y = 0,
                             source = game_stats_figure_2_source,
                             width = 1, height = 'heights',
                             fill_color = plot_dot_color, alpha = 0)
    #</editor-fold>
    #<editor-fold CustomJSHover Creation:
    hover_args = dict(game_stats_figure_2_source = game_stats_figure_2_source)
    fig_2_xs_custom = CustomJSHover(code = fig_2_xs_code, args = hover_args)
    fig_2_ys_custom = CustomJSHover(code = fig_2_ys_code, args = hover_args)
    #</editor-fold>
    #<editor-fold Create HoverTool:
    hover_formatter = { '@xs' : fig_2_xs_custom,
                        '@ys' : fig_2_ys_custom}
    game_stats_figure_2.add_tools(HoverTool(tooltips = fig_2_custom_tooltip,
                                            formatters = hover_formatter,
                                            mode = "mouse",
                                            point_policy = "follow_mouse"))
    #</editor-fold>
    return (game_stats_figure_2, game_stats_figure_2_source)
