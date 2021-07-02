from bokeh.models import Button, CustomJS
from . import gameloop_codestrings

#<editor-fold create():
def create(game_parts, label = "Start", button_type = "success",
           sizing_mode = "scale_width", width_policy = "fit",
           disabled = False, visible = False):
    b_start_automate = Button(label = label, button_type = button_type,
                        sizing_mode = sizing_mode, width_policy = width_policy,
                        disabled = disabled, visible = visible)
    game_parts.buttons['start'] = b_start_automate
#</editor-fold>

#<editor-fold setup():
#Needs:
#   from bokeh.models import CustomJS
def setup(game_parts):
    args_dict =  dict(chances_source = game_parts.sources['automation_table'],
                      distribution_source = game_parts.sources['distribution_table'],
                      strategy_to_use = game_parts.divs['strategy_to_use'],
                      nround = game_parts.divs['nround'],
                      iterations_to_run = game_parts.divs['iterations_to_run'],
                      txt = game_parts.texts['scr_text'],
                      b_auto_next = game_parts.buttons['next'],
                      game_figure = game_parts.figures['game_figure'],
                      distribution_table = game_parts.tables['distribution'],
                      goalie_head = game_parts.glyphs['goalie_head'],
                      goalie_body = game_parts.glyphs['goalie_body'],
                      counter_source = game_parts.sources['goalie_counter'],
                      ball = game_parts.glyphs['ball'],
                      score = game_parts.divs['score'],
                      b_fig_1 = game_parts.buttons['fig_1'],
                      b_fig_2 = game_parts.buttons['fig_2'],
                      b_fig_3 = game_parts.buttons['fig_3'],
                      b_fig_4 = game_parts.buttons['fig_4'],
                      stats_fig_1 = game_parts.figures['stats_1'],
                      stats_fig_2 = game_parts.figures['stats_2'],
                      stats_fig_3 = game_parts.figures['stats_3'],
                      stats_fig_4 = game_parts.figures['stats_4'],
                      stats_fig_1_source = game_parts.sources['stats_fig_1'],
                      stats_fig_2_source = game_parts.sources['stats_fig_2'],
                      stats_fig_3_source = game_parts.sources['stats_fig_3'],
                      stats_fig_4_source = game_parts.sources['stats_fig_4'],
                      b_start_automate = game_parts.buttons['start'],
                      iterations_slider = game_parts.sliders['iterations'],
                      strategy_dropdown = game_parts.dropdowns['cpu_strategy'],
                      automation_table = game_parts.tables['automation'],
                      ll_aim_text_input = game_parts.textinputs['ll_aim'],
                      lm_aim_text_input = game_parts.textinputs['lm_aim'],
                      lr_aim_text_input = game_parts.textinputs['lr_aim'],
                      rl_aim_text_input = game_parts.textinputs['rl_aim'],
                      rm_aim_text_input = game_parts.textinputs['rm_aim'],
                      rr_aim_text_input = game_parts.textinputs['rr_aim'])
    b_start_automate_click = CustomJS(args = args_dict,
                                      code = gameloop_codestrings.b_automate_start_code)
    game_parts.buttons['start'].js_on_click(b_start_automate_click)
#</editor-fold>
