from bokeh.plotting import figure
from bokeh.models import (CustomJSHover, ColumnDataSource, HoverTool,
                          CustomJSTransform)
from bokeh.transform import transform

score_probabilities = {'Right' : {'LeftLeft' :     0.55,
                                  'LeftMiddle' :   0.65,
                                  'LeftRight' :    0.93,
                                  'MiddleLeft' :   0.74,
                                  'MiddleMiddle' : 0.60,
                                  'MiddleRight' :  0.72,
                                  'RightLeft' :    0.95,
                                  'RightMiddle' :  0.73,
                                  'RightRight' :   0.70},
                       'Left' :  {'LeftLeft' :     0.67,
                                  'LeftMiddle' :   0.70,
                                  'LeftRight' :    0.96,
                                  'MiddleLeft' :   0.74,
                                  'MiddleMiddle' : 0.60,
                                  'MiddleRight' :  0.72,
                                  'RightLeft' :    0.87,
                                  'RightMiddle' :  0.65,
                                  'RightRight' :   0.61}};
footedness_dicts = ['Right', 'Left']
aim_directions = ['Left', 'Middle', 'Right']
goalie_actions = ['Left', 'Middle', 'Right']
#<editor-fold fig_4_ys_custom:
fig_4_ys_code = """
const index = special_vars.index;
const data = source.data;
const length = data['xs'].length;
data['highlight_alphas'] = new Array(length).fill(0);
data['highlight_alphas'][index] = 1;
source.change.emit();
return data['ys'][index].toString();"""
#</editor-fold>
#<editor-fold avgs_custom_code:
avgs_custom_code = """
const index = special_vars.index;
const data = source.data;
let val;

function avgRecursive(index){
    let val = data['ys'][index];
    if(index > 0){
        val += (index * avgRecursive(index - 1));
        val = val/(index + 1);
    }
    return val;
}

if(index == 0){
    val = data['ys'][0];
}
else{
    val = avgRecursive(index);
}
return (val.toString().substring(0,5));
"""
#</editor-fold>
#<editor-fold Custom Hover Tooltip:
fig_4_custom_tooltip="""
<div>
    <span style='font-size: 10px;'>Iteration:</span>
    <span style='font-size: 10px;'>@xs</span>
</div>
<div>
    <span style='font-size: 10px;'>Striker Foot:</span>
    <span style='font-size: 10px;'>@feet</span>
<div>
<div>
    <span style='font-size: 10px;'>Aim Direction:</span>
    <span style='font-size: 10px;'>@directions</span>
</div>
<div>
    <span style='font-size: 10px;'>Goalie Action:</span>
    <span style='font-size: 10px;'>@actions</span>
</div>
<div>
    <span style='font-size: 10px;'>Score Chance:</span>
    <span style='font-size: 10px;'>@ys{custom}</span>
</div>
<div>
    <span style='font-size: 10px;'>Avg Score Chance:</span>
    <span style='font-size: 10px;'>@avgs_placeholder{custom}</span>
</div>
"""
#</editor-fold>
#<editor-fold Get Average Code String:
get_averages = """
let new_xs = new Array(xs.length);
for(let i = 0; i < xs.length; i++){
    if(i == 0){
        new_xs[i] = xs[i];
    }
    else{
        new_xs[i] = (xs[i] + i * new_xs[i-1]) / (i + 1);
    }
}
return new_xs;
"""
#</editor-fold>

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
                 figure_background_color = "white",
                 plot_dot_line_color = "#D8CB2D",
                 plot_dot_fill_color = "#ECDF41",
                 plot_dot_size = 5, plot_dot_alpha = 1,
                 guiding_line_color = "#000000",
                 guiding_line_alpha = 0.1, hitbox_alpha = 0,
                 plot_highlight_dot_size = 10,
                 plot_highlight_dot_color = "#ECB841",
                 plot_highlight_dot_outline_color = "#D8A42D",
                 plot_avgs_line_color = "#000000"):
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
        self.plot_dot_line_color = plot_dot_line_color
        self.plot_dot_fill_color = plot_dot_fill_color
        self.plot_dot_size = plot_dot_size
        self.plot_dot_alpha = plot_dot_alpha
        self.guiding_line_color = guiding_line_color
        self.guiding_line_alpha = guiding_line_alpha
        self.hitbox_alpha = hitbox_alpha
        self.plot_highlight_dot_size = plot_highlight_dot_size
        self.plot_highlight_dot_color = plot_highlight_dot_color
        self.plot_highlight_dot_outline_color = plot_highlight_dot_outline_color
        self.plot_avgs_line_color = plot_avgs_line_color
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

    #Create initial values for game_stats_figure_4_source
    source_xs = []
    source_ys = []
    source_feet = []
    source_directions = []
    source_actions = []
    source_highlights = []
    source_avgs_placeholder = []
    #Fill the Lists
    for i in range(51):
        source_xs.append(i)
        source_ys.append(0)
        source_feet.append(None)
        source_directions.append(None)
        source_actions.append(None)
        source_highlights.append(0)
        source_avgs_placeholder.append(0)
    #Create game_stats_figure_4_source with the values that were created.
    source_data = dict(xs = source_xs,
                       ys = source_ys,
                       feet = source_feet,
                       directions = source_directions,
                       actions = source_actions,
                       highlight_alphas = source_highlights,
                       avgs_placeholder = source_avgs_placeholder)
    game_stats_figure_4_source = ColumnDataSource(data = source_data)

    #Plot data points:
    game_stats_figure_4.circle_dot('xs', 'ys',
                                   source = game_stats_figure_4_source,
                                   size = fig_configs.plot_dot_size,
                                   alpha = fig_configs.plot_dot_alpha,
                                   line_color = fig_configs.plot_dot_line_color,
                                   fill_color = fig_configs.plot_dot_fill_color)
    game_stats_figure_4.circle_dot('xs', 'ys',
                                   source = game_stats_figure_4_source,
                                   size = fig_configs.plot_highlight_dot_size,
                                   alpha = 'highlight_alphas',
                                   line_color = fig_configs.plot_highlight_dot_outline_color,
                                   fill_color = fig_configs.plot_highlight_dot_color)
    #Plot averages line:
    get_avgs = CustomJSTransform(v_func = get_averages)
    avgs_line = game_stats_figure_4.line('xs', transform('ys', get_avgs),
                                         source = game_stats_figure_4_source,
                                         line_color = fig_configs.plot_avgs_line_color)

    #Plot guiding lines:
    for foot in footedness_dicts:
        for direction in aim_directions:
            for action in goalie_actions:
                y_val = score_probabilities[foot][direction + action]
                game_stats_figure_4.line('xs', y_val,
                                         line_color = fig_configs.guiding_line_color,
                                         source = game_stats_figure_4_source,
                                         line_alpha = fig_configs.guiding_line_alpha)

    #Hitboxes:
    hbs = game_stats_figure_4.rect('xs', 0.5, source = game_stats_figure_4_source,
                                   width = 1, height = 1, fill_alpha = 0,
                                   line_alpha = fig_configs.hitbox_alpha,
                                   line_color = "black")

    #Custom HoverTool:
    hover_main_args_dict = dict(source = game_stats_figure_4_source)
    fig_4_ys_custom = CustomJSHover(code = fig_4_ys_code,
                                    args = hover_main_args_dict)
    fig_4_avgs_custom = CustomJSHover(code = avgs_custom_code,
                                      args = hover_main_args_dict)
    hovertool_formatters = {'@ys' : fig_4_ys_custom,
                            '@avgs_placeholder' : fig_4_avgs_custom}

    game_stats_figure_4.add_tools(HoverTool(tooltips = fig_4_custom_tooltip,
                                            formatters = hovertool_formatters,
                                            mode = "mouse",
                                            point_policy = "follow_mouse",
                                            renderers = [hbs]))
    return game_stats_figure_4, game_stats_figure_4_source