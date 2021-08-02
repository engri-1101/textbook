from bokeh.plotting import figure
from bokeh.models import (CustomJSHover, ColumnDataSource, CustomJSTransform,
                          HoverTool, Legend)
from bokeh.transform import transform

#<editor-fold hovered_ws_code_strings:
def bar_ws_code(bar_name):
    bar_names = ["scored", "blockedl", "blockedm", "blockedr"]
    bar_value = str(bar_names.index(bar_name) + 1)

    codeString = """
    const newXs = xs.map(
      (v) => ((v === """ + bar_value + """) ? 1 : 0.8)
    )
    return newXs;
    """
    return codeString
#</editor-fold>
#<editor-fold bar_cs_code_strings:
def bar_cs_code(bar_name):
    bar_names = ["scored", "blockedl", "blockedm", "blockedr"]
    bar_value = bar_names.index(bar_name) - 1
    calcNewXs = "newXs[i] = v/2"
    src_dats = [""" + src.data['scored_y'][i]""",
                """ + src.data['blockedl_y'][i]""",
                """ + src.data['blockedm_y'][i]""",
                """ + src.data['blockedr_y'][i]"""]

    while(bar_value >= 0):
        calcNewXs += src_dats[bar_value]
        bar_value -= 1

    #calcNewXs += ";"

    #Create and return the full code string:
    codeString = """
    const newXs = new Array(xs.length);
    xs.forEach(
      (v, i) => """ + calcNewXs + """
    );
    return newXs;
    """
    return codeString
#</editor-fold>

#<editor-fold xs code string:
xsCode = """
const kfkks = [
  '(L, L)', '(L, M)', '(L, R)',
  '(R, L)', '(R, M)', '(R, R)'
];
return kfkks[special_vars.index];
"""
#</editor-fold>
#<editor-fold Hovered Bar code string:
hoveredBarCode = """
return special_vars.name;
"""
#</editor-fold>
#<editor-fold Bar height code string:
barHeightCode = """
const barTypes = [
  'Scored',
  'Blocked Left',
  'Blocked Middle',
  'Blocked Right'
];
const columns = [
  'scored',
  'blockedl',
  'blockedm',
  'blockedr'
];
const wCodes = [1, 2, 3, 4];
const data = src.data;
const index = special_vars.index;
const selected = barTypes.indexOf(special_vars.name);

data['hovered_widths'].fill('');
data['hovered_widths'][index] = wCodes[selected];
src.change.emit();

const val = data[`${columns[selected]}_y`][index];
return val.toString();
"""
#</editor-fold>
#<editor-fold Custom HoverTool tooltip code string:
custom_tooltip = """
<div>
    <span style='font-size: 10px;'>Kicker (Foot, Kick):</span>
    <span style='font-size: 10px;'>@x{custom}</span>
</div>
<div>
    <span style='font-size: 10px;'>Hovered Bar:</span>
    <span style='font-size: 10px;'>@scored_y{custom}</span>
</div>
<div>
    <span style='font-size: 10px;'>Bar Height:</span>
    <span style='font-size: 10px;'>@blockedl_y{custom}</span>
</div>
"""
#</editor-fold>

#<editor-fold Stats_fig_1_configs
class Configs():
    def __init__(
        self, scored_bar_color = "#3F6750", blocked_left_bar_color = "#64A580",
        blocked_middle_bar_color = "#8AD3AA",
        blocked_right_bar_color = "#CBEBD9", ll_loc = 0.5, lm_loc = 1.5,
        lr_loc = 2.5, rl_loc = 3.5, rm_loc = 4.5, rr_loc = 5.5,
        bar_width = 0.9, fig_width = 600, fig_height = 360, fig_base_tools = "",
        fig_toolbar_loc = None, fig_title = 'Shot Status Statistics',
        fig_x_range = (0, 6), fig_y_range = (0, 50),
        fig_initial_visibility = False, fig_title_font_size = '16pt',
        fig_x_axis_visibility = False, fig_y_axis_visibility = True,
        fig_x_axis_line_color = None, fig_y_axis_line_color = None,
        fig_outline_line_color = None, fig_background_color = "white",
        bar_line_width = 0, leg1_width = 308, leg2_width = 464, leg1_y_loc = 20,
        leg2_y_loc = 40, leg_label_font_size = "10pt", leg_label_height = 10,
        leg_padding = 0, leg_border_line_alpha = 0,
        leg_background_fill_alpha = 0, hitbox_alpha = 0
    ):
        #<editor-fold bars:
        self.scored_bar_color = scored_bar_color
        self.blocked_left_bar_color = blocked_left_bar_color
        self.blocked_middle_bar_color = blocked_middle_bar_color
        self.blocked_right_bar_color = blocked_right_bar_color
        self.ll_loc = ll_loc
        self.lm_loc = lm_loc
        self.lr_loc = lr_loc
        self.rl_loc = rl_loc
        self.rm_loc = rm_loc
        self.rr_loc = rr_loc
        self.bar_width = bar_width
        #</editor-fold>>
        #<editor-fold figure:
        self.fig_width = fig_width
        self.fig_height = fig_height
        self.fig_base_tools = fig_base_tools
        self.fig_toolbar_loc = fig_toolbar_loc
        self.fig_title = fig_title
        self.fig_x_range = fig_x_range
        self.fig_y_range = fig_y_range
        self.fig_initial_visibility = fig_initial_visibility
        self.fig_title_font_size = fig_title_font_size
        self.fig_x_axis_visibility = fig_x_axis_visibility
        self.fig_y_axis_visibility = fig_y_axis_visibility
        self.fig_x_axis_line_color = fig_x_axis_line_color
        self.fig_y_axis_line_color = fig_y_axis_line_color
        self.fig_outline_line_color = fig_outline_line_color
        self.fig_background_color = fig_background_color
        #</editor-fold>
        #<editor-fold legends:
        self.leg1_width = leg1_width
        self.leg2_width = leg2_width
        self.bar_line_width = bar_line_width
        self.leg1_y_loc = leg1_y_loc
        self.leg2_y_loc = leg2_y_loc
        self.leg_label_font_size = leg_label_font_size
        self.leg_label_height = leg_label_height
        self.leg_padding = leg_padding
        self.leg_border_line_alpha = leg_border_line_alpha
        self.leg_background_fill_alpha = leg_background_fill_alpha
        #</editor-fold>
        self.hitbox_alpha = hitbox_alpha
#</editor-fold>

#<editor-fold stats_figure_1_setup:
def create(game_parts, configs = Configs()):
    #<editor-fold Create Figure:
    fig = figure(
        tools = configs.fig_base_tools,
        toolbar_location = configs.fig_toolbar_loc, title = configs.fig_title,
        plot_width = configs.fig_width, plot_height = configs.fig_height,
        x_range = configs.fig_x_range, y_range = configs.fig_y_range,
        visible = configs.fig_initial_visibility
    )

    fig.title.text_font_size = configs.fig_title_font_size
    #Configure Gridlines And Axes
    fig.xaxis.visible = configs.fig_x_axis_visibility
    fig.yaxis.visible = configs.fig_y_axis_visibility
    fig.xgrid.grid_line_color = configs.fig_x_axis_line_color
    fig.ygrid.grid_line_color = configs.fig_y_axis_line_color
    fig.outline_line_color = configs.fig_outline_line_color
        #Set Figure Background Color
    fig.background_fill_color = configs.fig_background_color
    #</editor-fold>
    #<editor-fold Create Legend:
    #Add shapes to represent colors (Cannot be seen as radius=0):
    l1scored = fig.circle(
        x = 0, y = 0, radius = 0, color = configs.scored_bar_color
    )
    l1blockedl = fig.circle(
        x = 0, y = 0, radius = 0, color = configs.blocked_left_bar_color
    )
    l2blockedm = fig.circle(
        x = 0, y = 0, radius = 0, color = configs.blocked_middle_bar_color
    )
    l2blockedr = fig.circle(
        x = 0, y = 0, radius = 0, color = configs.blocked_right_bar_color
    )
    #Create Legends, Configure Placement And Names:
    leg1_items = [("Scored", [l1scored]),
                  ("Goalie Blocked By Going Left", [l1blockedl])]
    leg1_loc = (int((configs.fig_width - configs.leg1_width) / 2),
                configs.leg1_y_loc)
    leg1 = Legend(
        items = leg1_items, orientation = "horizontal", location = leg1_loc,
        label_text_font_size = configs.leg_label_font_size,
        label_height = configs.leg_label_height, padding = configs.leg_padding,
        border_line_alpha = configs.leg_border_line_alpha,
        background_fill_alpha = configs.leg_background_fill_alpha
    )
    leg2_items = [("Goalie Blocked By Going Middle", [l2blockedm]),
                  ("Goalie Blocked By Going Right", [l2blockedr])]
    leg2_loc = (int((configs.fig_width - configs.leg2_width) / 2),
                configs.leg2_y_loc)
    leg2 = Legend(
        items = leg2_items, orientation = "horizontal", location = leg2_loc,
        label_text_font_size = configs.leg_label_font_size,
        label_height = configs.leg_label_height, padding = configs.leg_padding,
        border_line_alpha = configs.leg_border_line_alpha,
        background_fill_alpha = configs.leg_background_fill_alpha
    )
    fig.add_layout(leg1, "below")
    fig.add_layout(leg2, "below")
    #</editor-fold>
    #<editor-fold ColumnDataSource Creation:
    src_xs = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
    src_scored_ys = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    src_blockedl_ys = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    src_blockedm_ys = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    src_blockedr_ys = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    src_hovered_widths = ['' , '' , '' , '' , '' , '' ]

    src_data = dict(
        x = src_xs,
        scored_y = src_scored_ys,
        blockedl_y = src_blockedl_ys,
        blockedm_y = src_blockedm_ys,
        blockedr_y = src_blockedr_ys,
        hovered_widths = src_hovered_widths
    )
    fig_src = ColumnDataSource(src_data)
    #</editor-fold>
    #<editor-fold Create CustomJSTransforms:
    scored_gw = CustomJSTransform(v_func = bar_ws_code('scored'))
    blockedl_gw = CustomJSTransform(v_func = bar_ws_code('blockedl'))
    blockedm_gw = CustomJSTransform(v_func = bar_ws_code('blockedm'))
    blockedr_gw = CustomJSTransform(v_func = bar_ws_code('blockedr'))

    args_dict = dict(src = fig_src)
    scored_gcs = CustomJSTransform(
        v_func = bar_cs_code('scored'), args = args_dict
    )
    blockedl_gcs = CustomJSTransform(
        v_func = bar_cs_code('blockedl'), args = args_dict
    )
    blockedm_gcs = CustomJSTransform(
        v_func = bar_cs_code('blockedm'), args = args_dict
    )
    blockedr_gcs = CustomJSTransform(
        v_func = bar_cs_code('blockedr'), args = args_dict
    )
    #</editor-fold>
    #<editor-fold Create Hitbox Bars:
    score_hbs = fig.rect(
        x = 'x', y = transform('scored_y', scored_gcs), source = fig_src,
        width = 1, height = 'scored_y', alpha = configs.hitbox_alpha,
        fill_alpha = 0, name = "Scored", color = configs.scored_bar_color
    )
    blockedl_hbs = fig.rect(
        x = 'x', y = transform('blockedl_y', blockedl_gcs), source = fig_src,
        width = 1, height = 'blockedl_y', alpha = configs.hitbox_alpha,
        fill_alpha = 0, name = "Blocked Left",
        color = configs.blocked_left_bar_color
    )
    blockedm_hbs = fig.rect(
        x = 'x', y = transform('blockedm_y', blockedm_gcs), source = fig_src,
        width = 1, height = 'blockedm_y', alpha = configs.hitbox_alpha,
        fill_alpha = 0, name = "Blocked Middle",
        color = configs.blocked_middle_bar_color
    )
    blockedr_hbs = fig.rect(
        x = 'x', y = transform('blockedr_y', blockedr_gcs), source = fig_src,
        width = 1, height = 'blockedr_y', alpha = configs.hitbox_alpha,
        fill_alpha = 0, name = "Blocked Right",
        color = configs.blocked_right_bar_color
    )
    #</editor-fold>
    #<editor-fold Create Bars:
    score_bars = fig.rect(
        x = 'x', y = transform('scored_y', scored_gcs), source = fig_src,
        width = transform('hovered_widths', scored_gw), height = 'scored_y',
        color = configs.scored_bar_color
    )
    blockedl_bars = fig.rect(
        x = 'x', y = transform('blockedl_y', blockedl_gcs), source = fig_src,
        width = transform('hovered_widths', blockedl_gw), height = 'blockedl_y',
        color = configs.blocked_left_bar_color
    )
    blockedm_bars = fig.rect(
        x = 'x', y = transform('blockedm_y', blockedm_gcs), source = fig_src,
        width = transform('hovered_widths', blockedm_gw), height = 'blockedm_y',
        color = configs.blocked_middle_bar_color
    )
    blockedr_bars = fig.rect(
        x = 'x', y = transform('blockedr_y', blockedr_gcs), source = fig_src,
        width = transform('hovered_widths', blockedr_gw), height = 'blockedr_y',
        color = configs.blocked_right_bar_color
    )
    #</editor-fold>
    #<editor-fold Create CustomJSHovers:
    args_dict = dict(src = fig_src)

    xs_custom = CustomJSHover(code = xsCode)
    hovered_custom = CustomJSHover(code = hoveredBarCode)
    height_custom = CustomJSHover(code = barHeightCode, args = args_dict)
    #</editor-fold>
    #<editor-fold Create HoverTool:
    hovertool_formatters = {'@x' : xs_custom,
                            '@scored_y' : hovered_custom,
                            '@blockedl_y' : height_custom}
    hover_tool = HoverTool(
        tooltips = custom_tooltip, formatters = hovertool_formatters,
        mode = "mouse", point_policy = "follow_mouse",
        renderers = [score_hbs, blockedl_hbs, blockedm_hbs, blockedr_hbs]
    )
    fig.add_tools(hover_tool)
    game_parts.figures['stats_1'] = fig
    game_parts.sources['stats_fig_1'] = fig_src
    #</editor-fold>
 #</editor-fold>
