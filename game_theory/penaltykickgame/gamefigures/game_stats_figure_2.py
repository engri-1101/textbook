from bokeh.plotting import figure
from bokeh.models import (CustomJSHover, ColumnDataSource, HoverTool)

#<editor-fold Custom JSHover fig_2_xs Code String:
#Returns the iteration number and makes the necessary changes for highlighting
#the hovered data point.
fig_2_xs_code = """
const index = special_vars.index;
const data = game_stats_figure_2_source.data;

data['highlight_alphas'] = new Array(data['highlight_alphas'].length).fill(0);
data['highlight_alphas'][index] = 1;
game_stats_figure_2_source.change.emit();

return(data['xs'][index].toString());
"""
#</editor-fold>
#<editor-fold Custom JSHover fig_2_ys Code String:
#Returns the y value of the hovered data point.
fig_2_ys_code = """
return(game_stats_figure_2_source.data['ys'][special_vars.index].toString());
"""
#</editor-fold>
#<editor-fold Custom HoverTool Tooltip Code String:
#Code below is for how the custom HoverTool displays the information.
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

#<editor-fold Stats_fig_2_configs:
class Stats_fig_2_configs:
    """Objects of this class are used to organize and pass parameters to
    Stats Figure 2. All arguments are mutable, and default values for them are
    the currently decided values being used to make the game. The main purpose
    of the configurability provided through the use of this class is to make it
    easier to test changes. Any changes that improve the game should be made
    directly to the default values of the arguments in this class after
    successful testing.
    """
    def __init__(self, figure_base_tools = "box_zoom, wheel_zoom, pan",
                 figure_toolbar_location = "below",
                 figure_toolbar_sticky = False,
                 figure_title = 'Score Over Iterations',
                 figure_width = 600, figure_height = 360,
                 figure_x_range = (0, 50), figure_y_range = (-50, 50),
                 figure_initial_visibility = False,
                 figure_title_font_size = '16pt',
                 figure_x_axis_visibility = True,
                 figure_y_axis_visibility = True,
                 figure_xgrid_line_color = None,
                 figure_ygrid_line_color = None,
                 figure_outline_line_color = None,
                 figure_background_color = "white",
                 plot_dot_size = 5, plot_dot_outline_color = "#B56464",
                 plot_dot_color = "#CE7D7D", plot_highlight_dot_size = 10,
                 plot_highlight_dot_outline_color = "#6464B5",
                 plot_highlight_dot_color = "#7D7DCE"):
        #<editor-fold figure:
        self.figure_base_tools = figure_base_tools
        self.figure_toolbar_location = figure_toolbar_location
        self.figure_toolbar_sticky = figure_toolbar_sticky
        self.figure_title = figure_title
        self.figure_width = figure_width
        self.figure_height = figure_height
        self.figure_x_range = figure_x_range
        self.figure_y_range = figure_y_range
        self.figure_initial_visibility = figure_initial_visibility
        self.figure_title_font_size = figure_title_font_size
        self.figure_x_axis_visibility = figure_x_axis_visibility
        self.figure_y_axis_visibility = figure_y_axis_visibility
        self.figure_xgrid_line_color = figure_xgrid_line_color
        self.figure_ygrid_line_color = figure_ygrid_line_color
        self.figure_outline_line_color = figure_outline_line_color
        self.figure_background_color = figure_background_color
        #</editor-fold>
        #<editor-fold plot:
        self.plot_dot_size = plot_dot_size
        self.plot_dot_outline_color = plot_dot_outline_color
        self.plot_dot_color = plot_dot_color
        self.plot_highlight_dot_size = plot_highlight_dot_size
        self.plot_highlight_dot_outline_color = plot_highlight_dot_outline_color
        self.plot_highlight_dot_color = plot_highlight_dot_color
        #</editor-fold>
#</editor-fold>

#<editor-fold stats_figure_2_setup:
def stats_figure_2_setup(fig_configs, game_parts):
    """Fully creates and sets up Stats Figure 2 for use in the main game. Stats
    Figure 2 displays the player's score over the iterations played.


    Keyword Argument:

    fig_configs - An oject of type Stats_fig_2_configs containing the user's
    desired figure values within its attributes.


    Returns:

    game_stats_figure_2 - The Game stats Bokeh figure displaying the data.

    game_stats_figure_2_source - The ColumnDataSource used by
    game_stats_figure_2.
    """
    #<editor-fold Figure Creation:
    #Create and configure the main aspects of the figure:
    game_stats_figure_2 = figure(tools = fig_configs.figure_base_tools,
                                 toolbar_location = fig_configs.figure_toolbar_location,
                                 toolbar_sticky = fig_configs.figure_toolbar_sticky,
                                 title = fig_configs.figure_title,
                                 plot_width = fig_configs.figure_width,
                                 plot_height = fig_configs.figure_height,
                                 x_range = fig_configs.figure_x_range,
                                 y_range = fig_configs.figure_y_range,
                                 visible = fig_configs.figure_initial_visibility)
    game_stats_figure_2.title.text_font_size = fig_configs.figure_title_font_size
    game_stats_figure_2.xaxis.visible = fig_configs.figure_x_axis_visibility
    game_stats_figure_2.yaxis.visible = fig_configs.figure_y_axis_visibility
    game_stats_figure_2.xgrid.grid_line_color = fig_configs.figure_xgrid_line_color
    game_stats_figure_2.ygrid.grid_line_color = fig_configs.figure_ygrid_line_color
    game_stats_figure_2.outline_line_color = fig_configs.figure_outline_line_color
    game_stats_figure_2.background_fill_color = fig_configs.figure_background_color
    #</editor-fold>
    #<editor-fold ColumnDataSource Creation:
    #Create initial values for game_stats_figure_2_source
    source_xs = []
    source_ys = []
    source_chance_ys = []
    source_heights = []
    source_highlight_alphas = []
    #Fill the Lists
    for i in range(51):
        source_xs.append(i)
        source_ys.append(0)
        source_chance_ys.append(0)
        source_heights.append(100)
        source_highlight_alphas.append(0)

    #Create game_stats_figure_2_source with the values that were created.
    source_data = dict(xs = source_xs,
                       ys = source_ys,
                       chance_ys = source_chance_ys,
                       heights = source_heights,
                       highlight_alphas = source_highlight_alphas)
    game_stats_figure_2_source = ColumnDataSource(data = source_data)
    #</editor-fold>
    #<editor-fold Plot Figure Points:
    #Create the data points for the figure.
    game_stats_figure_2.circle_dot('xs', 'ys',
                                   source = game_stats_figure_2_source,
                                   size = fig_configs.plot_dot_size,
                                   line_color = fig_configs.plot_dot_outline_color,
                                   fill_color = fig_configs.plot_dot_color)
    game_stats_figure_2.circle_dot('xs', 'chance_ys',
                                   source = game_stats_figure_2_source,
                                   size = 1,
                                   line_color = "black",
                                   fill_color = "black")
    #</editor-fold>
    #<editor-fold Plot Figure Highlight Points:
    #Plot Highlight Points For Figure:
    game_stats_figure_2.circle_dot('xs', 'ys',
                                   source = game_stats_figure_2_source,
                                   size = fig_configs.plot_highlight_dot_size,
                                   line_color = fig_configs.plot_highlight_dot_outline_color,
                                   fill_color = fig_configs.plot_highlight_dot_color,
                                   alpha = 'highlight_alphas')
    #</editor-fold>
    #<editor-fold Plot Invisible Hitboxes:
    #Create the invisible hitboxes for the figure:
    hbs = game_stats_figure_2.rect(x = 'xs', y = 0,
                                   source = game_stats_figure_2_source,
                                   width = 1, height = 'heights',
                                   fill_color = fig_configs.plot_dot_color,
                                   alpha = 0)
    #</editor-fold>
    #<editor-fold CustomJSHover Creation:
    #Create the CustomJSHovers used to format the data for the figure's
    #custom HoverTool:
    hover_args = dict(game_stats_figure_2_source = game_stats_figure_2_source)
    fig_2_xs_custom = CustomJSHover(code = fig_2_xs_code, args = hover_args)
    fig_2_ys_custom = CustomJSHover(code = fig_2_ys_code, args = hover_args)
    #</editor-fold>
    #<editor-fold Create HoverTool:
    #Create the Custom HoverTool and add it to the figure:
    hover_formatter = { '@xs' : fig_2_xs_custom,
                        '@ys' : fig_2_ys_custom}
    game_stats_figure_2.add_tools(HoverTool(tooltips = fig_2_custom_tooltip,
                                            formatters = hover_formatter,
                                            mode = "mouse",
                                            point_policy = "follow_mouse",
                                            renderers = [hbs]))
    #</editor-fold>
    game_parts.figures['stats_2'] = game_stats_figure_2
    game_parts.sources['stats_fig_2'] = game_stats_figure_2_source
#</editor-fold>
