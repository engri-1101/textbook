from . import figure_creation as fig_creation
from bokeh.models import (CustomJSHover, ColumnDataSource, CustomJSTransform,
                          HoverTool, Div)
from bokeh.transform import transform

# CONSTANT USED ACROSS FILE TO ITERATE THROUGH Striker Foot,
# Keeper Action Possibilities:
SFKAS = ["ll", "lm", "lr", "rl", "rm", "rr"]

#<editor-fold hb_gc_code():
def hb_gc_code(hbno):
    """hb_gc_code is a function used to obtain the correct v_func code string
    for the CustomJSTransform being used to get the center y coordinates of a
    given set of hbs (hitboxes). When calling the function for a hb (they are
    labeled hb1 through hb6), the parameter hbno should be the number of that
    hb (E.g hbno should be 4 for hb4).


    Argument:
    hbno - An int, either 1, 2, 3, 4, 5, or 6. Should correspond to the int in
    the hb name.


    Returns:
    string - A JavaScript code string that will work as the v_func for a bokeh
    CustomJSTransform being used to obtain the y coordinates of the centers of
    a set of hbs.
    """
    srcDats = [
        """ + data['hb1'][i]""", """ + data['hb2'][i]""",
        """ + data['hb3'][i]""", """ + data['hb4'][i]""",
        """ + data['hb5'][i]"""
    ]
    hbno -= 2

    newXs = """v/2"""
    while(hbno >= 0):
        newXs += srcDats[hbno]
        hbno -= 1

    codeString = """
const newXs = [];
const data = src.data;
xs.forEach(
  (v, i) => newXs.push(""" + newXs + """)
);

return newXs;
"""
    return codeString
#</editor-fold>

#<editor-fold highlight_ga_code():
def highlight_ga_code(sfka):
    """highlight_ga_code is a function used to obtain the correct v_func code
    string for the CustomJSTransform being used to process the
    'highlight_alphas' column of fig_src.data for use in highlighting the
    correct dots on the plot according to the user's mouse position. When given
    the correct args and used in a v_func, the code string returned by this
    function will return a modified version of the 'highlight_alphas' column to
    each set of invisible highlight plot dots. The modified version will contain
    an array of ints, containing at most a single value of 1, with all other
    items in the array being 0. The returned array will only have the value of 1
    if the original 'highlight_alphas' column contained the int corresponding to
    the dot's sfka pair (Striker Foot, Keeper Action pair) in the index being
    checked by the v_func. Setting the highlight alphas of all highlight dots
    other than the indicated highlighted dot to zero makes it so that they are
    hidden to the user, giving the effect of highlighting the user's hovered
    dot.


    Argument:
    sfka - A string, either 'll', 'lm', 'lr', 'rl', 'rm', or 'rr'. The value
    used should correspond to the sfka pair associated with the set of highlight
    dots the returned v_func code string will be used for.


    Returns:
    string - A JavaScript code string that will work as the v_func for a bokeh
    CustomJSTransform being used to set the alphas of a set of highlight dots.
    """

    highlightVal = str(SFKAS.index(sfka) + 1)

    codeString = """
const index = parseInt(highlightIndex.text);
if(xs[index] === """ + highlightVal + """) {
  const newAlphas = new Array(xs.length).fill(0);
  newAlphas[index] = 1;
  return newAlphas;
} else { return alphasZeroes; }
"""
    return codeString
#</editor-fold>

# Code used in the Custom Hover Code strings:
customHoverCodeSetup = """
const index = special_vars.index;
const name = special_vars.name;
const data = src.data;

"""

#<editor-fold xs Code String:
#obtains the iteration number of the selected data point and makes changes
#necessary for the other hover functions and the highlighting functionality
#of the figure.
xsCode = customHoverCodeSetup + """
function selectSortedValIndex() {
  const values = [
    data['ll_ys'][index], data['lm_ys'][index], data['lr_ys'][index],
    data['rl_ys'][index], data['rm_ys'][index], data['rr_ys'][index]
  ];

  const sortedValues = values.slice();
  sortedValues.sort((a, b) => b - a);

  selectedIndex.text = values.indexOf(sortedValues[parseInt(name)]).toString();
}

const column = [1, 2, 3, 4, 5, 6];

selectSortedValIndex();

const selected = column[parseInt(selectedIndex.text)];

data['highlight_alphas'][parseInt(highlightIndex.text)] = 0;
highlightIndex.text = index.toString();
data['highlight_alphas'][index] = selected;

src.change.emit();

return index.toString();
"""
#</editor-fold>

#<editor-fold ys Code String:
#Obtains the y value of the selected data point.
ysCode = customHoverCodeSetup + """
const column = ['ll', 'lm', 'lr', 'rl', 'rm', 'rr'];
const selected = column[parseInt(selectedIndex.text)];

return data[`${selected}_ys`][index].toString().substring(0, 5);
"""
#</editor-fold>

#<editor-fold selected Code String:
#Obtains the SF-GA associated with the selected data point
selectedCode = customHoverCodeSetup + """
const column = ['ll', 'lm', 'lr', 'rl', 'rm', 'rr'];
return column[parseInt(selectedIndex.text)];
"""
#</editor-fold>

#<editor-fold Custom Hover Tooltip Code String:
#Code below is for how the custom HoverTool displays the information.
#Note: some of the columns used by the hovertool don't need to actually be
#those columns (ll_ys, lm_ys). They were used because the hovertool needs an
#actual column in the src.
custom_tooltip = """
<div>
  <font size="1pt"><p>Iteration: @xs{custom}<br>
Risk: @ll_ys{custom}<br>
Risk SFKA: @lm_ys{custom}</p></font>
</div>
"""
#</editor-fold>

#<editor-fold Configs():
class Configs():
    """A class used to configure Stats figure 3.


    Attributes:
    fig -- A figure_creation.FigureConfigs object being used to configure the
      main figure.
    plot_dots -- A list of _DotConfigs objects being used to configure the
      sets of dots representing data within the plot.
    highlight_dots -- A _DotConfigs object being used to configure the
      highlight_dots within the plot.
    hitbox_alpha -- An int or float between 0 and 1. The alpha to use for the
      plot's hitboxes.


    Inner Classes:
    _DotConfigs -- A class for configuring the dots within the plot.
    """

    #<editor-fold __init__():
    plot_dot_fill_colors_default = [
        "#C8AFAF", "#C8C8AF", "#AFC8AF", "#AFC8C8", "#AFAFC8", "#C8AFC8"
    ]
    plot_dot_line_colors_default = [
        "#AF9696", "#AFAF96", "#96AF96", "#96AFAF", "#9696AF", "#AF96AF"
    ]
    def __init__(
        self, fig_base_tools="", fig_toolbar_loc="below",
        fig_toolbar_sticky=False,
        fig_title="Keeper's Perceived Risks Over Iterations", fig_width=600,
        fig_height=360, fig_x_range=(-0.5, 50.5), fig_y_range=(0, 1),
        fig_visibility=False, fig_sizing_mode="stretch_both",
        fig_outline_line_color="black", fig_background_color="white",
        fig_title_font_size="16pt", fig_x_axis_visibility=True,
        fig_y_axis_visibility=True, fig_x_axis_line_color="black",
        fig_y_axis_line_color="black", fig_x_grid_visibility=False,
        fig_y_grid_visibility=False, fig_x_grid_line_color="black",
        fig_y_grid_line_color="black",
        plot_dot_line_colors=plot_dot_line_colors_default,
        plot_dot_fill_colors=plot_dot_fill_colors_default, plot_dot_size=5,
        plot_dot_alpha=1, highlight_dot_line_color="#000000",
        highlight_dot_fill_color="#000000", highlight_dot_size=10,
        hitbox_alpha=0
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
        plot_dot_line_colors -- A list of strings containing the colors to use
          for the plot's data dot outlines. Must be Bokeh compatible.
        plot_dot_fill_colors -- A list of strings containing the colors to use
          for the plot's data dot fills. Must be Bokeh compatible.
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
        self.plot_dots=[]
        for i in range(len(plot_dot_fill_colors)):
            dots = self._DotConfigs(
                plot_dot_line_colors[i], plot_dot_fill_colors[i], plot_dot_size,
                plot_dot_alpha
            )
            self.plot_dots.append(dots)
        self.highlight_dots = self._DotConfigs(
            highlight_dot_line_color, highlight_dot_fill_color,
            highlight_dot_size, None
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
#</editor-fold>

#<editor-fold create():
def create(game_parts, configs):
    """Creates Game Stats Figure 3 according to the passed in Configs object's
    attributes. Also creates Game Stats Figure 3's ColumnDataSource. Game Stats
    Figure 3 is then fully set up, before both the figure and its source are
    added to the passed in _GameParts object being used to collect the game
    components.


    Arguments:
    game_parts -- The penalty_kick_automated_game._GameParts object being used
      to collect the game components.
    configs -- The Configs object being used to configure the figure.
    """
    fig = fig_creation.make_fig(configs.fig)
    highlight_index = Div(text="0")
    selected_index = Div(text="-1")
    #<editor-fold ColumnDataSource Creation:
    src_xs = []
    for i in range(51):
        src_xs.append(i)

    src_data = {
        "xs" : src_xs,
        "ll_ys" : [0.760000] + [0]*50,
        "lm_ys" : [0.650000] + [0]*50,
        "lr_ys" : [0.763333] + [0]*50,
        "rl_ys" : [0.746666] + [0]*50,
        "rm_ys" : [0.660000] + [0]*50,
        "rr_ys" : [0.783333] + [0]*50,
        "hb1" : [0] * 51,
        "hb2" : [0] * 51,
        "hb3" : [0] * 51,
        "hb4" : [0] * 51,
        "hb5" : [0] * 51,
        "hb6" : [0] * 51,
        "highlight_alphas" : [0] * 51,
        "alphas_zeroes" : [0] * 51
    }

    fig_src = ColumnDataSource(data=src_data)
    #</editor-fold>

    #<editor-fold Create CustomJSTransforms:
    #Create the CustomJSTransforms that are used by the figure
    ga_args_dict = {
        "highlightIndex" : highlight_index,
        "alphasZeroes" : fig_src.data["alphas_zeroes"]
    }
    gc_args_dict = {"src" : fig_src}

    highlight_gas = []
    gcs = []
    for i in range(6):
        highlight_ga = CustomJSTransform(
            v_func=highlight_ga_code(SFKAS[i]), args=ga_args_dict
        )
        gc = CustomJSTransform(args=gc_args_dict, v_func=hb_gc_code(i + 1))

        highlight_gas.append(highlight_ga)
        gcs.append(gc)
    #</editor-fold>

    #<editor-fold Plot Figure Elements:
    #Create the Data Points and hitboxes for the figure:
    # plot_ys = ["ll_ys", "lm_ys", "lr_ys", "rl_ys", "rm_ys", "rr_ys"]
    hb_ids = ["hb1", "hb2", "hb3", "hb4", "hb5", "hb6"]
    hb_names = ["5", "4", "3", "2", "1", "0"]

    hbs = []
    for i in range(6):
        dot = configs.plot_dots[i]
        fig.circle_dot(
            x="xs", y=(SFKAS[i] + "_ys"), source=fig_src, size=dot.size,
            line_color=dot.line_color, fill_color=dot.fill_color,
            alpha=dot.alpha
        )
        hb = fig.rect(
            x="xs", y=transform(hb_ids[i], gcs[i]), source=fig_src, width=1,
            height=hb_ids[i], name=hb_names[i], fill_alpha=0,
            alpha=configs.hitbox_alpha
        )

        hbs.append(hb)

    for i in range(6): #Has to be after initial dots due to display order.
        fig.circle_dot(
            x="xs", y=(SFKAS[i] + "_ys"), source=fig_src,
            size=configs.highlight_dots.size,
            line_color=configs.highlight_dots.line_color,
            fill_color=configs.highlight_dots.fill_color,
            alpha=transform("highlight_alphas", highlight_gas[i])
        )

    #</editor-fold>

    #<editor-fold CustomJSHover Creation:
    #Create the CustomJSHovers used to format the data for the figure's
    #custom HoverTool:
    hover_main_args_dict = {"src" : fig_src, "selectedIndex" : selected_index}

    hover_xs_args_dict = hover_main_args_dict.copy()
    hover_xs_args_dict["highlightIndex"] = highlight_index

    xs_custom = CustomJSHover(code=xsCode, args=hover_xs_args_dict)
    ys_custom = CustomJSHover(code=ysCode, args=hover_main_args_dict)

    selected_custom = CustomJSHover(
        code=selectedCode, args=hover_main_args_dict
    )
    #</editor-fold>

    #<editor-fold Custom HoverTool Creation:
    #Create the Custom HoverTool and add it to the figure:
    hovertool_formatters = {"@xs" : xs_custom,
                            "@ll_ys" : ys_custom,
                            "@lm_ys" : selected_custom}
    hover_tool = HoverTool(
        tooltips=custom_tooltip, formatters=hovertool_formatters, mode="mouse",
        point_policy="follow_mouse", renderers=hbs
    )
    fig.add_tools(hover_tool)
    #</editor-fold>

    game_parts.figures["stats_3"] = fig
    game_parts.sources["stats_fig_3"] = fig_src
#</editor-fold>
