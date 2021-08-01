from bokeh.models import Button, CustomJS
from . import gameloop_codestrings

#<editor-fold create():
def create(game_parts, config):
    b_start_automate = Button(label = config.label,
                              button_type = config.button_type,
                              sizing_mode = config.sizing_mode,
                              width_policy = config.width_policy,
                              disabled = config.disabled,
                              visible = config.visible)
    game_parts.buttons['start'] = b_start_automate
#</editor-fold>

#<editor-fold setup():
#Needs:
#   from bokeh.models import CustomJS
def setup(game_parts,
          stats_fig_1_enabled,
          stats_fig_2_enabled,
          stats_fig_3_enabled,
          stats_fig_4_enabled):

    args_dict =  dict(chancesSrc = game_parts.sources['automation_table'],
                      distTableSrc = game_parts.sources['distribution_table'],
                      stratToUseDiv = game_parts.divs['strategy_to_use'],
                      nround = game_parts.divs['nround'],
                      txt = game_parts.texts['scr_text'],
                      nextButton = game_parts.buttons['next'],
                      gameFig = game_parts.figures['game_figure'],
                      distTable = game_parts.tables['distribution'],
                      goalieHead = game_parts.glyphs['goalie_head'],
                      goalieBody = game_parts.glyphs['goalie_body'],
                      counterSrc = game_parts.sources['goalie_counter'],
                      ball = game_parts.glyphs['ball'],
                      score = game_parts.divs['score'],
                      statsFig1 = game_parts.figures['stats_1'],
                      statsFig2 = game_parts.figures['stats_2'],
                      statsFig3 = game_parts.figures['stats_3'],
                      statsFig4 = game_parts.figures['stats_4'],
                      statsFig1Src = game_parts.sources['stats_fig_1'],
                      statsFig2Src = game_parts.sources['stats_fig_2'],
                      statsFig3Src = game_parts.sources['stats_fig_3'],
                      statsFig4Src = game_parts.sources['stats_fig_4'],
                      startButton = game_parts.buttons['start'],
                      iterSlider = game_parts.sliders['iterations'],
                      stratDropdown = game_parts.dropdowns['cpu_strategy'],
                      automationTable = game_parts.tables['automation'],
                      llAimTextInput = game_parts.textinputs['ll_aim'],
                      lmAimTextInput = game_parts.textinputs['lm_aim'],
                      lrAimTextInput = game_parts.textinputs['lr_aim'],
                      rlAimTextInput = game_parts.textinputs['rl_aim'],
                      rmAimTextInput = game_parts.textinputs['rm_aim'],
                      rrAimTextInput = game_parts.textinputs['rr_aim'],
                      autoAdvButton = game_parts.buttons['auto_advance'],
                      inAnIter = game_parts.divs['in_an_iter'],
                      advSpdSlider = game_parts.sliders['auto_advance_speed'],
                      gameFigButton = game_parts.buttons['game_fig'],
                      statsFig1Button = game_parts.buttons['fig_1'],
                      statsFig2Button = game_parts.buttons['fig_2'],
                      statsFig3Button = game_parts.buttons['fig_3'],
                      statsFig4Button = game_parts.buttons['fig_4'])
    b_start_automate_click = CustomJS(args = args_dict,
                                      code = gameloop_codestrings.make_automateStartCode(stats_fig_1_enabled,
                                                                                         stats_fig_2_enabled,
                                                                                         stats_fig_3_enabled,
                                                                                         stats_fig_4_enabled))
    game_parts.buttons['start'].js_on_click(b_start_automate_click)
#</editor-fold>
