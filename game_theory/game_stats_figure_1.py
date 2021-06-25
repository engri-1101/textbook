from bokeh.plotting import figure
from bokeh.models import (CustomJSHover, ColumnDataSource, CustomJSTransform,
                          HoverTool, Legend)
from bokeh.transform import transform

#<editor-fold hovered_widths_code_strings:
def bar_width_code(bar_name):
    bar_names = ["scored", "blockedl", "blockedm", "blockedr"]
    bar_value = str(bar_names.index(bar_name) + 1)

    code_string = """
    let new_xs = new Array(xs.length);
    for(let i = 0; i < new_xs.length; i++){
        if(xs[i] == """ + bar_value + """){
            new_xs[i] = 1;
        }
        else{
            new_xs[i] = 0.8;
        }
    }
    return new_xs;
    """
    return code_string
#</editor-fold>
#<editor-fold bar_centers_code_strings:
def bar_centers_code(bar_name):
    bar_names = ["scored", "blockedl", "blockedm", "blockedr"]
    bar_value = bar_names.index(bar_name) - 1
    new_xs = "new_xs[i] = xs[i]/2"
    source_dats = [" + source.data['scored_y'][i]",
                   " + source.data['blockedl_y'][i]",
                   " + source.data['blockedm_y'][i]",
                   " + source.data['blockedr_y'][i]"]

    while(bar_value >= 0):
        new_xs += source_dats[bar_value]
        bar_value -= 1

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

#<editor-fold xs code string:
fig1_xs_code = """
const kfkks = ["(L, L)", "(L, M)", "(L, R)", "(R, L)", "(R, M)", "(R, R)"];
return kfkks[special_vars.index];
"""
#</editor-fold>
#<editor-fold Hovered Bar code string:
hovered_bar_code = """
return special_vars.name;
"""
#</editor-fold>
#<editor-fold Bar height code string:
bar_height_code = """
const bar_types = ["Scored", "Blocked Left", "Blocked Middle", "Blocked Right"];
const columns = ["scored", "blockedl", "blockedm", "blockedr"];
const width_codes = [1, 2, 3, 4];
const data = source.data;
const index = special_vars.index;
const selected = bar_types.indexOf(special_vars.name);

data['hovered_widths'] = new Array(6);
data['hovered_widths'][index] = width_codes[selected];
source.change.emit();
return data[columns[selected] + "_y"][index].toString();
"""
#</editor-fold>
#<editor-fold Custom HoverTool tooltip code string:
fig_1_custom_tooltip = """
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
class Stats_fig_1_configs():
    def __init__(self, scored_bar_color = "#3F6750",
                 blocked_left_bar_color = "#64A580",
                 blocked_middle_bar_color = "#8AD3AA",
                 blocked_right_bar_color = "#CBEBD9", figure_width = 600,
                 figure_height = 360, legend1_width = 308, legend2_width = 464,
                 ll_loc = 0.5, lm_loc = 1.5, lr_loc = 2.5, rl_loc = 3.5,
                 rm_loc = 4.5, rr_loc = 5.5, bar_width = 0.9,
                 figure_base_tools = "", figure_toolbar_location = None,
                 figure_title = 'Shot Status Statistics',
                 figure_x_range = (0, 6), figure_y_range = (0, 50),
                 figure_initial_visibility = False,
                 figure_title_font_size = '16pt',
                 figure_x_axis_visibility = False,
                 figure_y_axis_visibility = True,
                 figure_x_axis_line_color = None,
                 figure_y_axis_line_color = None,
                 figure_outline_line_color = None,
                 figure_background_color = "white", bar_line_width = 0,
                 legend1_y_loc = 20, legend2_y_loc = 40,
                 legend_label_font_size = "10pt", legend_label_height = 10,
                 legend_padding = 0, legend_border_line_alpha = 0,
                 legend_background_fill_alpha = 0, hitbox_alpha = 0):
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
        self.figure_width = figure_width
        self.figure_height = figure_height
        self.figure_base_tools = figure_base_tools
        self.figure_toolbar_location = figure_toolbar_location
        self.figure_title = figure_title
        self.figure_x_range = figure_x_range
        self.figure_y_range = figure_y_range
        self.figure_initial_visibility = figure_initial_visibility
        self.figure_title_font_size = figure_title_font_size
        self.figure_x_axis_visibility = figure_x_axis_visibility
        self.figure_y_axis_visibility = figure_y_axis_visibility
        self.figure_x_axis_line_color = figure_x_axis_line_color
        self.figure_y_axis_line_color = figure_y_axis_line_color
        self.figure_outline_line_color = figure_outline_line_color
        self.figure_background_color = figure_background_color
        #</editor-fold>
        #<editor-fold legends:
        self.legend1_width = legend1_width
        self.legend2_width = legend2_width
        self.bar_line_width = bar_line_width
        self.legend1_y_loc = legend1_y_loc
        self.legend2_y_loc = legend2_y_loc
        self.legend_label_font_size = legend_label_font_size
        self.legend_label_height = legend_label_height
        self.legend_padding = legend_padding
        self.legend_border_line_alpha = legend_border_line_alpha
        self.legend_background_fill_alpha = legend_background_fill_alpha
        #</editor-fold>
        self.hitbox_alpha = hitbox_alpha
#</editor-fold>

#<editor-fold stats_figure_1_setup:
def stats_figure_1_setup(fig_configs):
    #<editor-fold Create Figure:
    game_stats_figure_1 = figure(tools = fig_configs.figure_base_tools,
                                 toolbar_location = fig_configs.figure_toolbar_location,
                                 title = fig_configs.figure_title,
                                 plot_width = fig_configs.figure_width,
                                 plot_height = fig_configs.figure_height,
                                 x_range = fig_configs.figure_x_range,
                                 y_range = fig_configs.figure_y_range,
                                 visible = fig_configs.figure_initial_visibility)

    game_stats_figure_1.title.text_font_size = fig_configs.figure_title_font_size
    #Configure Gridlines And Axes
    game_stats_figure_1.xaxis.visible = fig_configs.figure_x_axis_visibility
    game_stats_figure_1.yaxis.visible = fig_configs.figure_y_axis_visibility
    game_stats_figure_1.xgrid.grid_line_color = fig_configs.figure_x_axis_line_color
    game_stats_figure_1.ygrid.grid_line_color = fig_configs.figure_y_axis_line_color
    game_stats_figure_1.outline_line_color = fig_configs.figure_outline_line_color
        #Set Figure Background Color
    game_stats_figure_1.background_fill_color = fig_configs.figure_background_color
    #</editor-fold>
    #<editor-fold Create Legend:
    #Add shapes to represent colors (Cannot be seen as radius=0):
    l1scored = game_stats_figure_1.circle(x = 0, y = 0, radius = 0,
                                          color = fig_configs.scored_bar_color)
    l1blockedl = game_stats_figure_1.circle(x = 0, y = 0, radius = 0,
                                            color = fig_configs.blocked_left_bar_color)
    l2blockedm = game_stats_figure_1.circle(x = 0, y = 0, radius = 0,
                                            color = fig_configs.blocked_middle_bar_color)
    l2blockedr = game_stats_figure_1.circle(x = 0, y = 0, radius = 0,
                                            color = fig_configs.blocked_right_bar_color)
    #Create Legends, Configure Placement And Names:
    legend1 = Legend(items = [("Scored", [l1scored]),
                              ("Goalie Blocked By Going Left", [l1blockedl])],
                     orientation = "horizontal",
                     location = (int((fig_configs.figure_width
                                      - fig_configs.legend1_width) / 2),
                                     fig_configs.legend1_y_loc),
                     label_text_font_size = fig_configs.legend_label_font_size,
                     label_height = fig_configs.legend_label_height,
                     padding = fig_configs.legend_padding,
                     border_line_alpha = fig_configs.legend_border_line_alpha,
                     background_fill_alpha = fig_configs.legend_background_fill_alpha)
    legend2 = Legend(items = [("Goalie Blocked By Going Middle", [l2blockedm]),
                              ("Goalie Blocked By Going Right", [l2blockedr])],
                     orientation = "horizontal",
                     location = (int((fig_configs.figure_width
                                      - fig_configs.legend2_width) / 2),
                                 fig_configs.legend2_y_loc),
                     label_text_font_size = fig_configs.legend_label_font_size,
                     label_height = fig_configs.legend_label_height,
                     padding = fig_configs.legend_padding,
                     border_line_alpha = fig_configs.legend_border_line_alpha,
                     background_fill_alpha = fig_configs.legend_background_fill_alpha)
    game_stats_figure_1.add_layout(legend1, "below")
    game_stats_figure_1.add_layout(legend2, "below")
    #</editor-fold>
    #<editor-fold ColumnDataSource Creation:
    figure_1_source_xs =             [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
    figure_1_source_scored_ys =      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    figure_1_source_blockedl_ys =    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    figure_1_source_blockedm_ys =    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    figure_1_source_blockedr_ys =    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    figure_1_source_hovered_widths = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    game_stats_figure_1_data = dict(x = figure_1_source_xs,
                                    scored_y = figure_1_source_scored_ys,
                                    blockedl_y = figure_1_source_blockedl_ys,
                                    blockedm_y = figure_1_source_blockedm_ys,
                                    blockedr_y = figure_1_source_blockedr_ys,
                                    hovered_widths = figure_1_source_hovered_widths)
    game_stats_figure_1_source = ColumnDataSource(game_stats_figure_1_data)
    #</editor-fold>
    #<editor-fold Create CustomJSTransforms:
    scored_get_width = CustomJSTransform(v_func = bar_width_code('scored'))
    blockedl_get_width = CustomJSTransform(v_func = bar_width_code('blockedl'))
    blockedm_get_width = CustomJSTransform(v_func = bar_width_code('blockedm'))
    blockedr_get_width = CustomJSTransform(v_func = bar_width_code('blockedr'))

    args_dict = dict(source = game_stats_figure_1_source)
    scored_get_centers = CustomJSTransform(v_func = bar_centers_code('scored'),
                                           args = args_dict)
    blockedl_get_centers = CustomJSTransform(v_func = bar_centers_code('blockedl'),
                                             args = args_dict)
    blockedm_get_centers = CustomJSTransform(v_func = bar_centers_code('blockedm'),
                                             args = args_dict)
    blockedr_get_centers = CustomJSTransform(v_func = bar_centers_code('blockedr'),
                                             args = args_dict)
    #</editor-fold>
    #<editor-fold Create Hitbox Bars:
    score_hbs = game_stats_figure_1.rect(x = 'x',
                                         y = transform('scored_y',
                                                       scored_get_centers),
                                         source = game_stats_figure_1_source,
                                         width = 1, height = 'scored_y',
                                         alpha = fig_configs.hitbox_alpha,
                                         fill_alpha = 0, name = "Scored",
                                         color = fig_configs.scored_bar_color)
    blockedl_hbs = game_stats_figure_1.rect(x = 'x',
                                            y = transform('blockedl_y',
                                                          blockedl_get_centers),
                                            source = game_stats_figure_1_source,
                                            width = 1, height = 'blockedl_y',
                                            alpha = fig_configs.hitbox_alpha,
                                            fill_alpha = 0, name = "Blocked Left",
                                            color = fig_configs.blocked_left_bar_color)
    blockedm_hbs = game_stats_figure_1.rect(x = 'x',
                                            y = transform('blockedm_y',
                                                          blockedm_get_centers),
                                            source = game_stats_figure_1_source,
                                            width = 1, height = 'blockedm_y',
                                            alpha = fig_configs.hitbox_alpha,
                                            fill_alpha = 0, name = "Blocked Middle",
                                            color = fig_configs.blocked_middle_bar_color)
    blockedr_hbs = game_stats_figure_1.rect(x = 'x',
                                            y = transform('blockedr_y',
                                                          blockedr_get_centers),
                                            source = game_stats_figure_1_source,
                                            width = 1, height = 'blockedr_y',
                                            alpha = fig_configs.hitbox_alpha,
                                            fill_alpha = 0, name = "Blocked Right",
                                            color = fig_configs.blocked_right_bar_color)
    #</editor-fold>
    #<editor-fold Create Bars:
    score_bars = game_stats_figure_1.rect(x = 'x',
                                          y = transform('scored_y',
                                                        scored_get_centers),
                                          source = game_stats_figure_1_source,
                                          width = transform('hovered_widths',
                                                            scored_get_width),
                                          height = 'scored_y',
                                          color = fig_configs.scored_bar_color)
    blockedl_bars = game_stats_figure_1.rect(x = 'x',
                                             y = transform('blockedl_y',
                                                           blockedl_get_centers),
                                             source = game_stats_figure_1_source,
                                             width = transform('hovered_widths',
                                                               blockedl_get_width),
                                             height = 'blockedl_y',
                                             color = fig_configs.blocked_left_bar_color)
    blockedm_bars = game_stats_figure_1.rect(x = 'x',
                                             y = transform('blockedm_y',
                                                           blockedm_get_centers),
                                             source = game_stats_figure_1_source,
                                             width = transform('hovered_widths',
                                                               blockedm_get_width),
                                             height = 'blockedm_y',
                                             color = fig_configs.blocked_middle_bar_color)
    blockedr_bars = game_stats_figure_1.rect(x = 'x',
                                             y = transform('blockedr_y',
                                                           blockedr_get_centers),
                                             source = game_stats_figure_1_source,
                                             width = transform('hovered_widths',
                                                               blockedr_get_width),
                                             height = 'blockedr_y',
                                             color = fig_configs.blocked_right_bar_color)
    #</editor-fold>
    #<editor-fold Create CustomJSHovers:
    height_args_dict = dict(source = game_stats_figure_1_source)

    fig_1_xs_custom = CustomJSHover(code = fig1_xs_code)
    fig_1_hovered_custom = CustomJSHover(code = hovered_bar_code)
    fig_1_height_custom = CustomJSHover(code = bar_height_code,
                                        args = height_args_dict)
    #</editor-fold>
    #<editor-fold Create HoverTool:
    hovertool_formatters = { '@x' : fig_1_xs_custom,
                             '@scored_y' : fig_1_hovered_custom,
                             '@blockedl_y' : fig_1_height_custom}
    game_stats_figure_1.add_tools(HoverTool(tooltips = fig_1_custom_tooltip,
                                            formatters = hovertool_formatters,
                                            mode = "mouse",
                                            point_policy = "follow_mouse",
                                            renderers = [score_hbs,
                                                         blockedl_hbs,
                                                         blockedm_hbs,
                                                         blockedr_hbs]))
    return(game_stats_figure_1, game_stats_figure_1_source)
    #</editor-fold>
 #</editor-fold>
