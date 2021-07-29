from bokeh.plotting import figure
from bokeh.models import (CustomJSHover, ColumnDataSource, CustomJSTransform,
                          HoverTool, Div)
from bokeh.transform import transform

#Create a div used by the figure to determine the highlighted index for
#hovering.
highlight_index = Div(text = "0")
selected_index = Div(text = "-1")

#<editor-fold Code String Function hb_gc_code:
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
    #Create newXs, the line of code that changes between hb v_funcs:
    newXs = """v/2"""

    #Create srcDats to organize the possible additions to the newXs line:
    srcDats = [""" + data['hb1'][i]""",
               """ + data['hb2'][i]""",
               """ + data['hb3'][i]""",
               """ + data['hb4'][i]""",
               """ + data['hb5'][i]"""]

    #Make necessary changes to newXs:
    hbno -= 2
    while(hbno >= 0):
        newXs += srcDats[hbno]
        hbno -= 1

    #Create and return the full code string:
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
#<editor-fold highlight_ga Code Strings:
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
    #Get highlight value from sfga:
    sfgas = ['ll', 'lm', 'lr', 'rl', 'rm', 'rr']
    highlightVal = str(sfgas.index(sfga) + 1)

    #Create and return code string:
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
#<editor-fold Custom Hover Code Strings:
    #<editor-fold Shared Code String Parts:
#Selects the corresponding datapoint to the hovered hitbox.
selectSortedValIndex = """
function selectSortedValIndex() {
  const values = [
    data['ll_ys'][index], data['lm_ys'][index], data['lr_ys'][index],
    data['rl_ys'][index], data['rm_ys'][index], data['rr_ys'][index]
  ];

  const sortedValues = values.slice();
  sortedValues.sort((a, b) => b - a);

  selectedIndex.text = values.indexOf(sortedValues[parseInt(name)]).toString();
}
"""
#Setup code for the code string.
customHoverCodeSetup = """
const index = special_vars.index;
const name = special_vars.name;
const data = src.data;

"""
    #</editor-fold>
    #<editor-fold xs Code String:
    #obtains the iteration number of the selected data point and makes changes
    #necessary for the other hover functions and the highlighting functionality
    #of the figure.
xsCode = customHoverCodeSetup + selectSortedValIndex + """
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

#<editor-fold Fig configs():
class Configs():
    """Objects of this class are used to organize and pass parameters to
    Stats Figure 3. All arguments are mutable, and default values for them are
    the currently decided values being used to make the game. The main purpose
    of the configurability provided through the use of this class is to make it
    easier to test changes. Any changes that improve the game should be made
    directly to the default values of the arguments in this class after
    successful testing.
    """
    def __init__(self, fig_base_tools = "box_zoom, wheel_zoom, pan",
                 fig_toolbar_loc = "below",
                 fig_title = "Goalie Perceived Risks Over Iterations",
                 fig_width = 600, fig_height = 360,
                 fig_x_range = (-0.5, 50.5), fig_y_range = (0, 1),
                 fig_initial_visibility = False,
                 fig_sizing_mode = "stretch_both", fig_title_font_size = '16pt',
                 fig_x_axis_visibility = True, fig_y_axis_visibility = True,
                 fig_xgrid_line_color = None, fig_ygrid_line_color = None,
                 fig_outline_line_color = None, fig_background_color = "white",
                 plot_dot_size = 5,
                 plot_ll_dot_color = "#C8AFAF", plot_lm_dot_color = "#C8C8AF",
                 plot_lr_dot_color = "#AFC8AF", plot_rl_dot_color = "#AFC8C8",
                 plot_rm_dot_color = "#AFAFC8", plot_rr_dot_color = "#C8AFC8",
                 plot_ll_dot_outline_color = "#AF9696",
                 plot_lm_dot_outline_color = "#AFAF96",
                 plot_lr_dot_outline_color = "#96AF96",
                 plot_rl_dot_outline_color = "#96AFAF",
                 plot_rm_dot_outline_color = "#9696AF",
                 plot_rr_dot_outline_color = "#AF96AF",
                 plot_highlight_dot_size = 10,
                 plot_highlight_dot_outline_color = "#000000",
                 plot_highlight_dot_color = "#000000", hitbox_alpha = 0):
        #<editor-fold figure:
        self.fig_base_tools = fig_base_tools
        self.fig_toolbar_loc = fig_toolbar_loc
        self.fig_title = fig_title
        self.fig_width = fig_width
        self.fig_height = fig_height
        self.fig_x_range = fig_x_range
        self.fig_y_range = fig_y_range
        self.fig_initial_visibility = fig_initial_visibility
        self.fig_sizing_mode = fig_sizing_mode
        self.fig_title_font_size = fig_title_font_size
        self.fig_x_axis_visibility = fig_x_axis_visibility
        self.fig_y_axis_visibility = fig_y_axis_visibility
        self.fig_xgrid_line_color = fig_xgrid_line_color
        self.fig_ygrid_line_color = fig_ygrid_line_color
        self.fig_outline_line_color = fig_outline_line_color
        self.fig_background_color = fig_background_color
        #</editor-fold>
        #<editor-fold plot:
        self.plot_dot_size = plot_dot_size
        self.plot_ll_dot_color = plot_ll_dot_color
        self.plot_lm_dot_color = plot_lm_dot_color
        self.plot_lr_dot_color = plot_lr_dot_color
        self.plot_rl_dot_color = plot_rl_dot_color
        self.plot_rm_dot_color = plot_rm_dot_color
        self.plot_rr_dot_color = plot_rr_dot_color
        self.plot_ll_dot_outline_color = plot_ll_dot_outline_color
        self.plot_lm_dot_outline_color = plot_lm_dot_outline_color
        self.plot_lr_dot_outline_color = plot_lr_dot_outline_color
        self.plot_rl_dot_outline_color = plot_rl_dot_outline_color
        self.plot_rm_dot_outline_color = plot_rm_dot_outline_color
        self.plot_rr_dot_outline_color = plot_rr_dot_outline_color
        self.plot_highlight_dot_size = plot_highlight_dot_size
        self.plot_highlight_dot_outline_color = plot_highlight_dot_outline_color
        self.plot_highlight_dot_color = plot_highlight_dot_color
        #</editor-fold>
        self.hitbox_alpha = hitbox_alpha
#</editor-fold>

#<editor-fold stats_figure_3_setup:
def create(game_parts, configs = Configs()):
    """Fully creates and sets up stats figure 3 for use in the main game. Stats
    Figure 3 displays the goalie's perceived risks determined through
    fictitious play within the demo, according to game iteration.


    Keyword Argument:

    configs - An object of type Configs containing the user's
    desired figure values within its attributes.
    """
    #<editor-fold Figure Creation:
    #Create and configure the main aspects of the figure:
    fig = figure(tools = configs.fig_base_tools,
                 toolbar_location = configs.fig_toolbar_loc,
                 title = configs.fig_title,
                 plot_width = configs.fig_width,
                 plot_height = configs.fig_height,
                 x_range = configs.fig_x_range, y_range = configs.fig_y_range,
                 visible = configs.fig_initial_visibility,
                 sizing_mode = configs.fig_sizing_mode)
    fig.title.text_font_size = configs.fig_title_font_size
    fig.xaxis.visible = configs.fig_x_axis_visibility
    fig.yaxis.visible = configs.fig_y_axis_visibility
    fig.xgrid.grid_line_color = configs.fig_xgrid_line_color
    fig.ygrid.grid_line_color = configs.fig_ygrid_line_color
    fig.outline_line_color = configs.fig_outline_line_color
    fig.background_fill_color = configs.fig_background_color
    #</editor-fold>
    #<editor-fold ColumnDataSource Creation:
        #<editor-fold Create Base Values:
        #Create initial values for fig_src
    src_xs = []

    src_ll_ys = []
    src_lm_ys = []
    src_lr_ys = []
    src_rl_ys = []
    src_rm_ys = []
    src_rr_ys = []

    src_highlight_alphas = []
    src_alphas_zeroes = []

    src_hb1_ys = []
    src_hb2_ys = []
    src_hb3_ys = []
    src_hb4_ys = []
    src_hb5_ys = []
    src_hb6_ys = []

    for i in range(51):
        src_xs.append(i)

        src_ll_ys.append(0)
        src_lm_ys.append(0)
        src_lr_ys.append(0)
        src_rl_ys.append(0)
        src_rm_ys.append(0)
        src_rr_ys.append(0)

        src_highlight_alphas.append(0)
        src_alphas_zeroes.append(0)

        src_hb1_ys.append(0)
        src_hb2_ys.append(0)
        src_hb3_ys.append(0)
        src_hb4_ys.append(0)
        src_hb5_ys.append(0)
        src_hb6_ys.append(0)

    #Update Initial Values (Based off of data from table in lab key):
    src_ll_ys[0] = ((1/3 * 0.67) + (1/3 * 0.74) + (1/3 * 0.87))
    src_lm_ys[0] = ((1/3 * 0.70) + (1/3 * 0.60) + (1/3 * 0.65))
    src_lr_ys[0] = ((1/3 * 0.96) + (1/3 * 0.72) + (1/3 * 0.61))
    src_rl_ys[0] = ((1/3 * 0.55) + (1/3 * 0.74) + (1/3 * 0.95))
    src_rm_ys[0] = ((1/3 * 0.65) + (1/3 * 0.60) + (1/3 * 0.73))
    src_rr_ys[0] = ((1/3 * 0.93) + (1/3 * 0.72) + (1/3 * 0.70))
        #</editor-fold>
        #<editor-fold Make Data Source Using Base Values:
        #Create fig_src with the values that were created.
    src_data = dict(xs = src_xs,
                    ll_ys = src_ll_ys, lm_ys = src_lm_ys, lr_ys = src_lr_ys,
                    rl_ys = src_rl_ys, rm_ys = src_rm_ys, rr_ys = src_rr_ys,

                    hb1 = src_hb1_ys, hb2 = src_hb2_ys, hb3 = src_hb3_ys,
                    hb4 = src_hb4_ys, hb5 = src_hb5_ys, hb6 = src_hb6_ys,

                    highlight_alphas = src_highlight_alphas,
                    alphas_zeroes = src_alphas_zeroes)

    fig_src = ColumnDataSource(data = src_data)
        #</editor-fold>
    #</editor-fold>
    #<editor-fold Get Alpha Transforms:
    #Create the CustomJSTransforms that are used by the figure to update the
    #highlight dots according to the values contained within the
    #fig_src column 'highlight_alphas'
    args_dict = dict(highlightIndex = highlight_index,
                     alphasZeroes = fig_src.data['alphas_zeroes'])
    ll_highlight_ga = CustomJSTransform(v_func = highlight_ga_code('ll'),
                                        args = args_dict)
    lm_highlight_ga = CustomJSTransform(v_func = highlight_ga_code('lm'),
                                        args = args_dict)
    lr_highlight_ga = CustomJSTransform(v_func = highlight_ga_code('lr'),
                                        args = args_dict)
    rl_highlight_ga = CustomJSTransform(v_func = highlight_ga_code('rl'),
                                        args = args_dict)
    rm_highlight_ga = CustomJSTransform(v_func = highlight_ga_code('rm'),
                                        args = args_dict)
    rr_highlight_ga = CustomJSTransform(v_func = highlight_ga_code('rr'),
                                        args = args_dict)
    #</editor-fold>
    #<editor-fold Plot Figure Data Points:
    #Create the Data Points for the figure:
    fig.circle_dot('xs', 'll_ys', source = fig_src,
                   size = configs.plot_dot_size,
                   line_color = configs.plot_ll_dot_outline_color,
                   fill_color = configs.plot_ll_dot_color)
    fig.circle_dot('xs', 'lm_ys', source = fig_src,
                   size = configs.plot_dot_size,
                   line_color = configs.plot_lm_dot_outline_color,
                   fill_color = configs.plot_lm_dot_color)
    fig.circle_dot('xs', 'lr_ys', source = fig_src,
                   size = configs.plot_dot_size,
                   line_color = configs.plot_lr_dot_outline_color,
                   fill_color = configs.plot_lr_dot_color)
    fig.circle_dot('xs', 'rl_ys', source = fig_src,
                   size = configs.plot_dot_size,
                   line_color = configs.plot_rl_dot_outline_color,
                   fill_color = configs.plot_rl_dot_color)
    fig.circle_dot('xs', 'rm_ys', source = fig_src,
                   size = configs.plot_dot_size,
                   line_color = configs.plot_rm_dot_outline_color,
                   fill_color = configs.plot_rm_dot_color)
    fig.circle_dot('xs', 'rr_ys', source = fig_src,
                   size = configs.plot_dot_size,
                   line_color = configs.plot_rr_dot_outline_color,
                   fill_color = configs.plot_rr_dot_color)

    #Plot Highlight Points For Figure:
    fig.circle_dot('xs', 'll_ys', source = fig_src,
                   size = configs.plot_highlight_dot_size,
                   line_color = configs.plot_highlight_dot_outline_color,
                   fill_color = configs.plot_highlight_dot_color,
                   alpha = transform('highlight_alphas', ll_highlight_ga))
    fig.circle_dot('xs', 'lm_ys', source = fig_src,
                   size = configs.plot_highlight_dot_size,
                   line_color = configs.plot_highlight_dot_outline_color,
                   fill_color = configs.plot_highlight_dot_color,
                   alpha = transform('highlight_alphas', lm_highlight_ga))
    fig.circle_dot('xs', 'lr_ys', source = fig_src,
                   size = configs.plot_highlight_dot_size,
                   line_color = configs.plot_highlight_dot_outline_color,
                   fill_color = configs.plot_highlight_dot_color,
                   alpha = transform('highlight_alphas', lr_highlight_ga))
    fig.circle_dot('xs', 'rl_ys', source = fig_src,
                   size = configs.plot_highlight_dot_size,
                   line_color = configs.plot_highlight_dot_outline_color,
                   fill_color = configs.plot_highlight_dot_color,
                   alpha = transform('highlight_alphas', rl_highlight_ga))
    fig.circle_dot('xs', 'rm_ys', source = fig_src,
                   size = configs.plot_highlight_dot_size,
                   line_color = configs.plot_highlight_dot_outline_color,
                   fill_color = configs.plot_highlight_dot_color,
                   alpha = transform('highlight_alphas', rm_highlight_ga))
    fig.circle_dot('xs', 'rr_ys', source = fig_src,
                   size = configs.plot_highlight_dot_size,
                   line_color = configs.plot_highlight_dot_outline_color,
                   fill_color = configs.plot_highlight_dot_color,
                   alpha = transform('highlight_alphas', rr_highlight_ga))
    #</editor-fold>
    #<editor-fold CustomJSTransform Definitions For Custom HoverTool:
    #Create the CustomJSTransforms that are used to update the y coordinates of
    #the centers of the invisible hitboxes used to determine the user's
    #highlighted data points.
    args_dict = dict(src = fig_src)
    hb1_gc = CustomJSTransform(args = args_dict, v_func = hb_gc_code(1))
    hb2_gc = CustomJSTransform(args = args_dict, v_func = hb_gc_code(2))
    hb3_gc = CustomJSTransform(args = args_dict, v_func = hb_gc_code(3))
    hb4_gc = CustomJSTransform(args = args_dict, v_func = hb_gc_code(4))
    hb5_gc = CustomJSTransform(args = args_dict, v_func = hb_gc_code(5))
    hb6_gc = CustomJSTransform(args = args_dict, v_func = hb_gc_code(6))
    #</editor-fold>
    #<editor-fold Plot Invisible Hitboxes:
    #Create the invisible hitboxes for the figure:
    hb1s = fig.rect(x = 'xs', y = transform('hb1', hb1_gc), source = fig_src,
                    width = 1, height = 'hb1', name = '5', fill_alpha = 0,
                    alpha = configs.hitbox_alpha)
    hb2s = fig.rect(x = 'xs', y = transform('hb2', hb2_gc), source = fig_src,
                    width = 1, height = 'hb2', name = '4', fill_alpha = 0,
                    alpha = configs.hitbox_alpha)
    hb3s = fig.rect(x = 'xs', y = transform('hb3', hb3_gc), source = fig_src,
                    width = 1, height = 'hb3', name = '3', fill_alpha = 0,
                    alpha = configs.hitbox_alpha)
    hb4s = fig.rect(x = 'xs', y = transform('hb4', hb4_gc), source = fig_src,
                    width = 1, height = 'hb4', name = '2', fill_alpha = 0,
                    alpha = configs.hitbox_alpha)
    hb5s = fig.rect(x = 'xs', y = transform('hb5', hb5_gc), source = fig_src,
                    width = 1, height = 'hb5', name = '1', fill_alpha = 0,
                    alpha = configs.hitbox_alpha)
    hb6s = fig.rect(x = 'xs', y = transform('hb6', hb6_gc), source = fig_src,
                    width = 1, height = 'hb6', name = '0', fill_alpha = 0,
                    alpha = configs.hitbox_alpha)
    #</editor-fold>
    #<editor-fold CustomJSHover Creation:
    #Create the CustomJSHovers used to format the data for the figure's
    #custom HoverTool:
    hover_main_args_dict = dict(src = fig_src, selectedIndex = selected_index)
    hover_xs_args_dict = hover_main_args_dict.copy()
    hover_xs_args_dict['highlightIndex'] = highlight_index

    xs_custom = CustomJSHover(code = xsCode, args = hover_xs_args_dict)
    ys_custom = CustomJSHover(code = ysCode, args = hover_main_args_dict)
    selected_custom = CustomJSHover(code = selectedCode,
                                    args = hover_main_args_dict)
    #</editor-fold>
    #<editor-fold Custom HoverTool Creation:
    #Create the Custom HoverTool and add it to the figure:
    hovertool_formatters = {'@xs' : xs_custom,
                            '@ll_ys' : ys_custom,
                            '@lm_ys' : selected_custom}
    fig.add_tools(HoverTool(tooltips = custom_tooltip,
                            formatters = hovertool_formatters,
                            mode = "mouse", point_policy = "follow_mouse",
                            renderers = [hb1s, hb2s, hb3s, hb4s, hb5s, hb6s]))
    #</editor-fold>
    game_parts.figures['stats_3'] = fig
    game_parts.sources['stats_fig_3'] = fig_src
#</editor-fold>
