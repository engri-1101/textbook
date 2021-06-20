from bokeh.plotting import figure
from bokeh.models import (CustomJSHover, ColumnDataSource, CustomJSTransform,
                          HoverTool)
from bokeh.transform import transform

#<editor-fold hb_gc Code Strings:
hb1_gc_code = """
var new_xs = new Array(xs.length);
for(var i = 0; i < xs.length; i++) {
    new_xs[i] = xs[i]/2;
}
return new_xs;
"""
hb2_gc_code = """
var new_xs = new Array(xs.length);
for(var i = 0; i < xs.length; i++) {
    new_xs[i] = xs[i]/2 + source.data['hb1'][i];
}
return new_xs;
"""
hb3_gc_code = """
var new_xs = new Array(xs.length);
for(var i = 0; i < xs.length; i++) {
    new_xs[i] = xs[i]/2 + source.data['hb2'][i] + source.data['hb1'][i];
}
return new_xs;
"""
hb4_gc_code = """
var new_xs = new Array(xs.length);
for(var i = 0; i < xs.length; i++) {
    new_xs[i] = xs[i]/2 + source.data['hb3'][i] + source.data['hb2'][i] + source.data['hb1'][i];
}
return new_xs;
"""
hb5_gc_code = """
var new_xs = new Array(xs.length);
for(var i = 0; i < xs.length; i++) {
    new_xs[i] = xs[i]/2 + source.data['hb4'][i] + source.data['hb3'][i] + source.data['hb2'][i] + source.data['hb1'][i];
}
return new_xs;
"""
hb6_gc_code = """
var new_xs = new Array(xs.length);
for(var i = 0; i < xs.length; i++) {
    new_xs[i] = xs[i]/2 + source.data['hb5'][i] + source.data['hb4'][i] + source.data['hb3'][i] + source.data['hb2'][i] + source.data['hb1'][i];
}
return new_xs;
"""
#</editor-fold>
#<editor-fold Custom Hover Code Strings:
    #<editor-fold xs Code String:
fig_3_xs_code = """
var index = special_vars.index;
var name = special_vars.name;
var data = source.data;
const length = data['xs'].length;
const column = ['ll',
                'lm',
                'lr',
                'rl',
                'rm',
                'rr'];
const values = [data['ll_ys'][index],
                data['lm_ys'][index],
                data['lr_ys'][index],
                data['rl_ys'][index],
                data['rm_ys'][index],
                data['rr_ys'][index]];
var sorted_values = [data['ll_ys'][index],
                     data['lm_ys'][index],
                     data['lr_ys'][index],
                     data['rl_ys'][index],
                     data['rm_ys'][index],
                     data['rr_ys'][index]];
sorted_values = sorted_values.sort((a, b) => b - a);
var selected = column[values.indexOf(sorted_values[parseInt(name)])];

for(var i = 0; i < length; i++){
    data['ll_highlight_alphas'][i] = 0;
    data['lm_highlight_alphas'][i] = 0;
    data['lr_highlight_alphas'][i] = 0;
    data['rl_highlight_alphas'][i] = 0;
    data['rm_highlight_alphas'][i] = 0;
    data['rr_highlight_alphas'][i] = 0;
}
if(selected == 'll'){
    data['ll_highlight_alphas'][index] = 1;
}
else if(selected == 'lm'){
    data['lm_highlight_alphas'][index] = 1;
}
else if(selected == 'lr'){
    data['lr_highlight_alphas'][index] = 1;
}
else if(selected == 'rl'){
    data['rl_highlight_alphas'][index] = 1;
}
else if(selected == 'rm'){
    data['rm_highlight_alphas'][index] = 1;
}
else if(selected == 'rr'){
    data['rr_highlight_alphas'][index] = 1;
}
source.change.emit();

return index.toString();
"""
    #</editor-fold>
    #<editor-fold ys Code String:
fig_3_ys_code = """
var index = special_vars.index;
var name = special_vars.name;
var data = source.data;
const length = data['xs'].length;
const column = ['ll',
                'lm',
                'lr',
                'rl',
                'rm',
                'rr'];
const values = [data['ll_ys'][index],
                data['lm_ys'][index],
                data['lr_ys'][index],
                data['rl_ys'][index],
                data['rm_ys'][index],
                data['rr_ys'][index]];
var sorted_values = [data['ll_ys'][index],
                     data['lm_ys'][index],
                     data['lr_ys'][index],
                     data['rl_ys'][index],
                     data['rm_ys'][index],
                     data['rr_ys'][index]];
sorted_values = sorted_values.sort((a, b) => b - a);
var selected = column[values.indexOf(sorted_values[parseInt(name)])];

if(selected == 'll'){
    return(source.data['ll_ys'][index].toString());
}
else if(selected == 'lm'){
    return(source.data['lm_ys'][index].toString());
}
else if(selected == 'lr'){
    return(source.data['lr_ys'][index].toString());
}
else if(selected == 'rl'){
    return(source.data['rl_ys'][index].toString());
}
else if(selected == 'rm'){
    return(source.data['rm_ys'][index].toString());
}
else if(selected == 'rr'){
    return(source.data['rr_ys'][index].toString());
}
"""
    #</editor-fold>
    #<editor-fold selected Code String:
fig_3_selected_code = """
var index = special_vars.index;
var name = special_vars.name;
var data = source.data;
const length = data['xs'].length;
const column = ['ll',
                'lm',
                'lr',
                'rl',
                'rm',
                'rr'];
const values = [data['ll_ys'][index],
                data['lm_ys'][index],
                data['lr_ys'][index],
                data['rl_ys'][index],
                data['rm_ys'][index],
                data['rr_ys'][index]];
var sorted_values = [data['ll_ys'][index],
                     data['lm_ys'][index],
                     data['lr_ys'][index],
                     data['rl_ys'][index],
                     data['rm_ys'][index],
                     data['rr_ys'][index]];
sorted_values = sorted_values.sort((a, b) => b - a);
var selected = column[values.indexOf(sorted_values[parseInt(name)])];
return(selected);
"""
    #</editor-fold>
#</editor-fold>
#<editor-fold Cusstom Hover Tooltip Code String:
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
    <span style='font-size: 10px;'>Risk Type:</span>
    <span style='font-size: 10px;'>@lm_ys{custom}</span>
</div>
"""
#</editor-fold>

def stats_figure_3_setup(figure_base_tools = "box_zoom, wheel_zoom, pan",
                         figure_toolbar_location = "below",
                         figure_title = "Goalie Perceived Risks Over Iterations",
                         figure_width = 300, figure_height = 240,
                         figure_x_range = (0, 50), figure_y_range = (0, 1),
                         figure_initial_visibility = False,
                         figure_sizing_mode = "stretch_both",
                         figure_title_font_size = '8pt',
                         figure_x_axis_visibility = True,
                         figure_y_axis_visibility = True,
                         figure_xgrid_line_color = None,
                         figure_ygrid_line_color = None,
                         figure_outline_line_color = None,
                         figure_background_color = "white",
                         plot_dot_size = 5, plot_ll_dot_color = "#C8AFAF",
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
    #<editor-fold Figure Creation:
    game_stats_figure_3 = figure(tools = figure_base_tools,
                                 toolbar_location = figure_toolbar_location,
                                 title = figure_title,
                                 plot_width = figure_width,
                                 plot_height = figure_height,
                                 x_range = figure_x_range,
                                 y_range = figure_y_range,
                                 visible = figure_initial_visibility,
                                 sizing_mode = figure_sizing_mode)
    game_stats_figure_3.title.text_font_size = figure_title_font_size
    game_stats_figure_3.xaxis.visible = figure_x_axis_visibility
    game_stats_figure_3.yaxis.visible = figure_y_axis_visibility
    game_stats_figure_3.xgrid.grid_line_color = figure_xgrid_line_color
    game_stats_figure_3.ygrid.grid_line_color = figure_ygrid_line_color
    game_stats_figure_3.outline_line_color = figure_outline_line_color
    game_stats_figure_3.background_fill_color = figure_background_color
    #</editor-fold>
    #<editor-fold ColumnDataSource Creation:
        #<editor-fold Create Base Values:
    source_xs = []

    source_ll_ys = []
    source_lm_ys = []
    source_lr_ys = []
    source_rl_ys = []
    source_rm_ys = []
    source_rr_ys = []

    ll_highlight_alphas = []
    lm_highlight_alphas = []
    lr_highlight_alphas = []
    rl_highlight_alphas = []
    rm_highlight_alphas = []
    rr_highlight_alphas = []

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

        ll_highlight_alphas.append(0)
        lm_highlight_alphas.append(0)
        lr_highlight_alphas.append(0)
        rl_highlight_alphas.append(0)
        rm_highlight_alphas.append(0)
        rr_highlight_alphas.append(0)

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
    source_data = dict(xs = source_xs,

                       ll_ys = source_ll_ys, lm_ys = source_lm_ys,
                       lr_ys = source_lr_ys, rl_ys = source_rl_ys,
                       rm_ys = source_rm_ys, rr_ys = source_rr_ys,

                       hb1 = source_hb1_ys, hb2 = source_hb2_ys,
                       hb3 = source_hb3_ys, hb4 = source_hb4_ys,
                       hb5 = source_hb5_ys, hb6 = source_hb6_ys,

                       ll_highlight_alphas = ll_highlight_alphas,
                       lm_highlight_alphas = lm_highlight_alphas,
                       lr_highlight_alphas = lr_highlight_alphas,
                       rl_highlight_alphas = rl_highlight_alphas,
                       rm_highlight_alphas = rm_highlight_alphas,
                       rr_highlight_alphas = rr_highlight_alphas)

    game_stats_figure_3_source = ColumnDataSource(data = source_data)
        #</editor-fold>
    #</editor-fold>
    #<editor-fold Plot Figure Data Points:
    game_stats_figure_3.circle_dot('xs', 'll_ys',
                                   source = game_stats_figure_3_source,
                                   size = plot_dot_size,
                                   color = plot_ll_dot_outline_color,
                                   fill_color = plot_ll_dot_color)
    game_stats_figure_3.circle_dot('xs', 'lm_ys',
                                   source = game_stats_figure_3_source,
                                   size = plot_dot_size,
                                   color = plot_lm_dot_outline_color,
                                   fill_color = plot_lm_dot_color)
    game_stats_figure_3.circle_dot('xs', 'lr_ys',
                                   source = game_stats_figure_3_source,
                                   size = plot_dot_size,
                                   color = plot_lr_dot_outline_color,
                                   fill_color = plot_lr_dot_color)
    game_stats_figure_3.circle_dot('xs', 'rl_ys',
                                   source = game_stats_figure_3_source,
                                   size = plot_dot_size,
                                   color = plot_rl_dot_outline_color,
                                   fill_color = plot_rl_dot_color)
    game_stats_figure_3.circle_dot('xs', 'rm_ys',
                                   source = game_stats_figure_3_source,
                                   size = plot_dot_size,
                                   color = plot_rm_dot_outline_color,
                                   fill_color = plot_rm_dot_color)
    game_stats_figure_3.circle_dot('xs', 'rr_ys',
                                   source = game_stats_figure_3_source,
                                   size = plot_dot_size,
                                   color = plot_rr_dot_outline_color,
                                   fill_color = plot_rr_dot_color)

    #Plot Highlight Points For Figure:
    game_stats_figure_3.circle_dot('xs', 'll_ys',
                                   source = game_stats_figure_3_source,
                                   size = plot_highlight_dot_size,
                                   color = plot_highlight_dot_outline_color,
                                   fill_color = plot_highlight_dot_color,
                                   alpha = 'll_highlight_alphas')
    game_stats_figure_3.circle_dot('xs', 'lm_ys',
                                   source = game_stats_figure_3_source,
                                   size = plot_highlight_dot_size,
                                   color = plot_highlight_dot_outline_color,
                                   fill_color = plot_highlight_dot_color,
                                   alpha = 'lm_highlight_alphas')
    game_stats_figure_3.circle_dot('xs', 'lr_ys',
                                   source = game_stats_figure_3_source,
                                   size = plot_highlight_dot_size,
                                   color = plot_highlight_dot_outline_color,
                                   fill_color = plot_highlight_dot_color,
                                   alpha = 'lr_highlight_alphas')
    game_stats_figure_3.circle_dot('xs', 'rl_ys',
                                   source = game_stats_figure_3_source,
                                   size = plot_highlight_dot_size,
                                   color = plot_highlight_dot_outline_color,
                                   fill_color = plot_highlight_dot_color,
                                   alpha = 'rl_highlight_alphas')
    game_stats_figure_3.circle_dot('xs', 'rm_ys',
                                   source = game_stats_figure_3_source,
                                   size = plot_highlight_dot_size,
                                   color = plot_highlight_dot_outline_color,
                                   fill_color = plot_highlight_dot_color,
                                   alpha = 'rm_highlight_alphas')
    game_stats_figure_3.circle_dot('xs', 'rr_ys',
                                   source = game_stats_figure_3_source,
                                   size = plot_highlight_dot_size,
                                   color = plot_highlight_dot_outline_color,
                                   fill_color = plot_highlight_dot_color,
                                   alpha = 'rr_highlight_alphas')
    #</editor-fold>
    #<editor-fold CustomJSTransform Definitions For Custom HoverTool:
    hb_gc_args_dict = dict(source = game_stats_figure_3_source)

    hb1_get_center = CustomJSTransform(v_func = hb1_gc_code)
    hb2_get_center = CustomJSTransform(args = hb_gc_args_dict,
                                       v_func = hb2_gc_code)
    hb3_get_center = CustomJSTransform(args = hb_gc_args_dict,
                                       v_func = hb3_gc_code)
    hb4_get_center = CustomJSTransform(args = hb_gc_args_dict,
                                       v_func = hb4_gc_code)
    hb5_get_center = CustomJSTransform(args = hb_gc_args_dict,
                                       v_func = hb5_gc_code)
    hb6_get_center = CustomJSTransform(args = hb_gc_args_dict,
                                       v_func = hb6_gc_code)
    #</editor-fold>
    #<editor-fold Plot Invisible Hitboxes:
    game_stats_figure_3.rect(x = 'xs', y = transform('hb1', hb1_get_center),
                             source = game_stats_figure_3_source, width = 1,
                             height = 'hb1', alpha = hitbox_alpha,
                             fill_alpha = 0, name = '5')
    game_stats_figure_3.rect(x = 'xs', y = transform('hb2', hb2_get_center),
                             source = game_stats_figure_3_source, width = 1,
                             height = 'hb2', alpha = hitbox_alpha,
                             fill_alpha = 0, name = '4')
    game_stats_figure_3.rect(x = 'xs', y = transform('hb3', hb3_get_center),
                             source = game_stats_figure_3_source, width = 1,
                             height = 'hb3', alpha = hitbox_alpha,
                             fill_alpha = 0, name = '3')
    game_stats_figure_3.rect(x = 'xs', y = transform('hb4', hb4_get_center),
                             source = game_stats_figure_3_source, width = 1,
                             height = 'hb4', alpha = hitbox_alpha,
                             fill_alpha = 0, name = '2')
    game_stats_figure_3.rect(x = 'xs', y = transform('hb5', hb5_get_center),
                             source = game_stats_figure_3_source, width = 1,
                             height = 'hb5', alpha = hitbox_alpha,
                             fill_alpha = 0, name = '1')
    game_stats_figure_3.rect(x = 'xs', y = transform('hb6', hb6_get_center),
                             source = game_stats_figure_3_source, width = 1,
                             height = 'hb6', alpha = hitbox_alpha,
                             fill_alpha = 0, name = '0')
    #</editor-fold>
    #<editor-fold CustomJSHover Creation:
    customjshover_args_dict = dict(source = game_stats_figure_3_source)
    fig_3_xs_custom = CustomJSHover(code = fig_3_xs_code,
                                    args = customjshover_args_dict)
    fig_3_ys_custom = CustomJSHover(code = fig_3_ys_code,
                                    args = customjshover_args_dict)
    fig_3_selected_custom = CustomJSHover(code = fig_3_selected_code,
                                          args = customjshover_args_dict)
    #</editor-fold>
    #<editor-fold Custom HoverTool Creation:
    hovertool_formatters = { '@xs' : fig_3_xs_custom,
                             '@ll_ys' : fig_3_ys_custom,
                             '@lm_ys' : fig_3_selected_custom}
    game_stats_figure_3.add_tools(HoverTool(tooltips = fig_3_custom_tooltip,
                                            formatters = hovertool_formatters,
                                            mode = "mouse",
                                            point_policy = "follow_mouse"))
    #</editor-fold>
    return (game_stats_figure_3, game_stats_figure_3_source)
