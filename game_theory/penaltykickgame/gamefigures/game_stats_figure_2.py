from bokeh.models import (CustomJSHover, ColumnDataSource, HoverTool)
from . import figure_creation as fig_creation

#<editor-fold xs Code String:
# Returns the iteration number and makes the necessary changes for highlighting
# the hovered data point.
xsCode = """
const index = special_vars.index;
const data = src.data;

data['highlight_alphas'].fill(0);
data['highlight_alphas'][index] = 1;
src.change.emit();

return(data['xs'][index].toString());
"""
#</editor-fold>

#<editor-fold Custom HoverTool Tooltip Code String:
# Code below is for how the custom HoverTool displays the information.
custom_tooltip = """
<div>
  <font size="1pt"><p>Iteration: @xs{custom}<br>
Score: @ys</p></font>
</div>
"""
#</editor-fold>

#<editor-fold Configs:
class Configs:
    """A class used to configure Stats figure 2.


    Attributes:
    fig -- A figure_creation.FigureConfigs object being used to configure the
      main figure.
    score_dots -- A _DotConfigs object being used to configure the plot's dots
      for showing the scores.
    chance_dots -- A _DotConfigs object being used to configure the plot's dots
      for showing the expected scores not subject to chance.
    highlight_dots -- A _DotConfigs object being used to configure the
      highlight_dots within the plot.
    hitbox_alpha -- An int or float between 0 and 1. The alpha to use for the
      plot's hitboxes.


    Inner Classes:
    _DotConfigs -- A class for configuring the dots within the plot.
    """

    #<editor-fold __init__():
    def __init__(
        self, fig_base_tools="", fig_toolbar_loc="below",
        fig_toolbar_sticky=False, fig_title="Score Over Iterations Run",
        fig_width=600, fig_height=360, fig_x_range=(-0.5, 50.5),
        fig_y_range=(-50, 50), fig_visibility=False,
        fig_sizing_mode="stretch_both", fig_outline_line_color="black",
        fig_background_color="white", fig_title_font_size='16pt',
        fig_x_axis_visibility=True, fig_y_axis_visibility=True,
        fig_x_axis_line_color="black", fig_y_axis_line_color="black",
        fig_x_grid_visibility=False, fig_y_grid_visibility=False,
        fig_x_grid_line_color="black", fig_y_grid_line_color="black",
        score_dot_line_color="#B56464", score_dot_fill_color="#CE7D7D",
        score_dot_size=5, score_dot_alpha=1, chance_dot_line_color="black",
        chance_dot_fill_color="black", chance_dot_size=3, chance_dot_alpha=1,
        highlight_dot_line_color="#6464B5", highlight_dot_fill_color="#7D7DCE",
        highlight_dot_size=10, hitbox_alpha=0
    ):
        """Initializer for the class Configs. Creates a Configs object
        containing the relevant information for creating the figure with the
        input argument values.


        Keyword Arguments:
        fig_base_tools -- A string containing the base tools to add to the
          figure. Must be Bokeh compatible.
        fig_toolbar_loc -- A string containing the location to use for the
          figure toolbar. Must be Bokeh compatible.
        fig_toolbar_sticky -- A bool for whether or not to make the figure tool
          bar sticky.
        fig_title -- A string. The title to use for the figure.
        fig_width -- An int. The width to use for the figure.
        fig_height -- An int. The width to use for the figure.
        fig_x_range -- An (int, int) or (float, float) pair containing the
          x range to use for the figure.
        fig_y_range -- An (int, int) or (float, float) pair cointaining the
          y range to use for the figure.
        fig_visibility -- A bool for setting the figure's initial visibility.
        fig_sizing_mode -- A string containing how the figure should be sized.
          Must be Bokeh compatible.
        fig_outline_line_color -- A string containing the color to use for the
          figure outline. Must be Bokeh compatible.
        fig_background_color -- A string containing the color to use for the
          figure background. Must be Bokeh compatible.
        fig_title_font_size -- A string containing the font size to use for the
          figure title. Must be Bokeh compatible.
        fig_x_axis_visibility -- A bool for setting the figure's
          x axis' visibility.
        fig_y_axis_visibility -- A bool for setting the figure's
          y axis' visibility.
        fig_x_axis_line_color -- A string containing the color to use for the
          figure's x axis. Must be Bokeh compatible.
        fig_y_axis_line_color -- A string containing the color to use for the
          figure's y axis. Must be Bokeh compatible.
        fig_x_grid_visibility -- A bool for setting the figure's
          x grid's visibility.
        fig_y_grid_visibility -- A bool for setting the figure's
          y grid's visibility.
        fig_x_grid_line_color -- A string containing the color to use for the
          figure's x grid. Must be Bokeh compatible.
        fig_y_grid_line_color -- A string containing the color to use for the
          figure's y grid. Must be Bokeh compatible.
        score_dot_line_color -- A string containing the color to use for the
          plot's score dot outlines. Must be Bokeh compatible.
        score_dot_fill_colors -- A string containing the color to use for the
          plot's score dot fills. Must be Bokeh compatible.
        score_dot_size -- An int or float to use as the size of the plot's
          score dots.
        score_dot_alpha -- An int or float between 0 and 1 to use as the alpha
          of the plot's score dots.
        chance_dot_line_color -- A string containing the color to use for the
          outlines of the plot's dots for showing expected score values. Must be
          Bokeh compatible.
        chance_dot_fill_colors -- A string containing the color to use for the
          fills of the plot's dots for showing expected score values. Must be
          Bokeh compatible.
        chance_dot_size -- An int or float to use as the size of the plot's
          dots for showing expected score values.
        chance_dot_alpha -- An int or float between 0 and 1 to use as the alpha
          of the plot's dots for showing expected score values.
        highlight_dot_line_color -- A string containing the color to use for the
          outline of the plot's highlight dots. Must be Bokeh compatible.
        highlight_dot_fill_color -- A string containing the color to use for the
          fill of the plot's highlight dots.  Must be Bokeh compatible.
        highlight_dot_size -- An int or float to use as the size of the plot's
          highlight dots.
        hitbox_alpha -- An int or float between 0 and 1 to use as the alpha for
          the plot's hitboxes.
        """
        self.fig = fig_creation.FigureConfigs(
            fig_base_tools,fig_toolbar_loc, fig_toolbar_sticky, fig_title,
            fig_width, fig_height, fig_x_range, fig_y_range, fig_visibility,
            fig_sizing_mode, fig_outline_line_color, fig_background_color,
            fig_title_font_size, fig_x_axis_visibility, fig_y_axis_visibility,
            fig_x_axis_line_color, fig_y_axis_line_color, fig_x_grid_visibility,
            fig_y_grid_visibility, fig_x_grid_line_color, fig_y_grid_line_color
        )
        self.score_dots = self._DotConfigs(
            score_dot_line_color, score_dot_fill_color, score_dot_size,
            score_dot_alpha
        )
        self.chance_dots = self._DotConfigs(
            chance_dot_line_color, chance_dot_fill_color, chance_dot_size,
            chance_dot_alpha
        )
        self.highlight_dots = self._DotConfigs(
            highlight_dot_line_color, highlight_dot_fill_color,
            highlight_dot_size, None
        )
        self.hitbox_alpha=hitbox_alpha
    #</editor-fold>

    #<editor-fold _DotConfigs:
    class _DotConfigs:
        """A class used to configure dots on the plot.


        Attributes:
        line_color -- A string containing the color to use as the outline color
          of the dot type. Must be Bokeh compatible.
        fill_color -- A string containing the color to use as the fill color of
          the dot type. Must be Bokeh compatible.
        size -- An int or float used to set the size of the dot type.
        alpha -- An int or float between 0 and 1 used to set the alpha of the
          dot type.
        """
        #<editor-fold __init__():
        def __init__(self, line_color, fill_color, size, alpha):
            """Initializer for the class _DotConfigs. Creates a _DotConfigs
            object with the input values from the arguments.


            Arguments:
            line_color -- A string containing the color used to set
              self.line_color. Must be Bokeh compatible.
            fill_color -- A string containing the color used to set
              self.fill_color. Must be Bokeh compatible.
            size -- An int or float used to set self.size.
            alpha -- An int or float between 0 and 1 used to set self.alpha.
            """
            self.line_color = line_color
            self.fill_color = fill_color
            self.size = size
            self.alpha = alpha
        #</editor-fold>
    #</editor-fold>
#</editor-fold>

#<editor-fold create():
def create(game_parts, configs):
    """Creates Game Stats Figure 2 according to the passed in Configs object's
    attributes. Also creates Game Stats Figure 2's ColumnDataSource. Game Stats
    Figure 2 is then fully set up, before both the figure and its source are
    added to the passed in _GameParts object being used to collect the game
    components.


    Arguments:
    game_parts -- The penalty_kick_automated_game._GameParts object being used
      to collect the game components.
    configs -- The Configs object being used to configure the figure.
    """
    fig = fig_creation.make_fig(configs.fig)

    #<editor-fold ColumnDataSource Creation:
    #Create initial values for stats_fig_2_source
    src_xs = []
    for i in range(51):
        src_xs.append(i)
    #Create stats_fig_2_source with the values that were created.
    src_data = {
        "xs" : src_xs,
        "ys" : [0] * 51,
        "chance_ys" : [0] * 51,
        "heights" : [100] * 51,
        "highlight_alphas" : [0] * 51
    }
    fig_src = ColumnDataSource(data=src_data)
    #</editor-fold>

    #<editor-fold Plot Figure Elements
    fig.circle_dot(
        x="xs", y="ys", source=fig_src, size=configs.score_dots.size,
        line_color=configs.score_dots.line_color,
        fill_color=configs.score_dots.fill_color, alpha=configs.score_dots.alpha
    )
    fig.circle_dot(
        x="xs", y="chance_ys", source=fig_src, size=configs.chance_dots.size,
        line_color=configs.chance_dots.line_color,
        fill_color=configs.chance_dots.fill_color,
        alpha=configs.chance_dots.alpha
    )
    fig.circle_dot(
        x="xs", y="ys", source=fig_src, size=configs.highlight_dots.size,
        line_color=configs.highlight_dots.line_color,
        fill_color=configs.highlight_dots.fill_color, alpha="highlight_alphas"
    )
    hbs = fig.rect(
        x="xs", y=0, source=fig_src, width=1, height="heights", alpha=0,
        line_color=configs.score_dots.fill_color,
        line_alpha=configs.hitbox_alpha
    )
    #</editor-fold>

    xs_custom = CustomJSHover(code=xsCode, args={"src" : fig_src})

    #<editor-fold Create HoverTool:
    #Create the Custom HoverTool and add it to the figure:
    hover_tool = HoverTool(
        tooltips=custom_tooltip, formatters={"@xs" : xs_custom},
        renderers=[hbs], mode="mouse", point_policy="follow_mouse"
    )
    fig.add_tools(hover_tool)
    #</editor-fold>

    game_parts.figures["stats_2"] = fig
    game_parts.sources["stats_fig_2"] = fig_src
#</editor-fold>
