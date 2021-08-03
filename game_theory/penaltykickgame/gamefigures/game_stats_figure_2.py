# from bokeh.plotting import figure
from bokeh.models import (CustomJSHover, ColumnDataSource, HoverTool)
from . import figure_creation as fig_creation
#<editor-fold Custom JSHover xs Code String:
#Returns the iteration number and makes the necessary changes for highlighting
#the hovered data point.
xsCode = """
const index = special_vars.index;
const data = src.data;

data['highlight_alphas'].fill(0);
data['highlight_alphas'][index] = 1;
src.change.emit();

return(data['xs'][index].toString());
"""
#</editor-fold>

#<editor-fold Custom JSHover ys Code String:
#Returns the y value of the hovered data point.
ysCode = """
const val = src.data['ys'][special_vars.index];
return val.toString();
"""
#</editor-fold>

#<editor-fold Custom HoverTool Tooltip Code String:
#Code below is for how the custom HoverTool displays the information.
custom_tooltip = """
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

#<editor-fold Stats fig 2 configs:
class Configs:
    """Objects of this class are used to organize and pass parameters to
    Stats Figure 2. All arguments are mutable, and default values for them are
    the currently decided values being used to make the game. The main purpose
    of the configurability provided through the use of this class is to make it
    easier to test changes. Any changes that improve the game should be made
    directly to the default values of the arguments in this class after
    successful testing.
    """
    def __init__(
        self, fig_base_tools="", fig_toolbar_loc="below",
        fig_toolbar_sticky=False, fig_title='Score Over Iterations',
        fig_width=600, fig_height=360, fig_x_range=(-0.5, 50.5),
        fig_y_range=(-50, 50), fig_visibility=False,
        fig_sizing_mode="stretch_both", fig_outline_line_color=None,
        fig_background_color="white", fig_title_font_size='16pt',
        fig_x_axis_visibility=True, fig_y_axis_visibility=True,
        fig_x_axis_line_color="black", fig_y_axis_line_color="black",
        fig_xgrid_visibility=False, fig_ygrid_visibility=False,
        fig_xgrid_line_color="black", fig_ygrid_line_color="black",
        plot_dot_size=5, plot_dot_outline_color="#B56464",
        plot_dot_color="#CE7D7D", plot_highlight_dot_size=10,
        plot_highlight_dot_outline_color="#6464B5",
        plot_highlight_dot_color="#7D7DCE"
    ):
        #<editor-fold figure:
        self.fig = fig_creation.FigureConfigs(
            base_tools=fig_base_tools, toolbar_loc=fig_toolbar_loc,
            toolbar_sticky=fig_toolbar_sticky, title=fig_title, width=fig_width,
            height=fig_height, x_range=fig_x_range, y_range=fig_y_range,
            visibility=fig_visibility, sizing_mode=fig_sizing_mode,
            outline_line_color=fig_outline_line_color,
            background_color=fig_background_color,
            title_font_size=fig_title_font_size,
            x_axis_visibility=fig_x_axis_visibility,
            y_axis_visibility=fig_y_axis_visibility,
            x_axis_line_color=fig_x_axis_line_color,
            y_axis_line_color=fig_y_axis_line_color,
            x_grid_visibility=fig_xgrid_visibility,
            y_grid_visibility=fig_ygrid_visibility,
            x_grid_line_color=fig_xgrid_line_color,
            y_grid_line_color=fig_ygrid_line_color
        )
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
def create(game_parts, configs=Configs()):
    """Fully creates and sets up Stats Figure 2 for use in the main game. Stats
    Figure 2 displays the player's score over the iterations played.


    Keyword Argument:

    configs - An oject of type Configs containing the user's
    desired figure values within its attributes.
    """

    fig = fig_creation.make_fig(configs.fig)

    #<editor-fold ColumnDataSource Creation:
    #Create initial values for stats_fig_2_source
    src_xs = []
    for i in range(51):
        src_xs.append(i)
    #Create stats_fig_2_source with the values that were created.
    src_data = dict(
        xs = src_xs,
        ys = [0] * 51,
        chance_ys = [0] * 51,
        heights = [100] * 51,
        highlight_alphas = [0] * 51
    )

    fig_src = ColumnDataSource(data=src_data)
    #</editor-fold>

    #<editor-fold Plot Figure ElementsL
    fig.circle_dot(
        x="xs", y="ys", source=fig_src, size=configs.plot_dot_size,
        line_color=configs.plot_dot_outline_color,
        fill_color=configs.plot_dot_color
    )
    fig.circle_dot(
        x="xs", y="chance_ys", source=fig_src, size=1, line_color="black",
        fill_color="black"
    )
    fig.circle_dot(
        x="xs", y="ys", source=fig_src, size=configs.plot_highlight_dot_size,
        line_color=configs.plot_highlight_dot_outline_color,
        fill_color=configs.plot_highlight_dot_color, alpha="highlight_alphas"
    )
    hbs = fig.rect(
        x="xs", y=0, source=fig_src, width=1, height="heights", alpha=0,
        fill_color=configs.plot_dot_color
    )
    #</editor-fold>

    #<editor-fold CustomJSHover Creation:
    #Create the CustomJSHovers used to format the data for the figure's
    #custom HoverTool:
    hover_args = dict(src = fig_src)
    xs_custom = CustomJSHover(code=xsCode, args=hover_args)
    ys_custom = CustomJSHover(code=ysCode, args=hover_args)
    #</editor-fold>

    #<editor-fold Create HoverTool:
    #Create the Custom HoverTool and add it to the figure:
    hover_formatter = {"@xs" : xs_custom, "@ys" : ys_custom}
    hover_tool = HoverTool(
        tooltips=custom_tooltip, formatters=hover_formatter, renderers=[hbs],
        mode="mouse", point_policy="follow_mouse"
    )
    fig.add_tools(hover_tool)
    #</editor-fold>

    game_parts.figures["stats_2"] = fig
    game_parts.sources["stats_fig_2"] = fig_src
#</editor-fold>
