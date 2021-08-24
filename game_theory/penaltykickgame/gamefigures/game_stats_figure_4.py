from . import figure_creation as fig_creation
from bokeh.models import (CustomJSHover, ColumnDataSource, HoverTool,
                          CustomJSTransform)
from bokeh.transform import transform

#<editor-fold ys code string:
# returns the the y value of the hovered data point, and modifies the
# 'highlight_alphas' column to be filled with zeros, except for the hovered data
# point's value, which is set to 1.
ysCode = """
const index = special_vars.index;
const data = src.data;
data['highlight_alphas'].fill(0);
data['highlight_alphas'][index] = 1;
src.change.emit();
return data['ys'][index].toString();
"""
#</editor-fold>

#<editor-fold avgs code string:
# returns the average of the y values up to the hovered data point.
avgsCode = """
const index = special_vars.index;
const data = src.data;

function avgRecursive(index) {
  let val = data['ys'][index];
  if(index > 0) {
    val += index * avgRecursive(index - 1);
    val = val / (index + 1);
  }
  return val;
}

const val = avgRecursive(index);

return val.toString().substring(0,5);
"""
#</editor-fold>

#<editor-fold Custom Hover Tooltip:
# Display for the hovered information.
custom_tooltip = """
<div>
  <font size="1pt"><p>Iteration: @xs<br>
Striker Foot: @feet<br>
Aim Direction: @directions<br>
Goalie Action: @actions<br>
Score Chance: @ys{custom}<br>
Avg Score Chance: @avgs_placeholder{custom}</p></font>
</div>
"""
#</editor-fold>

# <editor-fold Get Avgs Code String:
# returns a list with values equal to the average of the previous list's values
# up to that index.
getAvgs = """
let newXs = [];
xs.forEach(
  (v, i) => (newXs.push((i !== 0) ? ((v + i * newXs[i - 1]) / (i + 1)) : v))
);

return newXs;
"""
#</editor-fold>

#<editor-fold Configs:
class Configs:
    """A class used to configure Stats Figure 4.


    Attributes:
    fig -- The fig_creation.FigureConfigs object being used to configure the
      main figure.
    plot_dots -- The _DotConfigs object being used to configure the plot
      data dots.
    highlight_dots -- The _DotConfigs object being used to configure the plot
      highlight dots.
    guiding_lines -- The _LineConfigs object being used to configure the plot's
      guiding lines.
    avgs_line -- The _LineConfigs object being used to configure the plot's
      average value line.
    hitbox_alpha -- An int or float between 0 and 1 used to set the alphas of
      the plot's hitboxes.


    Inner Classes:
    _DotConfigs -- A class for configuring the dots within the plot.
    _LineConfigs -- A class for configuring the lines within the plot.
    """
    #<editor-fold __init__():
    def __init__(
        self, fig_base_tools="", fig_toolbar_loc="below",
        fig_toolbar_sticky=False, fig_title="Score Chance Over Iterations",
        fig_width=600, fig_height=360, fig_x_range=(0.5, 50.5),
        fig_y_range=(0.5, 1.0), fig_visibility=False,
        fig_sizing_mode="stretch_both", fig_outline_line_color="black",
        fig_background_color="white", fig_title_font_size="16pt",
        fig_x_axis_visibility=True, fig_y_axis_visibility=True,
        fig_x_axis_line_color="black", fig_y_axis_line_color="black",
        fig_x_grid_visibility=False, fig_y_grid_visibility=False,
        fig_x_grid_line_color="black", fig_y_grid_line_color="black",
        plot_dot_line_color="#D8CB2D", plot_dot_fill_color="#ECDF41",
        plot_dot_size=5, plot_dot_alpha=1, highlight_dot_line_color="#D8A42D",
        highlight_dot_fill_color="#ECB841", highlight_dot_size=10,
        guiding_line_color="#000000", guiding_line_alpha=0.1,
        avgs_line_color="#000000", avgs_line_alpha=1, hitbox_alpha=0
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
        plot_dot_line_color -- A string containing the color to use for the
          plot's data dot outline. Must be Bokeh compatible.
        plot_dot_fill_color -- A string containing the color to use for the
          plot's data dot fill. Must be Bokeh compatible.
        plot_dot_size -- An int or float to use as the size of the dots for the
          plot's data.
        plot_dot_alpha -- An int or float between 0 and 1 to use as the alpha of
          the plot's data dots.
        highlight_dot_line_color -- A string containing the color to use for the
          outline of the plot's highlight dots. Must be Bokeh compatible.
        highlight_dot_fill_color -- A string containing the color to use for the
          fill of the plot's highlight dots.  Must be Bokeh compatible.
        highlight_dot_size -- An int or float to use as the size of the plot's
          highlight dots.
        guiding_line_color -- A string containing the color to use for the
          guidining lines of the plot. Must be Bokeh compatible.
        guiding_line_alpha -- An int or float between 0 and 1 to use as the
          alpha for the plot's guiding lines.
        avgs_line_color -- A string containing the color to use for the average
          value line of the plot. Must be Bokeh compatible.
        avgs_line_alpha -- An int or float between 0 and 1 to use as the alpha
          for the average value line of the plot.
        hitbox_alpha -- An int or float between 0 and 1 to use as the alpha for
          the plot's hitboxes.
        """
        self.fig = fig_creation.FigureConfigs(
            fig_base_tools, fig_toolbar_loc, fig_toolbar_sticky, fig_title,
            fig_width, fig_height, fig_x_range, fig_y_range, fig_visibility,
            fig_sizing_mode, fig_outline_line_color, fig_background_color,
            fig_title_font_size, fig_x_axis_visibility, fig_y_axis_visibility,
            fig_x_axis_line_color, fig_y_axis_line_color, fig_x_grid_visibility,
            fig_y_grid_visibility, fig_x_grid_line_color, fig_y_grid_line_color
        )
        self.plot_dots = self._DotConfigs(
            plot_dot_line_color, plot_dot_fill_color, plot_dot_size,
            plot_dot_alpha
        )
        self.highlight_dots = self._DotConfigs(
            highlight_dot_line_color, highlight_dot_fill_color,
            highlight_dot_size, None
        )
        self.guiding_lines = self._LineConfigs(
            guiding_line_color, guiding_line_alpha
        )
        self.avgs_line = self._LineConfigs(
            avgs_line_color, avgs_line_alpha
        )
        self.hitbox_alpha = hitbox_alpha
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

    #<editor-fold _LineConfigs:
    class _LineConfigs:
        """A class used to configure lines on the plot.


        Attributes:
        color -- A string containing the color to use for the line type. Must be
          Bokeh compatible.
        alpha -- An int or float between 0 and 1 used to set the alpha of the
          line type.
        """
        #<editor-fold __init__():
        def __init__(self, color, alpha):
            """Initializer for the class _LineConfigs. Creates a _LineConfigs
            object with the input values from the arguments.


            Arguments:
            color -- A string containing the color used to set self.color. Must
              be Bokeh compatible.
            alpha -- An int or float between 0 and 1 used to set self.alpha.
            """
            self.color = color
            self.alpha = alpha
        #</editor-fold>
    #</editor-fold>
#</editor-fold>

#<editor-fold create():
def create(game_parts, configs):
    """Creates Game Stats Figure 4 according to the passed in Configs object's
    attributes. Also creates Game Stats Figure 4's ColumnDataSource. Game Stats
    Figure 4 is then fully set up, before both the figure and its source are
    added to the passed in _GameParts object being used to collect the game
    components.


    Arguments:
    game_parts -- The penalty_kick_automated_game._GameParts object being used
      to collect the game components.
    configs -- The Configs object being used to configure the figure.
    """
    fig = fig_creation.make_fig(configs.fig)

    #<editor-fold ColumnDataSource Creation:
    src_xs = []
    for i in range(1, 51):
        src_xs.append(i)

    src_data = {
        "xs" : src_xs,
        "ys" : [0] * 50,
        "feet" : [None] * 50,
        "directions" : [None] * 50,
        "actions" : [None] * 50,
        "highlight_alphas" : [0] * 50,
        "avgs_placeholder" : [0] * 50
    }
    fig_src = ColumnDataSource(data=src_data)
    #</editor-fold>

    #<editor-fold Plot Figure Elements:
    fig.circle_dot(
        x="xs", y="ys", source=fig_src, size=configs.plot_dots.size,
        alpha=configs.plot_dots.alpha, line_color=configs.plot_dots.line_color,
        fill_color=configs.plot_dots.fill_color
    )

    fig.circle_dot(
        x="xs", y="ys", source=fig_src, size=configs.highlight_dots.size,
        alpha="highlight_alphas", line_color=configs.highlight_dots.line_color,
        fill_color=configs.highlight_dots.fill_color
    )

    hbs = fig.rect(
        x="xs", y=0.75, source=fig_src, width=1, height=0.5, fill_alpha=0,
        line_alpha=configs.hitbox_alpha, line_color="black"
    )

    get_avgs = CustomJSTransform(v_func=getAvgs)

    avgs_line = fig.line(
        x="xs", y=transform("ys", get_avgs), source=fig_src,
        line_color=configs.avgs_line.color, alpha=configs.avgs_line.alpha
    )

    y_vals = [
        0.55, 0.65, 0.93, 0.74, 0.60, 0.72, 0.95, 0.73, 0.70,
        0.67, 0.70, 0.96, 0.74, 0.60, 0.72, 0.87, 0.65, 0.61
    ]
    for y_val in y_vals:
        fig.line(
            x="xs", y=y_val, source=fig_src,
            line_color=configs.guiding_lines.color,
            line_alpha=configs.guiding_lines.alpha
        )
    #</editor-fold>

    #<editor-fold Create HoverTool:
    #Custom HoverTool:
    hover_main_args_dict = {"src" : fig_src}
    ys_custom = CustomJSHover(code=ysCode, args=hover_main_args_dict)
    avgs_custom = CustomJSHover(code=avgsCode, args=hover_main_args_dict)
    hovertool_formatters = {"@ys" : ys_custom,
                            "@avgs_placeholder" : avgs_custom}
    hover_tool = HoverTool(
        tooltips=custom_tooltip, formatters=hovertool_formatters,
        mode="mouse", point_policy="follow_mouse", renderers=[hbs]
    )
    fig.add_tools(hover_tool)
    #</editor-fold>

    game_parts.figures["stats_4"] = fig
    game_parts.sources["stats_fig_4"] = fig_src
#</editor-fold>
