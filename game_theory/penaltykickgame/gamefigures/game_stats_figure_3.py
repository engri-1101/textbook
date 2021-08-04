from . import figure_creation as fig_creation
from bokeh.models import (CustomJSHover, ColumnDataSource, CustomJSTransform,
                          HoverTool, Div)
from bokeh.transform import transform

SFGAS = ["ll", "lm", "lr", "rl", "rm", "rr"]

highlight_index = Div(text="0")
selected_index = Div(text="-1")

#<editor-fold hb_gc_code():
def hb_gc_code(hbno):
    """hb_gc_code is a function used to obtain the correct v_func code string
    for the CustomJSTransform being used to get the center y coordinates of a
    given set of hbs (hitboxes). When calling the function for an hb (they are
    labeled hb1 through hb6), the parameter hbno should be the number of that
    hb  (E.g hbno should be 4 for hb4).


    Keyword Argument:

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
def highlight_ga_code(sfga):
    """highlight_ga_code is a function used to obtain the correct v_func code
    string for the CustomJSTransform being used to process the
    'highlight_alphas' column of fig_src.data for use in
    highlighting the correct dots on the plot according to the user's mouse
    position. When given the correct args and used in a v_func, the code string
    returned by this function will return a modified version of the
    'highlight_alphas' column to each set of invisible highlight plot dots.
    The modified version will contain an array of ints, containing at most a
    single value of 1, with all other items in the array being 0. The returned
    array will only have the value of 1 if the original 'highlight_alphas'
    column contained the int corresponding to the dot's sfga pair (Striker
    Foot, Goalie Action pair) in the index being checked by the v_func.
    Setting the highlight alphas of all highlight dots other than the
    indicated highlighted dot to zero makes it so that they are hidden to the
    user, giving the effect of highlighting the user's hovered dot.


    Keyword Argument:

    sfga - A string, either 'll', 'lm', 'lr', 'rl', 'rm', or 'rr'. The value
    used should correspond to the sfga pair associated with the set of
    highlight dots the returned v_func code string will be used for.


    Returns:

    string - A JavaScript code string that will work as the v_func for a bokeh
    CustomJSTransform being used to set the alphas of a set of highlight dots.
    """

    highlightVal = str(SFGAS.index(sfga) + 1)

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
    <span style='font-size: 10px;'>Iteration:</span>
    <span style='font-size: 10px;'>@xs{custom}</span>
</div>
<div>
    <span style='font-size: 10px;'>Risk:</span>
    <span style='font-size: 10px;'>@ll_ys{custom}</span>
</div>
<div>
    <span style='font-size: 10px;'>Risk SF-GA:</span>
    <span style='font-size: 10px;'>@lm_ys{custom}</span>
</div>
"""
#</editor-fold>

#<editor-fold Configs():
class Configs():
    """Objects of this class are used to organize and pass parameters to
    Stats Figure 3. All arguments are mutable, and default values for them are
    the currently decided values being used to make the game. The main purpose
    of the configurability provided through the use of this class is to make it
    easier to test changes. Any changes that improve the game should be made
    directly to the default values of the arguments in this class after
    successful testing.
    """

    plot_dot_fill_colors_default = [
        "#C8AFAF", "#C8C8AF", "#AFC8AF", "#AFC8C8", "#AFAFC8", "#C8AFC8"
    ]
    plot_dot_outline_colors_default = [
        "#AF9696", "#AFAF96", "#96AF96", "#96AFAF", "#9696AF", "#AF96AF"
    ]

    #<editor-fold __init__():
    def __init__(
        self, fig_base_tools="", fig_toolbar_loc="below",
        fig_toolbar_sticky=False,
        fig_title="Goalie Perceived Risks Over Iterations", fig_width=600,
        fig_height=360, fig_x_range=(-0.5, 50.5), fig_y_range=(0, 1),
        fig_visibility=False, fig_sizing_mode="stretch_both",
        fig_outline_line_color=None, fig_background_color="white",
        fig_title_font_size="16pt", fig_x_axis_visibility=True,
        fig_y_axis_visibility=True, fig_x_axis_line_color="black",
        fig_y_axis_line_color="black", fig_xgrid_visibility=False,
        fig_ygrid_visibility=False, fig_xgrid_line_color="black",
        fig_ygrid_line_color="black", plot_dot_size=5,
        plot_dot_fill_colors=plot_dot_fill_colors_default,
        plot_dot_outline_colors=plot_dot_outline_colors_default,
        plot_highlight_dot_size=10,
        plot_highlight_dot_outline_color="#000000",
        plot_highlight_dot_color="#000000", hitbox_alpha=0
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
        self.dot_fill_colors = plot_dot_fill_colors
        self.dot_outline_colors = plot_dot_outline_colors
        self.plot_highlight_dot_size = plot_highlight_dot_size
        self.plot_highlight_dot_outline_color = plot_highlight_dot_outline_color
        self.plot_highlight_dot_color = plot_highlight_dot_color
        #</editor-fold>

        self.hitbox_alpha = hitbox_alpha
    #</editor-fold>
#</editor-fold>

#<editor-fold create():
def create(game_parts, configs=Configs()):
    """Fully creates and sets up stats figure 3 for use in the main game. Stats
    Figure 3 displays the goalie's perceived risks determined through
    fictitious play within the demo, according to game iteration.


    Keyword Argument:

    configs - An object of type Configs containing the user's
    desired figure values within its attributes.
    """
    fig = fig_creation.make_fig(configs.fig)

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
            v_func=highlight_ga_code(SFGAS[i]), args=ga_args_dict
        )
        gc = CustomJSTransform(args=gc_args_dict, v_func=hb_gc_code(i + 1))

        highlight_gas.append(highlight_ga)
        gcs.append(gc)
    #</editor-fold>

    #<editor-fold Plot Figure Elements:
    #Create the Data Points and hitboxes for the figure:
    plot_ys = ["ll_ys", "lm_ys", "lr_ys", "rl_ys", "rm_ys", "rr_ys"]
    hb_ids = ["hb1", "hb2", "hb3", "hb4", "hb5", "hb6"]
    hb_names = ["5", "4", "3", "2", "1", "0"]

    hbs = []
    for i in range(6):
        fig.circle_dot(
            x="xs", y=plot_ys[i], source=fig_src, size=configs.plot_dot_size,
            line_color=configs.dot_outline_colors[i],
            fill_color=configs.dot_fill_colors[i]
        )
        hb = fig.rect(
            x="xs", y=transform(hb_ids[i], gcs[i]), source=fig_src, width=1,
            height=hb_ids[i], name=hb_names[i], fill_alpha=0,
            alpha=configs.hitbox_alpha
        )

        hbs.append(hb)

    for i in range(6): #Has to be after initial dots due to display order.
        fig.circle_dot(
            x="xs", y=plot_ys[i], source=fig_src,
            size=configs.plot_highlight_dot_size,
            line_color=configs.plot_highlight_dot_outline_color,
            fill_color=configs.plot_highlight_dot_color,
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
