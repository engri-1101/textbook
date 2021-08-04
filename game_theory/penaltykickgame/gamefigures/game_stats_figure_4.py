from . import figure_creation as fig_creation
from bokeh.models import (CustomJSHover, ColumnDataSource, HoverTool,
                          CustomJSTransform)
from bokeh.transform import transform

#<editor-fold ys code string:
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

#<editor-fold avgs code string:
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

#<editor-fold Get Avgs Code String:
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
    """Objects of this class are used to organize and pass parameters to
    Stats Figure 4. All arguments are mutable, and default values for them are
    the currently decided values being used to make the game. The main purpose
    of the configurability provided through the use of this class is to make it
    easier to test changes. Any changes that improve the game should be made
    directly to the default values of the arguments in this class after
    successful testing.
    """
    #<editor-fold __init__():
    def __init__(
        self, fig_base_tools="", fig_toolbar_loc="below",
        fig_toolbar_sticky=False, fig_title="Score Chance Over Iterations",
        fig_width=600, fig_height=360, fig_x_range=(0.5, 50.5),
        fig_y_range=(0, 1), fig_visibility=False,
        fig_sizing_mode="stretch_both", fig_outline_line_color=None,
        fig_background_color="white", fig_title_font_size="16pt",
        fig_x_axis_visibility=True, fig_y_axis_visibility=True,
        fig_x_axis_line_color="black", fig_y_axis_line_color="black",
        fig_xgrid_visibility=False, fig_ygrid_visibility=False,
        fig_xgrid_line_color="black", fig_ygrid_line_color="black",
        plot_dot_line_color="#D8CB2D", plot_dot_fill_color="#ECDF41",
        plot_dot_size=5, plot_dot_alpha=1, guiding_line_color="#000000",
        guiding_line_alpha=0.1, hitbox_alpha=0, plot_highlight_dot_size=10,
        plot_highlight_dot_color="#ECB841",
        plot_highlight_dot_outline_color="#D8A42D",
        plot_avgs_line_color="#000000"
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
    #</editor-fold>
#</editor-fold>

#<editor-fold create():
def create(game_parts, configs = Configs()):

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
        x="xs", y="ys", source=fig_src, size=configs.plot_dot_size,
        alpha=configs.plot_dot_alpha, line_color=configs.plot_dot_line_color,
        fill_color=configs.plot_dot_fill_color
    )

    fig.circle_dot(
        x="xs", y="ys", source=fig_src, size=configs.plot_highlight_dot_size,
        alpha="highlight_alphas",
        line_color=configs.plot_highlight_dot_outline_color,
        fill_color=configs.plot_highlight_dot_color
    )

    hbs = fig.rect(
        x="xs", y=0.5, source=fig_src, width=1, height=1, fill_alpha=0,
        line_alpha=configs.hitbox_alpha, line_color="black"
    )

    get_avgs = CustomJSTransform(v_func=getAvgs)

    avgs_line = fig.line(
        x="xs", y=transform("ys", get_avgs), source=fig_src,
        line_color=configs.plot_avgs_line_color
    )

    y_vals = [
        0.55, 0.65, 0.93, 0.74, 0.60, 0.72, 0.95, 0.73, 0.70,
        0.67, 0.70, 0.96, 0.74, 0.60, 0.72, 0.87, 0.65, 0.61
    ]
    for y_val in y_vals:
        fig.line(
            x="xs", y=y_val, source=fig_src,
            line_color=configs.guiding_line_color,
            line_alpha=configs.guiding_line_alpha
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
