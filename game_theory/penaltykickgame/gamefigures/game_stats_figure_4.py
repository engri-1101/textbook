from bokeh.plotting import figure
from bokeh.models import (CustomJSHover, ColumnDataSource, HoverTool,
                          CustomJSTransform)
from bokeh.transform import transform
r_probs = {'LeftLeft'   : 0.55, 'LeftMiddle'   : 0.65, 'LeftRight'   : 0.93,
           'MiddleLeft' : 0.74, 'MiddleMiddle' : 0.60, 'MiddleRight' : 0.72,
           'RightLeft'  : 0.95, 'RightMiddle'  : 0.73, 'RightRight'  : 0.70}
l_probs = {'LeftLeft'   : 0.67, 'LeftMiddle'   : 0.70, 'LeftRight'   : 0.96,
           'MiddleLeft' : 0.74, 'MiddleMiddle' : 0.60, 'MiddleRight' : 0.72,
           'RightLeft'  : 0.87, 'RightMiddle'  : 0.65, 'RightRight'  : 0.61}
score_probs = {'Right' : r_probs, 'Left' : l_probs}

footedness_dicts = ['Right', 'Left']
directions = ['Left', 'Middle', 'Right']
#<editor-fold fig_4_ys_custom:
ysCode = """
const index = special_vars.index;
const data = src.data;
const length = data['xs'].length;
data['highlight_alphas'].fill(0);
data['highlight_alphas'][index] = 1;
src.change.emit();
return data['ys'][index].toString();
"""
#</editor-fold>
#<editor-fold avgs_custom_code:
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
custom_tooltip = """
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
getAvgs = """
let newXs = [];
xs.forEach(
  (v, i) => (newXs.push((i !== 0) ? ((v + i * newXs[i - 1]) / (i + 1)) : v))
);

return newXs;
"""
#</editor-fold>

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
        self, fig_base_tools = "", fig_toolbar_loc = "below",
        fig_toolbar_sticky = False, fig_title = 'Score Chance Over Iterations',
        fig_width = 600, fig_height = 360, fig_x_range = (0.5, 50.5),
        fig_y_range = (0, 1), fig_initial_visibility = False,
        fig_title_font_size = '16pt', fig_x_axis_visibility = True,
        fig_y_axis_visibility = True,  fig_xgrid_line_color = None,
        fig_ygrid_line_color = None, fig_outline_line_color = None,
        fig_background_color = "white", plot_dot_line_color = "#D8CB2D",
        plot_dot_fill_color = "#ECDF41", plot_dot_size = 5, plot_dot_alpha = 1,
        guiding_line_color = "#000000", guiding_line_alpha = 0.1,
        hitbox_alpha = 0, plot_highlight_dot_size = 10,
        plot_highlight_dot_color = "#ECB841",
        plot_highlight_dot_outline_color = "#D8A42D",
        plot_avgs_line_color = "#000000"
    ):
        #<editor-fold figure:
        self.fig_base_tools = fig_base_tools
        self.fig_toolbar_loc = fig_toolbar_loc
        self.fig_toolbar_sticky = fig_toolbar_sticky
        self.fig_title = fig_title
        self.fig_width = fig_width
        self.fig_height = fig_height
        self.fig_x_range = fig_x_range
        self.fig_y_range = fig_y_range
        self.fig_initial_visibility = fig_initial_visibility
        self.fig_title_font_size = fig_title_font_size
        self.fig_x_axis_visibility = fig_x_axis_visibility
        self.fig_y_axis_visibility = fig_y_axis_visibility
        self.fig_xgrid_line_color = fig_xgrid_line_color
        self.fig_ygrid_line_color = fig_ygrid_line_color
        self.fig_outline_line_color = fig_outline_line_color
        self.fig_background_color = fig_background_color
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
def create(game_parts, configs = Configs()):
    fig = figure(
        tools = configs.fig_base_tools,
        toolbar_location = configs.fig_toolbar_loc,
        toolbar_sticky = configs.fig_toolbar_sticky, title = configs.fig_title,
        plot_width = configs.fig_width, plot_height = configs.fig_height,
        x_range = configs.fig_x_range, y_range = configs.fig_y_range,
        visible = configs.fig_initial_visibility
     )
    fig.title.text_font_size = configs.fig_title_font_size
    fig.xaxis.visible = configs.fig_x_axis_visibility
    fig.yaxis.visible = configs.fig_y_axis_visibility
    fig.xgrid.grid_line_color = configs.fig_xgrid_line_color
    fig.ygrid.grid_line_color = configs.fig_ygrid_line_color
    fig.outline_line_color = configs.fig_outline_line_color
    fig.background_fill_color = configs.fig_background_color

    #Create initial values for fig_src
    src_xs = []
    src_ys = []
    src_feet = []
    src_directions = []
    src_actions = []
    src_highlights = []
    src_avgs_placeholder = []
    #Fill the Lists
    for i in range(1, 51):
        src_xs.append(i)
        src_ys.append(0)
        src_feet.append(None)
        src_directions.append(None)
        src_actions.append(None)
        src_highlights.append(0)
        src_avgs_placeholder.append(0)
    #Create fig_src with the values that were created.
    src_data = dict(
        xs = src_xs,
        ys = src_ys,
        feet = src_feet,
        directions = src_directions,
        actions = src_actions,
        highlight_alphas = src_highlights,
        avgs_placeholder = src_avgs_placeholder
    )
    fig_src = ColumnDataSource(data = src_data)

    #Plot data points:
    fig.circle_dot(
        x = 'xs', y = 'ys', source = fig_src, size = configs.plot_dot_size,
        alpha = configs.plot_dot_alpha,
        line_color = configs.plot_dot_line_color,
        fill_color = configs.plot_dot_fill_color
    )
    fig.circle_dot(
        x = 'xs', y = 'ys', source = fig_src,
        size = configs.plot_highlight_dot_size, alpha = 'highlight_alphas',
        line_color = configs.plot_highlight_dot_outline_color,
        fill_color = configs.plot_highlight_dot_color
    )
    #Plot averages line:
    get_avgs = CustomJSTransform(v_func = getAvgs)
    avgs_line = fig.line(
        x = 'xs', y = transform('ys', get_avgs), source = fig_src,
        line_color = configs.plot_avgs_line_color
    )

    #Plot guiding lines:
    for foot in footedness_dicts:
        for direction in directions:
            for action in directions:
                y_val = score_probs[foot][direction + action]
                fig.line(
                    x = 'xs', y = y_val, source = fig_src,
                    line_color = configs.guiding_line_color,
                    line_alpha = configs.guiding_line_alpha
                )

    #Hitboxes:
    hbs = fig.rect(
        x = 'xs', y = 0.5, source = fig_src, width = 1, height = 1,
        fill_alpha = 0, line_alpha = configs.hitbox_alpha, line_color = "black"
    )

    #Custom HoverTool:
    hover_main_args_dict = dict(src = fig_src)
    ys_custom = CustomJSHover(code = ysCode, args = hover_main_args_dict)
    avgs_custom = CustomJSHover(code = avgsCode, args = hover_main_args_dict)
    hovertool_formatters = {'@ys' : ys_custom,
                            '@avgs_placeholder' : avgs_custom}
    hover_tool = HoverTool(
        tooltips = custom_tooltip, formatters = hovertool_formatters,
        mode = "mouse", point_policy = "follow_mouse", renderers = [hbs]
    )
    fig.add_tools(hover_tool)

    game_parts.figures['stats_4'] = fig
    game_parts.sources['stats_fig_4'] = fig_src
