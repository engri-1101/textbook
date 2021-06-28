from bokeh.plotting import figure
from bokeh.models import (CustomJSHover, ColumnDataSource, HoverTool)

class Stats_fig_4_configs:
    """Objects of this class are used to organize and pass parameters to
    Stats Figure 2. All arguments are mutable, and default values for them are
    the currently decided values being used to make the game. The main purpose
    of the configurability provided through the use of this class is to make it
    easier to test changes. Any changes that improve the game should be made
    directly to the default values of the arguments in this class after
    successful testing.
    """
    def __init__(self, figure_base_tools = "",
                 figure_toolbar_location = "below",
                 figure_toolbar_sticky = False,
                 figure_title = 'Score Chance Over Iterations',
                 figure_width = 600, figure_height = 360,
                 figure_x_range = (1, 50), figure_y_range = (0, 1),
                 figure_initial_visibility = False,
                 figure_title_font_size = '16pt',
                 figure_x_axis_visibility = True,
                 figure_y_axis_visibility = True,
                 figure_xgrid_line_color = None,
                 figure_ygrid_line_color = None,
                 figure_outline_line_color = None,
                 figure_background_color = "white"):
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

def stats_figure_4_setup(fig_configs):
    game_stats_figure_4 = figure(tools = fig_configs.figure_base_tools,
                                 toolbar_location = fig_configs.figure_toolbar_location,
                                 toolbar_sticky = fig_configs.figure_toolbar_sticky,
                                 title = fig_configs.figure_title,
                                 plot_width = fig_configs.figure_width,
                                 plot_height = fig_configs.figure_height,
                                 x_range = fig_configs.figure_x_range,
                                 y_range = fig_configs.figure_y_range,
                                 visible = fig_configs.figure_initial_visibility)
    game_stats_figure_4.title.text_font_size = fig_configs.figure_title_font_size
    game_stats_figure_4.xaxis.visible = fig_configs.figure_x_axis_visibility
    game_stats_figure_4.yaxis.visible = fig_configs.figure_y_axis_visibility
    game_stats_figure_4.xgrid.grid_line_color = fig_configs.figure_xgrid_line_color
    game_stats_figure_4.ygrid.grid_line_color = fig_configs.figure_ygrid_line_color
    game_stats_figure_4.outline_line_color = fig_configs.figure_outline_line_color
    game_stats_figure_4.background_fill_color = fig_configs.figure_background_color

    #Create initial values for game_stats_figure_2_source
    source_xs = []
    source_ys = []
    #Fill the Lists
    for i in range(51):
        source_xs.append(i)
        source_ys.append(0)

    #Create game_stats_figure_2_source with the values that were created.
    source_data = dict(xs = source_xs,
                       ys = source_ys)

    game_stats_figure_4_source = ColumnDataSource(data = source_data)

    game_stats_figure_4.line('xs', 'ys', source = game_stats_figure_4_source,
                             line_color = "black")
    return game_stats_figure_4, game_stats_figure_4_source
