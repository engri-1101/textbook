from bokeh.plotting import figure
from bokeh.models import (CustomJSHover, ColumnDataSource, CustomJSTransform,
                          HoverTool, Div)
from bokeh.transform import transform

#Create a div used by the figure to determine the highlighted index for
#hovering.
highlight_index = Div(text = "0")

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
    #Create new_xs, the line of code that changes between hb v_funcs:
    new_xs = "new_xs[i] = xs[i]/2"

    #Create Source_dats to organize the possible additions to the new_xs line:
    source_dats = [" + source.data['hb1'][i]",
                   " + source.data['hb2'][i]",
                   " + source.data['hb3'][i]",
                   " + source.data['hb4'][i]",
                   " + source.data['hb5'][i]"]

    #Make necessary changes to new_xs:
    hbno -= 2
    while(hbno >= 0):
        new_xs += source_dats[hbno]
        hbno -= 1
    new_xs += ";"

    #Create and return the full code string:
    code_string = """
    let new_xs = new Array(xs.length);
    for(let i = 0; i < xs.length; i++){
        """ + new_xs + """
    }
    return new_xs;
    """
    return code_string
#</editor-fold>
#<editor-fold highlight_get_alpha Code Strings:
def sfga_get_alpha_code(sfga):
    """sfga_get_alpha_code is a function used to obtain the correct v_func code
    string for the CustomJSTransform being used to process the
    'highlight_alphas' column of stats_fig_3_source.data for use in
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
    highlight_val = sfgas.index(sfga) + 1
    highlight_val = str(highlight_val)

    #Create and return code string:
    code_string = """
    const index = parseInt(highlight_index.text);
    if(xs[index] == """ + highlight_val + """){
        let new_alphas = new Array(xs.length).fill(0);
        new_alphas[index] = 1;
        return new_alphas;
    }
    else{
        return alphas_zeroes;
    }
    """
    return code_string
#</editor-fold>
#<editor-fold Custom Hover Code Strings:
    #<editor-fold Shared Code String Parts:
#Selects the corresponding datapoint to the hovered hitbox.
select_sorted_value = """

const values = [data['ll_ys'][index],
                data['lm_ys'][index],
                data['lr_ys'][index],
                data['rl_ys'][index],
                data['rm_ys'][index],
                data['rr_ys'][index]];
let sorted_values = [data['ll_ys'][index],
                     data['lm_ys'][index],
                     data['lr_ys'][index],
                     data['rl_ys'][index],
                     data['rm_ys'][index],
                     data['rr_ys'][index]];
sorted_values = sorted_values.sort((a, b) => b - a);
let selected = column[values.indexOf(sorted_values[parseInt(name)])];

"""
#Setup code for the code string.
custom_hover_code_setup = """
let index = special_vars.index;
let name = special_vars.name;
let data = source.data;
const length = data['xs'].length;

"""
    #</editor-fold>
    #<editor-fold xs Code String:
    #obtains the iteration number of the selected data point and makes changes
    #necessary for the other hover functions and the highlighting functionality
    #of the figure.
fig_3_xs_code = custom_hover_code_setup + """
const column = [1, 2, 3, 4, 5, 6];
""" + select_sorted_value + """
data['highlight_alphas'][parseInt(highlight_index.text)] = 0;
highlight_index.text = index.toString();
data['highlight_alphas'][index] = selected;

source.change.emit();

return index.toString();
"""
    #</editor-fold>
    #<editor-fold ys Code String:
    #Obtains the y value of the selected data point.
fig_3_ys_code = custom_hover_code_setup + """
const column = ['ll', 'lm', 'lr', 'rl', 'rm', 'rr'];
""" + select_sorted_value + """
return(source.data[selected + "_ys"][index].toString().substring(0, 5));
"""
    #</editor-fold>
    #<editor-fold selected Code String:
    #Obtains the SF-GA associated with the selected data point
fig_3_selected_code = custom_hover_code_setup + """
const column = ['ll', 'lm', 'lr', 'rl', 'rm', 'rr'];
""" + select_sorted_value + """
return(selected);
"""
    #</editor-fold>
#</editor-fold>
#<editor-fold Custom Hover Tooltip Code String:
#Code below is for how the custom HoverTool displays the information.
#Note: some of the columns used by the hovertool don't need to actually be
#those columns (ll_ys, lm_ys). They were used because the hovertool needs an
#actual column in the source.
fig_3_custom_tooltip = """
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

#<editor-fold Stats_fig_3_configs():
class Stats_fig_3_configs():
    """Objects of this class are used to organize and pass parameters to
    Stats Figure 3. All arguments are mutable, and default values for them are
    the currently decided values being used to make the game. The main purpose
    of the configurability provided through the use of this class is to make it
    easier to test changes. Any changes that improve the game should be made
    directly to the default values of the arguments in this class after
    successful testing.
    """
    def __init__(self, figure_base_tools = "box_zoom, wheel_zoom, pan",
                 figure_toolbar_location = "below",
                 figure_title = "Goalie Perceived Risks Over Iterations",
                 figure_width = 600, figure_height = 360,
                 figure_x_range = (0, 50), figure_y_range = (0, 1),
                 figure_initial_visibility = False,
                 figure_sizing_mode = "stretch_both",
                 figure_title_font_size = '16pt',
                 figure_x_axis_visibility = True,
                 figure_y_axis_visibility = True,
                 figure_xgrid_line_color = None,
                 figure_ygrid_line_color = None,
                 figure_outline_line_color = None,
                 figure_background_color = "white",
                 plot_dot_size = 5,
                 plot_ll_dot_color = "#C8AFAF",
                 plot_lm_dot_color = "#C8C8AF",
                 plot_lr_dot_color = "#AFC8AF",
                 plot_rl_dot_color = "#AFC8C8",
                 plot_rm_dot_color = "#AFAFC8",
                 plot_rr_dot_color = "#C8AFC8",
                 plot_ll_dot_outline_color = "#AF9696",
                 plot_lm_dot_outline_color = "#AFAF96",
                 plot_lr_dot_outline_color = "#96AF96",
                 plot_rl_dot_outline_color = "#96AFAF",
                 plot_rm_dot_outline_color = "#9696AF",
                 plot_rr_dot_outline_color = "#AF96AF",
                 plot_highlight_dot_size = 10,
                 plot_highlight_dot_outline_color = "#000000",
                 plot_highlight_dot_color = "#000000",
                 hitbox_alpha = 0):
        #<editor-fold figure:
        self.figure_base_tools = figure_base_tools
        self.figure_toolbar_location = figure_toolbar_location
        self.figure_title = figure_title
        self.figure_width = figure_width
        self.figure_height = figure_height
        self.figure_x_range = figure_x_range
        self.figure_y_range = figure_y_range
        self.figure_initial_visibility = figure_initial_visibility
        self.figure_sizing_mode = figure_sizing_mode
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
def stats_figure_3_setup(game_parts, fig_configs = Stats_fig_3_configs()):
    """Fully creates and sets up stats figure 3 for use in the main game. Stats
    Figure 3 displays the goalie's perceived risks determined through
    fictitious play within the demo, according to game iteration.


    Keyword Argument:

    fig_configs - An oject of type Stats_fig_3_configs containing the user's
    desired figure values within its attributes.


    Returns:

    stats_fig_3 - The Game stats Bokeh figure displaying the data.

    stats_fig_3_source - The ColumnDataSource used by
    stats_fig_3.
    """
    #<editor-fold Figure Creation:
    #Create and configure the main aspects of the figure:
    stats_fig_3 = figure(tools = fig_configs.figure_base_tools,
                                 toolbar_location = fig_configs.figure_toolbar_location,
                                 title = fig_configs.figure_title,
                                 plot_width = fig_configs.figure_width,
                                 plot_height = fig_configs.figure_height,
                                 x_range = fig_configs.figure_x_range,
                                 y_range = fig_configs.figure_y_range,
                                 visible = fig_configs.figure_initial_visibility,
                                 sizing_mode = fig_configs.figure_sizing_mode)
    stats_fig_3.title.text_font_size = fig_configs.figure_title_font_size
    stats_fig_3.xaxis.visible = fig_configs.figure_x_axis_visibility
    stats_fig_3.yaxis.visible = fig_configs.figure_y_axis_visibility
    stats_fig_3.xgrid.grid_line_color = fig_configs.figure_xgrid_line_color
    stats_fig_3.ygrid.grid_line_color = fig_configs.figure_ygrid_line_color
    stats_fig_3.outline_line_color = fig_configs.figure_outline_line_color
    stats_fig_3.background_fill_color = fig_configs.figure_background_color
    #</editor-fold>
    #<editor-fold ColumnDataSource Creation:
        #<editor-fold Create Base Values:
        #Create initial values for stats_fig_3_source
    source_xs = []

    source_ll_ys = []
    source_lm_ys = []
    source_lr_ys = []
    source_rl_ys = []
    source_rm_ys = []
    source_rr_ys = []

    highlight_alphas = []
    alphas_zeroes = []

    source_hb1_ys = []
    source_hb2_ys = []
    source_hb3_ys = []
    source_hb4_ys = []
    source_hb5_ys = []
    source_hb6_ys = []

    for i in range(51):
        source_xs.append(i)

        source_ll_ys.append(0)
        source_lm_ys.append(0)
        source_lr_ys.append(0)
        source_rl_ys.append(0)
        source_rm_ys.append(0)
        source_rr_ys.append(0)

        highlight_alphas.append(0)
        alphas_zeroes.append(0)

        source_hb1_ys.append(0)
        source_hb2_ys.append(0)
        source_hb3_ys.append(0)
        source_hb4_ys.append(0)
        source_hb5_ys.append(0)
        source_hb6_ys.append(0)

    #Update Initial Values (Based off of data from table in lab key):
    source_ll_ys[0] = ((1/3 * 0.67) + (1/3 * 0.74) + (1/3 * 0.87))
    source_lm_ys[0] = ((1/3 * 0.70) + (1/3 * 0.60) + (1/3 * 0.65))
    source_lr_ys[0] = ((1/3 * 0.96) + (1/3 * 0.72) + (1/3 * 0.61))
    source_rl_ys[0] = ((1/3 * 0.55) + (1/3 * 0.74) + (1/3 * 0.95))
    source_rm_ys[0] = ((1/3 * 0.65) + (1/3 * 0.60) + (1/3 * 0.73))
    source_rr_ys[0] = ((1/3 * 0.93) + (1/3 * 0.72) + (1/3 * 0.70))
        #</editor-fold>
        #<editor-fold Make Data Source Using Base Values:
        #Create stats_fig_3_source with the values that were created.
    source_data = dict(xs = source_xs,

                       ll_ys = source_ll_ys, lm_ys = source_lm_ys,
                       lr_ys = source_lr_ys, rl_ys = source_rl_ys,
                       rm_ys = source_rm_ys, rr_ys = source_rr_ys,

                       hb1 = source_hb1_ys, hb2 = source_hb2_ys,
                       hb3 = source_hb3_ys, hb4 = source_hb4_ys,
                       hb5 = source_hb5_ys, hb6 = source_hb6_ys,

                       highlight_alphas = highlight_alphas,
                       alphas_zeroes = alphas_zeroes)

    stats_fig_3_source = ColumnDataSource(data = source_data)
        #</editor-fold>
    #</editor-fold>
    #<editor-fold Get Alpha Transforms:
    #Create the CustomJSTransforms that are used by the figure to update the
    #highlight dots according to the values contained within the
    #stats_fig_3_source column 'highlight_alphas'
    alpha_tform_args_dict = dict(highlight_index = highlight_index,
                                 alphas_zeroes = stats_fig_3_source.data['alphas_zeroes'])
    ll_highlight_get_alpha = CustomJSTransform(v_func = sfga_get_alpha_code('ll'),
                                               args = alpha_tform_args_dict)
    lm_highlight_get_alpha = CustomJSTransform(v_func = sfga_get_alpha_code('lm'),
                                               args = alpha_tform_args_dict)
    lr_highlight_get_alpha = CustomJSTransform(v_func = sfga_get_alpha_code('lr'),
                                               args = alpha_tform_args_dict)
    rl_highlight_get_alpha = CustomJSTransform(v_func = sfga_get_alpha_code('rl'),
                                               args = alpha_tform_args_dict)
    rm_highlight_get_alpha = CustomJSTransform(v_func = sfga_get_alpha_code('rm'),
                                               args = alpha_tform_args_dict)
    rr_highlight_get_alpha = CustomJSTransform(v_func = sfga_get_alpha_code('rr'),
                                               args = alpha_tform_args_dict)
    #</editor-fold>
    #<editor-fold Plot Figure Data Points:
    #Create the Data Points for the figure:
    stats_fig_3.circle_dot('xs', 'll_ys',
                                   source = stats_fig_3_source,
                                   size = fig_configs.plot_dot_size,
                                   line_color = fig_configs.plot_ll_dot_outline_color,
                                   fill_color = fig_configs.plot_ll_dot_color)
    stats_fig_3.circle_dot('xs', 'lm_ys',
                                   source = stats_fig_3_source,
                                   size = fig_configs.plot_dot_size,
                                   line_color = fig_configs.plot_lm_dot_outline_color,
                                   fill_color = fig_configs.plot_lm_dot_color)
    stats_fig_3.circle_dot('xs', 'lr_ys',
                                   source = stats_fig_3_source,
                                   size = fig_configs.plot_dot_size,
                                   line_color = fig_configs.plot_lr_dot_outline_color,
                                   fill_color = fig_configs.plot_lr_dot_color)
    stats_fig_3.circle_dot('xs', 'rl_ys',
                                   source = stats_fig_3_source,
                                   size = fig_configs.plot_dot_size,
                                   line_color = fig_configs.plot_rl_dot_outline_color,
                                   fill_color = fig_configs.plot_rl_dot_color)
    stats_fig_3.circle_dot('xs', 'rm_ys',
                                   source = stats_fig_3_source,
                                   size = fig_configs.plot_dot_size,
                                   line_color = fig_configs.plot_rm_dot_outline_color,
                                   fill_color = fig_configs.plot_rm_dot_color)
    stats_fig_3.circle_dot('xs', 'rr_ys',
                                   source = stats_fig_3_source,
                                   size = fig_configs.plot_dot_size,
                                   line_color = fig_configs.plot_rr_dot_outline_color,
                                   fill_color = fig_configs.plot_rr_dot_color)

    #Plot Highlight Points For Figure:
    stats_fig_3.circle_dot('xs', 'll_ys',
                                   source = stats_fig_3_source,
                                   size = fig_configs.plot_highlight_dot_size,
                                   line_color = fig_configs.plot_highlight_dot_outline_color,
                                   fill_color = fig_configs.plot_highlight_dot_color,
                                   alpha = transform('highlight_alphas',
                                                     ll_highlight_get_alpha))
    stats_fig_3.circle_dot('xs', 'lm_ys',
                                   source = stats_fig_3_source,
                                   size = fig_configs.plot_highlight_dot_size,
                                   line_color = fig_configs.plot_highlight_dot_outline_color,
                                   fill_color = fig_configs.plot_highlight_dot_color,
                                   alpha = transform('highlight_alphas',
                                                     lm_highlight_get_alpha))
    stats_fig_3.circle_dot('xs', 'lr_ys',
                                   source = stats_fig_3_source,
                                   size = fig_configs.plot_highlight_dot_size,
                                   line_color = fig_configs.plot_highlight_dot_outline_color,
                                   fill_color = fig_configs.plot_highlight_dot_color,
                                   alpha = transform('highlight_alphas',
                                                     lr_highlight_get_alpha))
    stats_fig_3.circle_dot('xs', 'rl_ys',
                                   source = stats_fig_3_source,
                                   size = fig_configs.plot_highlight_dot_size,
                                   line_color = fig_configs.plot_highlight_dot_outline_color,
                                   fill_color = fig_configs.plot_highlight_dot_color,
                                   alpha = transform('highlight_alphas',
                                                     rl_highlight_get_alpha))
    stats_fig_3.circle_dot('xs', 'rm_ys',
                                   source = stats_fig_3_source,
                                   size = fig_configs.plot_highlight_dot_size,
                                   line_color = fig_configs.plot_highlight_dot_outline_color,
                                   fill_color = fig_configs.plot_highlight_dot_color,
                                   alpha = transform('highlight_alphas',
                                                     rm_highlight_get_alpha))
    stats_fig_3.circle_dot('xs', 'rr_ys',
                                   source = stats_fig_3_source,
                                   size = fig_configs.plot_highlight_dot_size,
                                   line_color = fig_configs.plot_highlight_dot_outline_color,
                                   fill_color = fig_configs.plot_highlight_dot_color,
                                   alpha = transform('highlight_alphas',
                                                     rr_highlight_get_alpha))
    #</editor-fold>
    #<editor-fold CustomJSTransform Definitions For Custom HoverTool:
    #Create the CustomJSTransforms that are used to update the y coordinates of
    #the centers of the invisible hitboxes used to determine the user's
    #highlighted data points.
    hb_gc_args_dict = dict(source = stats_fig_3_source)
    hb1_get_center = CustomJSTransform(v_func = hb_gc_code(1))
    hb2_get_center = CustomJSTransform(args = hb_gc_args_dict,
                                       v_func = hb_gc_code(2))
    hb3_get_center = CustomJSTransform(args = hb_gc_args_dict,
                                       v_func = hb_gc_code(3))
    hb4_get_center = CustomJSTransform(args = hb_gc_args_dict,
                                       v_func = hb_gc_code(4))
    hb5_get_center = CustomJSTransform(args = hb_gc_args_dict,
                                       v_func = hb_gc_code(5))
    hb6_get_center = CustomJSTransform(args = hb_gc_args_dict,
                                       v_func = hb_gc_code(6))
    #</editor-fold>
    #<editor-fold Plot Invisible Hitboxes:
    #Create the invisible hitboxes for the figure:
    hb1s = stats_fig_3.rect(x = 'xs',
                                    y = transform('hb1', hb1_get_center),
                                    source = stats_fig_3_source,
                                    width = 1, height = 'hb1',
                                    alpha = fig_configs.hitbox_alpha,
                                    fill_alpha = 0, name = '5')
    hb2s = stats_fig_3.rect(x = 'xs',
                                    y = transform('hb2', hb2_get_center),
                                    source = stats_fig_3_source,
                                    width = 1, height = 'hb2',
                                    alpha = fig_configs.hitbox_alpha,
                                    fill_alpha = 0, name = '4')
    hb3s = stats_fig_3.rect(x = 'xs',
                                    y = transform('hb3', hb3_get_center),
                                    source = stats_fig_3_source,
                                    width = 1, height = 'hb3',
                                    alpha = fig_configs.hitbox_alpha,
                                    fill_alpha = 0, name = '3')
    hb4s = stats_fig_3.rect(x = 'xs',
                                    y = transform('hb4', hb4_get_center),
                                    source = stats_fig_3_source,
                                    width = 1, height = 'hb4',
                                    alpha = fig_configs.hitbox_alpha,
                                    fill_alpha = 0, name = '2')
    hb5s = stats_fig_3.rect(x = 'xs',
                                    y = transform('hb5', hb5_get_center),
                                    source = stats_fig_3_source,
                                    width = 1, height = 'hb5',
                                    alpha = fig_configs.hitbox_alpha,
                                    fill_alpha = 0, name = '1')
    hb6s = stats_fig_3.rect(x = 'xs',
                                    y = transform('hb6', hb6_get_center),
                                    source = stats_fig_3_source,
                                    width = 1, height = 'hb6',
                                    alpha = fig_configs.hitbox_alpha,
                                    fill_alpha = 0, name = '0')
    #</editor-fold>
    #<editor-fold CustomJSHover Creation:
    #Create the CustomJSHovers used to format the data for the figure's
    #custom HoverTool:
    hover_main_args_dict = dict(source = stats_fig_3_source)
    hover_xs_args_dict = hover_main_args_dict.copy()
    hover_xs_args_dict['highlight_index'] = highlight_index

    fig_3_xs_custom = CustomJSHover(code = fig_3_xs_code,
                                    args = hover_xs_args_dict)
    fig_3_ys_custom = CustomJSHover(code = fig_3_ys_code,
                                    args = hover_main_args_dict)
    fig_3_selected_custom = CustomJSHover(code = fig_3_selected_code,
                                          args = hover_main_args_dict)
    #</editor-fold>
    #<editor-fold Custom HoverTool Creation:
    #Create the Custom HoverTool and add it to the figure:
    hovertool_formatters = { '@xs' : fig_3_xs_custom,
                             '@ll_ys' : fig_3_ys_custom,
                             '@lm_ys' : fig_3_selected_custom}
    stats_fig_3.add_tools(HoverTool(tooltips = fig_3_custom_tooltip,
                                            formatters = hovertool_formatters,
                                            mode = "mouse",
                                            point_policy = "follow_mouse",
                                            renderers = [hb1s, hb2s, hb3s,
                                                         hb4s, hb5s, hb6s]))
    #</editor-fold>
    game_parts.figures['stats_3'] = stats_fig_3
    game_parts.sources['stats_fig_3'] = stats_fig_3_source
#</editor-fold>
