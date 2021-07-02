from bokeh.models import Slider, CustomJS

#<editor-fold iterations_slider_callback Code String:
iterations_slider_code = """

//Read iterations, and update iterations_to_run:
const iterations = cb_obj.value;
iterations_to_run.text = iterations.toString();

//Set the max of the y axis for stats_fig_1 to be the
//amount of iterations (It is impossible to have bars higher than that value):
stats_fig_1.y_range.end = iterations;

//Set the max and min of the y axis for stats_fig_2 to be
//+/- the amount of iterations as it is impossible to have a score higher or
//lower than that:
stats_fig_2.y_range.start = -iterations;
stats_fig_2.y_range.end = iterations;

//Sets the max of the x axis for stats_fig_2 and stats_fig_3 to
//be the amount of iterations.
stats_fig_2.x_range.end = iterations;
stats_fig_3.x_range.end = iterations;
stats_fig_4.x_range.end = iterations;
//Initiate arrays to update lengths and values of data in sources:
const array_length = iterations + 1;
let xs_2 = [];
let xs_3 = [];
let xs_4 = [];

let ys = new Array(array_length).fill(0);
let chance_ys = new Array(array_length).fill(0);
let ll_ys = new Array(array_length).fill(0);
let lm_ys = new Array(array_length).fill(0);
let lr_ys = new Array(array_length).fill(0);
let rl_ys = new Array(array_length).fill(0);
let rm_ys = new Array(array_length).fill(0);
let rr_ys = new Array(array_length).fill(0);
let hb1_ys = new Array(array_length).fill(0);
let hb2_ys = new Array(array_length).fill(0);
let hb3_ys = new Array(array_length).fill(0);
let hb4_ys = new Array(array_length).fill(0);
let hb5_ys = new Array(array_length).fill(0);
let hb6_ys = new Array(array_length).fill(0);
let heights = new Array(array_length).fill(iterations * 2);
let fig2_highlight_alphas = new Array(array_length).fill(0);
let fig3_highlight_alphas = new Array(array_length).fill(0);
let fig3_alphas_zeroes = new Array(array_length).fill(0);
let ys_4 = new Array(array_length).fill(0);
let feet_4 = new Array(array_length).fill(null);
let directions_4 = new Array(array_length).fill(null);
let actions_4 = new Array(array_length).fill(null);
let highlight_alphas_4 = new Array(array_length).fill(0);
let avgs_placeholder = new Array(array_length).fill(0);

//Update previously created arrays with their correct values:
for (let i = 0; i <= iterations; i++){
    xs_2.push(i);
    xs_3.push(i);
    xs_4.push(i);
}

//Write the correct initial values for the arrays that need it:
ll_ys[0] = 1/3 * (0.67 + 0.74 + 0.87);
lm_ys[0] = 1/3 * (0.70 + 0.60 + 0.65);
lr_ys[0] = 1/3 * (0.96 + 0.72 + 0.61);
rl_ys[0] = 1/3 * (0.55 + 0.74 + 0.95);
rm_ys[0] = 1/3 * (0.65 + 0.60 + 0.73);
rr_ys[0] = 1/3 * (0.93 + 0.72 + 0.70);

//Update stats_fig_2_source.data with its new arrays:
const fig_2_data = stats_fig_2_source.data;
fig_2_data['xs'] = xs_2;
fig_2_data['ys'] = ys;
fig_2_data['chance_ys'] = chance_ys;
fig_2_data['heights'] = heights;
fig_2_data['highlight_alphas'] = fig2_highlight_alphas;
stats_fig_2_source.change.emit();

//Update stats_fig_3_source.data with its new arrays:
const fig_3_data = stats_fig_3_source.data;
fig_3_data['xs'] = xs_3;
fig_3_data['ll_ys'] = ll_ys;
fig_3_data['lm_ys'] = lm_ys;
fig_3_data['lr_ys'] = lr_ys;
fig_3_data['rl_ys'] = rl_ys;
fig_3_data['rm_ys'] = rm_ys;
fig_3_data['rr_ys'] = rr_ys;
fig_3_data['highlight_alphas'] = fig3_highlight_alphas;
fig_3_data['alphas_zeroes'] = fig3_alphas_zeroes;
fig_3_data['hb1'] = hb1_ys;
fig_3_data['hb2'] = hb2_ys;
fig_3_data['hb3'] = hb3_ys;
fig_3_data['hb4'] = hb4_ys;
fig_3_data['hb5'] = hb5_ys;
fig_3_data['hb6'] = hb6_ys;
stats_fig_3_source.change.emit();

stats_fig_4_source.data['xs'] = xs_4;
stats_fig_4_source.data['ys'] = ys_4;
stats_fig_4_source.data['feet'] = feet_4;
stats_fig_4_source.data['directions'] = directions_4;
stats_fig_4_source.data['actions'] = actions_4;
stats_fig_4_source.data['highlight_alphas'] = highlight_alphas_4;
stats_fig_4_source.data['avgs_placeholder'] = avgs_placeholder;
stats_fig_4_source.change.emit();
"""
#</editor-fold>

#<editor-fold create():
#Needs:
#   from bokeh.models import Slider
def create(game_parts, config):
    iterations_slider = Slider(start = config.start, end = config.end,
                               value = config.value,
                               step = config.step, title = config.title,
                               disabled = config.disabled,
                               visible = config.visible)
    game_parts.sliders['iterations'] = iterations_slider
#</editor-fold>

#<editor-fold setup():
#Needs:
#    from bokeh.models import CustomJS
def setup(game_parts):
    args_dict = dict(iterations_to_run = game_parts.divs['iterations_to_run'],
                     stats_fig_1 = game_parts.figures['stats_1'],
                     stats_fig_2 = game_parts.figures['stats_2'],
                     stats_fig_3 = game_parts.figures['stats_3'],
                     stats_fig_4 = game_parts.figures['stats_4'],
                     stats_fig_2_source = game_parts.sources['stats_fig_2'],
                     stats_fig_3_source = game_parts.sources['stats_fig_3'],
                     stats_fig_4_source = game_parts.sources['stats_fig_4'])
    iterations_slider_callback = CustomJS(args = args_dict,
                                          code = iterations_slider_code)

    game_parts.sliders['iterations'].js_on_change('value',
                                                         iterations_slider_callback)
#</editor-fold>
