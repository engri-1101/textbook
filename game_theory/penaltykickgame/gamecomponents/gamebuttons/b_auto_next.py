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

    args_dict =  dict(chancesSrc = game_parts.sources['automation_table'],
                      distTableSrc = game_parts.sources['distribution_table'],
                      stratToUseDiv = game_parts.divs['strategy_to_use'],
                      nround = game_parts.divs['nround'],
                      itersToRunDiv = game_parts.divs['iterations_to_run'],
                      txt = game_parts.texts['scr_text'],
                      nextButton = game_parts.buttons['next'],
                      gameFig = game_parts.figures['game_figure'],
                      distTable = game_parts.tables['distribution'],
                      goalieHead = game_parts.glyphs['goalie_head'],
                      goalieBody = game_parts.glyphs['goalie_body'],
                      counterSrc = game_parts.sources['goalie_counter'],
                      ball = game_parts.glyphs['ball'],
                      score = game_parts.divs['score'],
                      figButtons = b_figs,
                      statsFig1 = game_parts.figures['stats_1'],
                      statsFig2 = game_parts.figures['stats_2'],
                      statsFig3 = game_parts.figures['stats_3'],
                      statsFig4 = game_parts.figures['stats_4'],
                      statsFig1Src = game_parts.sources['stats_fig_1'],
                      statsFig2Src = game_parts.sources['stats_fig_2'],
                      statsFig3Src = game_parts.sources['stats_fig_3'],
                      statsFig4Src = game_parts.sources['stats_fig_4'],
                      autoAdvanceButton = game_parts.buttons['auto_advance'],
                      inAnIter = game_parts.divs['in_an_iter'])
    b_auto_next_click = CustomJS(args = args_dict,
                                 code = gameloop_codestrings.game_iter)
    game_parts.buttons['next'].js_on_click(b_auto_next_click)
#</editor-fold>
