from bokeh.plotting import figure
from bokeh.models import (CustomJSHover, ColumnDataSource,
                          Rect, Legend, Circle, HoverTool)

#<editor-fold Custom HoverTool tooltip code string:
fig_1_custom_tooltip = """

    <div @hovershow{custom}>
        <span style='font-size: 10px;'>Closest Data Coords:</span>
        <span style='font-size: 10px;'>@hoverxy{custom}</span>
    </div>
    <div @hovershow{custom}>
        <span style='font-size: 10px;'>Closest Data:</span>
        <span style='font-size: 10px;'>@hoverhovering{custom}</span>
    </div>
    <div @hovershow{custom}>
        <span style='font-size: 10px;'>Hovered (x,y):</span>
        <span style='font-size: 10px;'>($x,$y)</span>
    </div>

"""
#</editor-fold>
#<editor-fold CustomJSHover Code Strings:
    #<editor-fold custom_hover_coordinates_code:
custom_hover_coordinates_code = """
var x = special_vars.x;
var y = special_vars.y;

var modified_x;
var modified_y;
var index = 0;

const data = game_stats_figure_1_source.data;

for(var i = 6; i >= 1; i--){
    if(x < i){
        modified_x = (i - 0.5);
        index = (3*i - 2);
    }
}

var closest_y;

var scored_val = data['scored_y'][index];
var blockedl_val = data['blockedl_y'][index];
var blockedm_val = data['blockedm_y'][index];
var blockedr_val = data['blockedr_y'][index];

closest_y = scored_val;

if((y > closest_y
    && blockedl_val != scored_val)){
    closest_y = blockedl_val;
}
if((y > closest_y
    && blockedm_val != blockedl_val)){
    closest_y = blockedm_val;
}
if((y > closest_y
    && blockedr_val != blockedm_val)){
    closest_y = blockedr_val;
}


modified_y = closest_y;

return("(" + modified_x.toString() + ","
       + modified_y.toString() + ")" );
"""
    #</editor-fold>
    #<editor-fold custom_hover_hovering_code:
custom_hover_hovering_code = """
var x = special_vars.x;
var y = special_vars.y;

var modified_x;
var modified_y;
var index = 0;

const data = game_stats_figure_1_source.data;

for(var i = 6; i >= 1; i--){
    if(x < i){
        modified_x = (i - 0.5);
        index = (3*i - 2);
    }
}

var closest_y;

var scored_val = data['scored_y'][index];
var blockedl_val = data['blockedl_y'][index];
var blockedm_val = data['blockedm_y'][index];
var blockedr_val = data['blockedr_y'][index];

closest_y = scored_val;
var hovering = "Scored";

if((y > closest_y
    && blockedl_val != scored_val)){
    closest_y = blockedl_val;
    hovering = "Goalie Left";
}
if((y > closest_y
    && blockedm_val != blockedl_val)){
    closest_y = blockedm_val;
    hovering = "Goalie Middle";
}
if((y > closest_y
    && blockedr_val != blockedm_val)){
    closest_y = blockedr_val;
    hovering = "Goalie Right";
}

return(hovering);
"""
    #</editor-fold>
    #<editor-fold custom_hover_code:
custom_hover_code = """
var index = special_vars.index;
const data = game_stats_figure_1_source.data;

if(data['hovershow'][index] == 0){
    return " hidden ";
}

var y = special_vars.y;

var closest_y;

var scored_val = data['scored_y'][index];
var blockedl_val = data['blockedl_y'][index];
var blockedm_val = data['blockedm_y'][index];
var blockedr_val = data['blockedr_y'][index];

closest_y = scored_val;
var hovering = "scored_y";

if((y > closest_y
    && blockedl_val != scored_val)){
    closest_y = blockedl_val;
    hovering = "blockedl_y";
}
if((y > closest_y
    && blockedm_val != blockedl_val)){
    closest_y = blockedm_val;
    hovering = "blockedm_y";
}
if((y > closest_y
    && blockedr_val != blockedm_val)){
    closest_y = blockedr_val;
    hovering = "blockedr_y";
}

if(special_vars.name != hovering){
    return " hidden ";
}

return " ";
"""
    #</editor-fold>
#</editor-fold>

#<editor-fold Stats_fig_1_configs():
class Stats_fig_1_configs():
    def __init__(self, scored_bar_color = "#3F6750",
                 blocked_left_bar_color = "#64A580",
                 blocked_middle_bar_color = "#8AD3AA",
                 blocked_right_bar_color = "#CBEBD9", figure_width = 300,
                 figure_height = 240, legend1_width = 191, legend2_width = 267,
                 ll_loc = 0.5, lm_loc = 1.5, lr_loc = 2.5, rl_loc = 3.5,
                 rm_loc = 4.5, rr_loc = 5.5, bar_width = 0.9,
                 figure_base_tools = "", figure_toolbar_location = None,
                 figure_title = 'Shot Status Statistics',
                 figure_x_range = (0, 6), figure_y_range = (0, 50),
                 figure_initial_visibility = False,
                 figure_title_font_size = '8pt',
                figure_x_axis_visibility = False,
                 figure_y_axis_visibility = True,
                 figure_x_axis_line_color = None,
                 figure_y_axis_line_color = None,
                 figure_outline_line_color = None,
                 figure_background_color = "white", bar_line_width = 0,
                 legend1_y_loc = 22, legend2_y_loc = 50,
                 legend_label_font_size = "5pt", legend_label_height = 10,
                 legend_padding = 0, legend_border_line_alpha = 0,
                 legend_background_fill_alpha = 0):
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
#</editor-fold>

#<editor-fold stats_figure_1_setup
def stats_figure_1_setup(fig_configs):
    #<editor-fold Figure Creation:
    #Create Figure
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
    #<editor-fold Data Bar Definitions:
        #<editor-fold Score Data Bars:
    ll_scored_bar = Rect(x = fig_configs.ll_loc, y = 0,
                         width = fig_configs.bar_width, height = 0,
                         angle = 0, fill_color = fig_configs.scored_bar_color,
                         line_width = fig_configs.bar_line_width)
    lm_scored_bar = Rect(x = fig_configs.lm_loc, y = 0,
                         width = fig_configs.bar_width, height = 0,
                         angle = 0, fill_color = fig_configs.scored_bar_color,
                         line_width = fig_configs.bar_line_width)
    lr_scored_bar = Rect(x = fig_configs.lr_loc, y = 0,
                         width = fig_configs.bar_width, height = 0,
                         angle = 0, fill_color = fig_configs.scored_bar_color,
                         line_width = fig_configs.bar_line_width)
    rl_scored_bar = Rect(x = fig_configs.rl_loc, y = 0,
                         width = fig_configs.bar_width, height = 0,
                         angle = 0, fill_color = fig_configs.scored_bar_color,
                         line_width = fig_configs.bar_line_width)
    rm_scored_bar = Rect(x = fig_configs.rm_loc, y = 0,
                         width = fig_configs.bar_width, height = 0,
                         angle = 0, fill_color = fig_configs.scored_bar_color,
                         line_width = fig_configs.bar_line_width)
    rr_scored_bar = Rect(x = fig_configs.rr_loc, y = 0,
                         width = fig_configs.bar_width, height = 0,
                         angle = 0, fill_color = fig_configs.scored_bar_color,
                         line_width = fig_configs.bar_line_width)

    game_stats_figure_1.add_glyph(ll_scored_bar)
    game_stats_figure_1.add_glyph(lm_scored_bar)
    game_stats_figure_1.add_glyph(lr_scored_bar)
    game_stats_figure_1.add_glyph(rl_scored_bar)
    game_stats_figure_1.add_glyph(rm_scored_bar)
    game_stats_figure_1.add_glyph(rr_scored_bar)
        #</editor-fold>
        #<editor-fold Blocked Left Data Bars:
    ll_blocked_left_bar = Rect(x = fig_configs.ll_loc, y = 0, angle = 0,
                               width = fig_configs.bar_width, height = 0,
                               fill_color = fig_configs.blocked_left_bar_color,
                               line_width = fig_configs.bar_line_width)
    lm_blocked_left_bar = Rect(x = fig_configs.lm_loc, y = 0, angle = 0,
                               width = fig_configs.bar_width, height = 0,
                               fill_color = fig_configs.blocked_left_bar_color,
                               line_width = fig_configs.bar_line_width)
    lr_blocked_left_bar = Rect(x = fig_configs.lr_loc, y = 0, angle = 0,
                               width = fig_configs.bar_width, height = 0,
                               fill_color = fig_configs.blocked_left_bar_color,
                               line_width = fig_configs.bar_line_width)
    rl_blocked_left_bar = Rect(x = fig_configs.rl_loc, y = 0, angle = 0,
                               width = fig_configs.bar_width, height = 0,
                               fill_color = fig_configs.blocked_left_bar_color,
                               line_width = fig_configs.bar_line_width)
    rm_blocked_left_bar = Rect(x = fig_configs.rm_loc, y = 0, angle = 0,
                               width = fig_configs.bar_width, height = 0,
                               fill_color = fig_configs.blocked_left_bar_color,
                               line_width = fig_configs.bar_line_width)
    rr_blocked_left_bar = Rect(x = fig_configs.rr_loc, y = 0, angle = 0,
                               width = fig_configs.bar_width, height = 0,
                               fill_color = fig_configs.blocked_left_bar_color,
                               line_width = fig_configs.bar_line_width)

    game_stats_figure_1.add_glyph(ll_blocked_left_bar)
    game_stats_figure_1.add_glyph(lm_blocked_left_bar)
    game_stats_figure_1.add_glyph(lr_blocked_left_bar)
    game_stats_figure_1.add_glyph(rl_blocked_left_bar)
    game_stats_figure_1.add_glyph(rm_blocked_left_bar)
    game_stats_figure_1.add_glyph(rr_blocked_left_bar)
        #</editor-fold>
        #<editor-fold Blocked Middle Data Bars:
    ll_blocked_middle_bar = Rect(x = fig_configs.ll_loc, y = 0, angle = 0,
                                 width = fig_configs.bar_width, height = 0,
                                 fill_color = fig_configs.blocked_middle_bar_color,
                                 line_width = fig_configs.bar_line_width)
    lm_blocked_middle_bar = Rect(x = fig_configs.lm_loc, y = 0, angle = 0,
                                 width = fig_configs.bar_width, height = 0,
                                 fill_color = fig_configs.blocked_middle_bar_color,
                                 line_width = fig_configs.bar_line_width)
    lr_blocked_middle_bar = Rect(x = fig_configs.lr_loc, y = 0, angle = 0,
                                 width = fig_configs.bar_width, height = 0,
                                 fill_color = fig_configs.blocked_middle_bar_color,
                                 line_width = fig_configs.bar_line_width)
    rl_blocked_middle_bar = Rect(x = fig_configs.rl_loc, y = 0, angle = 0,
                                 width = fig_configs.bar_width, height = 0,
                                 fill_color = fig_configs.blocked_middle_bar_color,
                                 line_width = fig_configs.bar_line_width)
    rm_blocked_middle_bar = Rect(x = fig_configs.rm_loc, y = 0, angle = 0,
                                 width = fig_configs.bar_width, height = 0,
                                 fill_color = fig_configs.blocked_middle_bar_color,
                                 line_width = fig_configs.bar_line_width)
    rr_blocked_middle_bar = Rect(x = fig_configs.rr_loc, y = 0, angle = 0,
                                 width = fig_configs.bar_width, height = 0,
                                 fill_color = fig_configs.blocked_middle_bar_color,
                                 line_width = fig_configs.bar_line_width)

    game_stats_figure_1.add_glyph(ll_blocked_middle_bar)
    game_stats_figure_1.add_glyph(lm_blocked_middle_bar)
    game_stats_figure_1.add_glyph(lr_blocked_middle_bar)
    game_stats_figure_1.add_glyph(rl_blocked_middle_bar)
    game_stats_figure_1.add_glyph(rm_blocked_middle_bar)
    game_stats_figure_1.add_glyph(rr_blocked_middle_bar)
        #</editor-fold>
        #<editor-fold Blocked Right Data Bars:
    ll_blocked_right_bar = Rect(x = fig_configs.ll_loc, y = 0, angle = 0,
                                width = fig_configs.bar_width, height = 0,
                                fill_color = fig_configs.blocked_right_bar_color,
                                line_width = fig_configs.bar_line_width)
    lm_blocked_right_bar = Rect(x = fig_configs.lm_loc, y = 0, angle = 0,
                                width = fig_configs.bar_width, height = 0,
                                fill_color = fig_configs.blocked_right_bar_color,
                                line_width = fig_configs.bar_line_width)
    lr_blocked_right_bar = Rect(x = fig_configs.lr_loc, y = 0, angle = 0,
                                width = fig_configs.bar_width, height = 0,
                                fill_color = fig_configs.blocked_right_bar_color,
                                line_width = fig_configs.bar_line_width)
    rl_blocked_right_bar = Rect(x = fig_configs.rl_loc, y = 0, angle = 0,
                                width = fig_configs.bar_width, height = 0,
                                fill_color = fig_configs.blocked_right_bar_color,
                                line_width = fig_configs.bar_line_width)
    rm_blocked_right_bar = Rect(x = fig_configs.rm_loc, y = 0, angle = 0,
                                width = fig_configs.bar_width, height = 0,
                                fill_color = fig_configs.blocked_right_bar_color,
                                line_width = fig_configs.bar_line_width)
    rr_blocked_right_bar = Rect(x = fig_configs.rr_loc, y = 0, angle = 0,
                                width = fig_configs.bar_width, height = 0,
                                fill_color = fig_configs.blocked_right_bar_color,
                                line_width = fig_configs.bar_line_width)

    game_stats_figure_1.add_glyph(ll_blocked_right_bar)
    game_stats_figure_1.add_glyph(lm_blocked_right_bar)
    game_stats_figure_1.add_glyph(lr_blocked_right_bar)
    game_stats_figure_1.add_glyph(rl_blocked_right_bar)
    game_stats_figure_1.add_glyph(rm_blocked_right_bar)
    game_stats_figure_1.add_glyph(rr_blocked_right_bar)
        #</editor-fold>
    #</editor-fold>
    #<editor-fold Legend Creation:
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
    game_stats_figure_1_source_xs = [0.00, 0.50, 1.00,
                                     1.00, 1.50, 2.00,
                                     2.00, 2.50, 3.00,
                                     3.00, 3.50, 4.00,
                                     4.00, 4.50, 5.00,
                                     5.00, 5.50, 6.00]

    game_stats_figure_1_source_scored_ys = [0.00, 0.00, 0.00,
                                            0.00, 0.00, 0.00,
                                            0.00, 0.00, 0.00,
                                            0.00, 0.00, 0.00,
                                            0.00, 0.00, 0.00,
                                            0.00, 0.00, 0.00]

    game_stats_figure_1_source_blockedl_ys = [0.00, 0.00, 0.00,
                                              0.00, 0.00, 0.00,
                                              0.00, 0.00, 0.00,
                                              0.00, 0.00, 0.00,
                                              0.00, 0.00, 0.00,
                                              0.00, 0.00, 0.00]

    game_stats_figure_1_source_blockedm_ys = [0.00, 0.00, 0.00,
                                              0.00, 0.00, 0.00,
                                              0.00, 0.00, 0.00,
                                              0.00, 0.00, 0.00,
                                              0.00, 0.00, 0.00,
                                              0.00, 0.00, 0.00]

    game_stats_figure_1_source_blockedr_ys = [0.00, 0.00, 0.00,
                                              0.00, 0.00, 0.00,
                                              0.00, 0.00, 0.00,
                                              0.00, 0.00, 0.00,
                                              0.00, 0.00, 0.00,
                                              0.00, 0.00, 0.00]
    game_stats_figure_1_data = dict(x = game_stats_figure_1_source_xs,
                                    scored_y = game_stats_figure_1_source_scored_ys,
                                    blockedl_y = game_stats_figure_1_source_blockedl_ys,
                                    blockedm_y = game_stats_figure_1_source_blockedm_ys,
                                    blockedr_y = game_stats_figure_1_source_blockedr_ys,
                                    hoverxy = [0,0,0,0,0,0,0,0,0,
                                               0,0,0,0,0,0,0,0,0],
                                    hoverhovering = [0,0,0,0,0,0,0,0,0,
                                                     0,0,0,0,0,0,0,0,0],
                                    hovershow = [0,1,0,0,1,0,0,1,0,
                                                 0,1,0,0,1,0,0,1,0])
    game_stats_figure_1_source = ColumnDataSource(game_stats_figure_1_data)
    #</editor-fold>
    #<editor-fold Invisible Lines for Custom HoverTool:
    game_stats_figure_1.line('x', 'scored_y',
                             source = game_stats_figure_1_source,
                             line_width = 1, line_alpha = 0,
                             line_color = fig_configs.scored_bar_color,
                             name = 'scored_y')
    game_stats_figure_1.line('x', 'blockedl_y',
                             source = game_stats_figure_1_source,
                             line_width = 1, line_alpha = 0,
                             line_color = fig_configs.blocked_left_bar_color,
                             name = 'blockedl_y')
    game_stats_figure_1.line('x', 'blockedm_y',
                             source = game_stats_figure_1_source,
                             line_width = 1, line_alpha = 0,
                             line_color = fig_configs.blocked_middle_bar_color,
                             name = 'blockedm_y')
    game_stats_figure_1.line('x', 'blockedr_y',
                             source = game_stats_figure_1_source,
                             line_width = 1, line_alpha = 0,
                             line_color = fig_configs.blocked_right_bar_color,
                             name = 'blockedr_y')
    #</editor-fold>
    #<editor-fold CustomJSHover Creation:
    #Create CustomJSHovers for the HoverTool:
    fig_1_jshover_args = dict(game_stats_figure_1_source = game_stats_figure_1_source)
    coordinates_custom = CustomJSHover(code = custom_hover_coordinates_code,
                                       args = fig_1_jshover_args)
    hovering_custom = CustomJSHover(code = custom_hover_hovering_code,
                                    args = fig_1_jshover_args)
    custom_hover = CustomJSHover(code = custom_hover_code,
                                 args = fig_1_jshover_args)
    #</editor-fold>
    #<editor-fold Tool Definition:
    fig_1_jshover_formatters = {'@hoverxy' : coordinates_custom,
                                '@hoverhovering' : hovering_custom,
                                '@hovershow' : custom_hover}
    game_stats_figure_1.add_tools(HoverTool(tooltips = fig_1_custom_tooltip,
                                            formatters = fig_1_jshover_formatters,
                                            mode = "vline"))
    #</editor-fold>
    return (game_stats_figure_1, game_stats_figure_1_source, ll_scored_bar,
            lm_scored_bar, lr_scored_bar, rl_scored_bar, rm_scored_bar,
            rr_scored_bar, ll_blocked_left_bar, lm_blocked_left_bar,
            lr_blocked_left_bar, rl_blocked_left_bar,
            rm_blocked_left_bar, rr_blocked_left_bar,
            ll_blocked_middle_bar, lm_blocked_middle_bar,
            lr_blocked_middle_bar, rl_blocked_middle_bar,
            rm_blocked_middle_bar, rr_blocked_middle_bar,
            ll_blocked_right_bar, lm_blocked_right_bar,
            lr_blocked_right_bar, rl_blocked_right_bar,
            rm_blocked_right_bar, rr_blocked_right_bar)
#</editor-fold>
