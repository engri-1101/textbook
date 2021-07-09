from bokeh.models import Button, CustomJS
from . import gameloop_codestrings

#<editor-fold create():
def create(game_parts, config):
    b_auto_next = Button(label = config.label, button_type = config.button_type,
                         sizing_mode = config.sizing_mode,
                         width_policy = config.width_policy,
                         disabled = config.disabled, visible = config.visible)
    game_parts.buttons['next'] = b_auto_next
#</editor-fold>

#<editor-fold setup():
#Needs:
#   from bokeh.models import CustomJS
def setup(game_parts):
    b_figs = [game_parts.buttons['fig_1'], game_parts.buttons['fig_2'],
              game_parts.buttons['fig_3'], game_parts.buttons['fig_4']]
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
                      score = game_parts.divs['score'], b_figs = b_figs,
                      stats_fig_1 = game_parts.figures['stats_1'],
                      stats_fig_2 = game_parts.figures['stats_2'],
                      stats_fig_3 = game_parts.figures['stats_3'],
                      stats_fig_4 = game_parts.figures['stats_4'],
                      stats_fig_1_source = game_parts.sources['stats_fig_1'],
                      stats_fig_2_source = game_parts.sources['stats_fig_2'],
                      stats_fig_3_source = game_parts.sources['stats_fig_3'],
                      stats_fig_4_source = game_parts.sources['stats_fig_4'])
    b_auto_next_click = CustomJS(args = args_dict,
                                 code = gameloop_codestrings.game_iteration)
    game_parts.buttons['next'].js_on_click(b_auto_next_click)
#</editor-fold>
