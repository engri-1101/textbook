from . import figure_creation as fig_creation
# from bokeh.plotting import figure
from bokeh.models import (CustomJSHover, ColumnDataSource, CustomJSTransform,
                          HoverTool, Legend)
from bokeh.transform import transform
BAR_NAMES = ["scored", "blockedl", "blockedm", "blockedr"]
#<editor-fold hovered_ws_code_strings:
def bar_ws_code(bar_name):
    bar_value = str(BAR_NAMES.index(bar_name) + 1)

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
    bar_value = BAR_NAMES.index(bar_name) - 1
    calcNewXs = "newXs[i] = v/2"
    src_dats = [
        """ + src.data["scored_y"][i]""", """ + src.data["blockedl_y"][i]""",
        """ + src.data["blockedm_y"][i]""", """ + src.data["blockedr_y"][i]"""
    ]

    while(bar_value >= 0):
        calcNewXs += src_dats[bar_value]
        bar_value -= 1

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
const kfkks = ['(L, L)', '(L, M)', '(L, R)', '(R, L)', '(R, M)', '(R, R)'];
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
const barTypes = ['Scored', 'Blocked Left', 'Blocked Middle', 'Blocked Right'];
const columns = ['scored', 'blockedl', 'blockedm', 'blockedr'];
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
        self, bar_colors=["#3F6750", "#64A580", "#8AD3AA", "#CBEBD9"],
        bar_width=0.9, fig_base_tools="", fig_toolbar_loc=None,
        fig_toolbar_sticky=False, fig_title="Shot Status Statistics",
        fig_width=600, fig_height=360, fig_x_range=(0, 6), fig_y_range=(0, 50),
        fig_visibility=False, fig_sizing_mode="stretch_both",
        fig_outline_line_color=None, fig_background_color="white",
        fig_title_font_size="16pt", fig_x_axis_visibility=False,
        fig_y_axis_visibility=True, fig_x_axis_line_color="black",
        fig_y_axis_line_color="black", fig_xgrid_visibility=False,
        fig_ygrid_visibility=False, fig_xgrid_line_color="black",
        fig_ygrid_line_color="black", leg1_width=308, leg2_width=464,
        leg1_y_loc=20, leg2_y_loc=40, leg_label_font_size="10pt",
        leg_label_height=10, leg_padding=0, leg_border_line_alpha=0,
        leg_background_fill_alpha=0, hitbox_alpha=0
    ):
        #<editor-fold bars:
        self.bar_colors = bar_colors
        self.bar_width = bar_width
        #</editor-fold>>
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
        #<editor-fold legends:
        self.leg_widths = [leg1_width, leg2_width]
        self.leg_y_locs = [leg1_y_loc, leg2_y_loc]
        self.leg_label_font_size = leg_label_font_size
        self.leg_label_height = leg_label_height
        self.leg_padding = leg_padding
        self.leg_border_line_alpha = leg_border_line_alpha
        self.leg_background_fill_alpha = leg_background_fill_alpha
        #</editor-fold>
        self.hitbox_alpha = hitbox_alpha
#</editor-fold>

#<editor-fold stats_figure_1_setup:
def create(game_parts, configs=Configs()):
    fig = fig_creation.make_fig(configs.fig)

    #<editor-fold Create Legend:
    #Add shapes to represent colors (Cannot be seen as radius=0):
    color_circles = []
    for i in range(4):
        color_circle = fig.circle(
            x=0, y=0, radius=0, color=configs.bar_colors[i]
        )
        color_circles.append(color_circle)

    #Create Legends, Configure Placement And Names:
    leg_item_texts = [
        "Scored", "Goalie Blocked By Going Left",
        "Goalie Blocked By Going Middle", "Goalie Blocked By Going Right"
    ]
    legs = []
    for i in range(2):
        item_1 = (leg_item_texts[2 * i], [color_circles[2 * i]])
        item_2 = (leg_item_texts[2*i + 1], [color_circles[2*i + 1]])
        leg_items = [item_1, item_2]
        loc_x = int((configs.fig.width - configs.leg_widths[i]) / 2)
        leg_loc = (loc_x, configs.leg_y_locs[i])
        leg = Legend(
            items=leg_items, orientation="horizontal", location=leg_loc,
            label_text_font_size=configs.leg_label_font_size,
            label_height=configs.leg_label_height, padding=configs.leg_padding,
            border_line_alpha=configs.leg_border_line_alpha,
            background_fill_alpha=configs.leg_background_fill_alpha
        )
        legs.append(leg)

    fig.add_layout(legs[0], "below")
    fig.add_layout(legs[1], "below")
    #</editor-fold>

    #<editor-fold ColumnDataSource Creation:
    src_data = dict(
        x = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5],
        scored_y = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        blockedl_y = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        blockedm_y = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        blockedr_y = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        hovered_widths = ["", "", "", "", "", ""]
    )
    fig_src = ColumnDataSource(src_data)
    #</editor-fold>

    #<editor-fold CustomJSTransform Creation:
    gcs = []
    gws = []

    args_dict = dict(src=fig_src)
    for i in range(4):
        gc = CustomJSTransform(
            v_func=bar_cs_code(BAR_NAMES[i]), args=args_dict
        )
        gcs.append(gc)
        gw = CustomJSTransform(v_func=bar_ws_code(BAR_NAMES[i]))
        gws.append(gw)
    #</editor-fold>

    #<editor-fold Plot Figure Elements:
    hbs = []
    bars = []

    hb_ids = ["scored_y", "blockedl_y", "blockedm_y", "blockedr_y"]
    hb_names = ["Scored", "Blocked Left", "Blocked Middle", "Blocked Right"]
    for i in range(4):
        hb = fig.rect(
            x="x", y=transform(hb_ids[i], gcs[i]), source=fig_src, width=1,
            height=hb_ids[i], alpha=configs.hitbox_alpha, fill_alpha=0,
            name=hb_names[i], color=configs.bar_colors[i]
        )
        hbs.append(hb)
        bar = fig.rect(
            x="x", y=transform(hb_ids[i], gcs[i]), source=fig_src,
            width=transform("hovered_widths", gws[i]), height=hb_ids[i],
            color=configs.bar_colors[i]
        )
        bars.append(bar)
    #</editor-fold>

    #<editor-fold Create HoverTool:
    args_dict = dict(src = fig_src)
    xs_custom = CustomJSHover(code=xsCode)
    hovered_custom = CustomJSHover(code=hoveredBarCode)
    height_custom = CustomJSHover(code=barHeightCode, args=args_dict)

    hovertool_formatters = {"@x" : xs_custom,
                            "@scored_y" : hovered_custom,
                            "@blockedl_y" : height_custom}
    hover_tool = HoverTool(
        tooltips=custom_tooltip, formatters=hovertool_formatters,
        mode="mouse", point_policy="follow_mouse", renderers=hbs
    )
    fig.add_tools(hover_tool)
    game_parts.figures["stats_1"] = fig
    game_parts.sources["stats_fig_1"] = fig_src
    #</editor-fold>
 #</editor-fold>
