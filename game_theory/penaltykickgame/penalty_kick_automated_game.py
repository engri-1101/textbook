from bokeh.models import (Button, Slider, Dropdown, ColumnDataSource,
                          TableColumn, DataTable, CustomJS, TextInput)
from bokeh.models.widgets import Div
from ortools.linear_solver import pywraplp as OR
from bokeh.models.glyphs import Text
from bokeh.layouts import row, column, gridplot
from . import gamecomponents as components
from . import game_layout
from . import gamefigures as figs


#<editor-fold scr_text and labels configs:
class Scr_text_and_labels_configs:
    def __init__(self, scr_text_xs = [2, 70, 2, 14, 14],
                 scr_text_ys = [86, 86, 5, 40, 32],
                 scr_text_ln_1 = 'Rounds played: 0',
                 scr_text_ln_2 = 'Total score: 0', scr_text_ln_3 = '',
                 scr_text_ln_4 = '', scr_text_ln_5 = '',
                 labels_text_color = "whitesmoke",
                 labels_text_font_size = "15pt",
                 labels_text_x_offset = 0,
                 labels_text_y_offset = +9,
                 labels_text_baseline = "ideographic",
                 labels_text_align = 'left'):
        self.scr_text_xs = scr_text_xs
        self.scr_text_ys = scr_text_ys
        self.scr_text_ln_1 = scr_text_ln_1
        self.scr_text_ln_2 = scr_text_ln_2
        self.scr_text_ln_3 = scr_text_ln_3
        self.scr_text_ln_4 = scr_text_ln_4
        self.scr_text_ln_5 = scr_text_ln_5
        self.labels_text_color = labels_text_color
        self.labels_text_font_size = labels_text_font_size
        self.labels_text_x_offset = labels_text_x_offset
        self.labels_text_y_offset = labels_text_y_offset
        self.labels_text_baseline = labels_text_baseline
        self.labels_text_align = labels_text_align
#</editor-fold>
#<editor-fold Gamestate_divs_configs:
class Gamestate_divs_configs:
    def __init__(self, iterations_to_run_start_text = "50",
                 iterations_to_run_visibility = False,
                 strategy_to_use_start_text = "Not Set",
                 strategy_to_use_visibility = False,
                 nround_text = '0', nround_visibility = False,
                 score_text = '0', score_visibility = False,
                 kicker_foot_text = '',
                 kicker_foot_visibility = False,
                 kicker_kick_text = '',
                 kicker_kick_visibility = False):
        self.iterations_to_run_start_text = iterations_to_run_start_text
        self.iterations_to_run_visibility = iterations_to_run_visibility
        self.strategy_to_use_start_text = strategy_to_use_start_text
        self.strategy_to_use_visibility = strategy_to_use_visibility
        self.nround_text = nround_text
        self.nround_visibility = nround_visibility
        self.score_text = score_text
        self.score_visibility = score_visibility
        self.kicker_foot_text = kicker_foot_text
        self.kicker_foot_visibility = kicker_foot_visibility
        self.kicker_kick_text = kicker_kick_text
        self.kicker_kick_visibility = kicker_kick_visibility
#</editor-fold>
#<editor-fold Button_configs:
class Button_configs:
    def __init__(self, b_automate_label = "Automate",
                 b_automate_button_type = "success",
                 b_automate_sizing_mode = "scale_width",
                 b_automate_width_policy = "fit",
                 b_automate_disabled = False, b_automate_visibility = True,
                 b_start_automate_label = "Start",
                 b_start_automate_button_type = "success",
                 b_start_automate_sizing_mode = "scale_width",
                 b_start_automate_width_policy = "fit",
                 b_start_automate_disabled = False,
                 b_start_automate_visibility = False,
                 b_auto_next_label = "Next",
                 b_auto_next_button_type = "success",
                 b_auto_next_sizing_mode = "scale_width",
                 b_auto_next_width_policy = "fit",
                 b_auto_next_disabled = False, b_auto_next_visibility = False,
                 b_make_counter_label = "Make Counter",
                 b_make_counter_button_type = "success",
                 b_make_counter_sizing_mode = "scale_width",
                 b_make_counter_width_policy = "fit",
                 b_make_counter_disabled = False,
                 b_make_counter_visibility = False,
                 b_fig_1_label = "Figure 1",
                 b_fig_1_button_type = "success",
                 b_fig_1_sizing_mode = "scale_width",
                 b_fig_1_width_policy = "fit",
                 b_fig_1_disabled = True,
                 b_fig_1_visibility = False,
                 b_fig_2_label = "Figure 2",
                 b_fig_2_button_type = "success",
                 b_fig_2_sizing_mode = "scale_width",
                 b_fig_2_width_policy = "fit",
                 b_fig_2_disabled = False,
                 b_fig_2_visibility = False,
                 b_fig_3_label = "Figure 3",
                 b_fig_3_button_type = "success",
                 b_fig_3_sizing_mode = "scale_width",
                 b_fig_3_width_policy = "fit",
                 b_fig_3_disabled = False,
                 b_fig_3_visibility = False,
                 b_fig_4_label = "Figure 4",
                 b_fig_4_button_type = "success",
                 b_fig_4_sizing_mode = "scale_width",
                 b_fig_4_width_policy = "fit",
                 b_fig_4_disabled = False,
                 b_fig_4_visibility = False):
        self.b_automate_label = b_automate_label
        self.b_automate_button_type = b_automate_button_type
        self.b_automate_sizing_mode = b_automate_sizing_mode
        self.b_automate_width_policy = b_automate_width_policy
        self.b_automate_disabled = b_automate_disabled
        self.b_automate_visibility = b_automate_visibility
        self.b_start_automate_label = b_start_automate_label
        self.b_start_automate_button_type = b_start_automate_button_type
        self.b_start_automate_sizing_mode = b_start_automate_sizing_mode
        self.b_start_automate_width_policy = b_start_automate_width_policy
        self.b_start_automate_disabled = b_start_automate_disabled
        self.b_start_automate_visibility = b_start_automate_visibility
        self.b_auto_next_label = b_auto_next_label
        self.b_auto_next_button_type = b_auto_next_button_type
        self.b_auto_next_sizing_mode = b_auto_next_sizing_mode
        self.b_auto_next_width_policy = b_auto_next_width_policy
        self.b_auto_next_disabled = b_auto_next_disabled
        self.b_auto_next_visibility = b_auto_next_visibility
        self.b_make_counter_label = b_make_counter_label
        self.b_make_counter_button_type = b_make_counter_button_type
        self.b_make_counter_sizing_mode = b_make_counter_sizing_mode
        self.b_make_counter_width_policy = b_make_counter_width_policy
        self.b_make_counter_disabled = b_make_counter_disabled
        self.b_make_counter_visibility = b_make_counter_visibility
        self.b_fig_1_label = b_fig_1_label
        self.b_fig_1_button_type = b_fig_1_button_type
        self.b_fig_1_sizing_mode = b_fig_1_sizing_mode
        self.b_fig_1_width_policy = b_fig_1_width_policy
        self.b_fig_1_disabled = b_fig_1_disabled
        self.b_fig_1_visibility = b_fig_1_visibility
        self.b_fig_2_label = b_fig_2_label
        self.b_fig_2_button_type = b_fig_2_button_type
        self.b_fig_2_sizing_mode = b_fig_2_sizing_mode
        self.b_fig_2_width_policy = b_fig_2_width_policy
        self.b_fig_2_disabled = b_fig_2_disabled
        self.b_fig_2_visibility = b_fig_2_visibility
        self.b_fig_3_label = b_fig_3_label
        self.b_fig_3_button_type = b_fig_3_button_type
        self.b_fig_3_sizing_mode = b_fig_3_sizing_mode
        self.b_fig_3_width_policy = b_fig_3_width_policy
        self.b_fig_3_disabled = b_fig_3_disabled
        self.b_fig_3_visibility = b_fig_3_visibility
        self.b_fig_4_label = b_fig_4_label
        self.b_fig_4_button_type = b_fig_4_button_type
        self.b_fig_4_sizing_mode = b_fig_4_sizing_mode
        self.b_fig_4_width_policy = b_fig_4_width_policy
        self.b_fig_4_disabled = b_fig_4_disabled
        self.b_fig_4_visibility = b_fig_4_visibility
#</editor-fold>
#<editor-fold Slider_configs:
class Slider_configs:
    def __init__(self,
                 iterations_slider_start = 10, iterations_slider_end = 500,
                 iterations_slider_value = 50, iterations_slider_step = 10,
                 iterations_slider_title = "Iterations To Run",
                 iterations_slider_disabled = False,
                 iterations_slider_visibility = False):
        self.iterations_slider_start = iterations_slider_start
        self.iterations_slider_end = iterations_slider_end
        self.iterations_slider_value = iterations_slider_value
        self.iterations_slider_step = iterations_slider_step
        self.iterations_slider_title = iterations_slider_title
        self.iterations_slider_disabled = iterations_slider_disabled
        self.iterations_slider_visibility = iterations_slider_visibility
#</editor-fold>
#<editor-fold Strategy_dropdown_configs:
class Strategy_dropdown_configs:
    def __init__(self, fictitious_play_text = "Fictitious_Play",
                 mixed_strategy_text = "Mixed_Strategy",
                 true_random_text = "Random",
                 goalie_cheats_text = "Goalie_Cheats",
                 dropdown_label = "CPU strategy to Use",
                 dropdown_button_type = "warning", dropdown_disabled = False,
                 dropdown_visibility = False):
        self.fictitious_play_text = fictitious_play_text
        self.mixed_strategy_text = mixed_strategy_text
        self.true_random_text = true_random_text
        self.goalie_cheats_text = goalie_cheats_text
        self.dropdown_label = dropdown_label
        self.dropdown_button_type = dropdown_button_type
        self.dropdown_disabled = dropdown_disabled
        self.dropdown_visibility = dropdown_visibility
#</editor-fold>
#<editor-fold Distribution_table_configs:
class Distribution_table_configs:
    def __init__(self, footedness_left_text = "Left",
                 footedness_right_text = "Right",
                 aim_direction_left_text = "Left",
                 aim_direction_middle_text = "Middle",
                 aim_direction_right_text = "Right",
                 footedness_column_title = "Striker Footedness",
                 footedness_column_width = 101,
                 aim_direction_column_title = "Striker Aim Direction",
                 aim_direction_column_width = 107,
                 freq_column_title = "Frequency", freq_column_width = 60,
                 decisions_column_title = "Goalie Decisions",
                 decisions_column_width = 90,
                 perceived_risks_column_title = "Goalie Perceived Risks",
                 perceived_risks_column_width = 130,
                 score_chance_column_title = "Striker's Score Chance",
                 score_chance_column_width = 120,
                 score_roll_column_title = "Striker's Score Roll",
                 score_roll_column_width = 103, table_width = 711,
                 table_height = 280, table_autosize_mode = "force_fit",
                 table_sizing_mode = "scale_width", table_visibility = False,
                 table_fit_columns = False):
        self.footedness_left_text = footedness_left_text
        self.footedness_right_text = footedness_right_text
        self.aim_direction_left_text = aim_direction_left_text
        self.aim_direction_middle_text = aim_direction_middle_text
        self.aim_direction_right_text = aim_direction_right_text

        self.footedness_column_title = footedness_column_title
        self.footedness_column_width = footedness_column_width
        self.aim_direction_column_title = aim_direction_column_title
        self.aim_direction_column_width = aim_direction_column_width
        self.freq_column_title = freq_column_title
        self.freq_column_width = freq_column_width
        self.decisions_column_title = decisions_column_title
        self.decisions_column_width = decisions_column_width
        self.perceived_risks_column_title = perceived_risks_column_title
        self.perceived_risks_column_width = perceived_risks_column_width
        self.score_chance_column_title = score_chance_column_title
        self.score_chance_column_width = score_chance_column_width
        self.score_roll_column_title = score_roll_column_title
        self.score_roll_column_width = score_roll_column_width
        self.table_width = table_width
        self.table_height = table_height
        self.table_autosize_mode = table_autosize_mode
        self.table_sizing_mode = table_sizing_mode
        self.table_visibility = table_visibility
        self.table_fit_columns = table_fit_columns
#</editor-fold>
#<editor-fold Automation_table_configs:
class Automation_table_configs:
    def __init__(self, ll_base_chance = 1/6, lm_base_chance = 1/6,
                 lr_base_chance = 1/6, rl_base_chance = 1/6,
                 rm_base_chance = 1/6, rr_base_chance = 1/6,
                 footedness_left_text = "Left",
                 footedness_right_text = "Right",
                 aim_direction_left_text = "Left",
                 aim_direction_middle_text = "Middle",
                 aim_direction_right_text = "Right",
                 footedness_column_title = "Striker Footedness",
                 aim_direction_column_title = "Striker Aim Direction",
                 chances_column_title = "Chance", table_width = 600,
                 table_height = 280,
                 table_autosize_mode = "force_fit",
                 table_visibility = False):
        self.ll_base_chance = ll_base_chance
        self.lm_base_chance = lm_base_chance
        self.lr_base_chance = lr_base_chance
        self.rl_base_chance = rl_base_chance
        self.rm_base_chance = rm_base_chance
        self.rr_base_chance = rr_base_chance
        self.footedness_left_text = footedness_left_text
        self.footedness_right_text = footedness_right_text
        self.aim_direction_left_text = aim_direction_left_text
        self.aim_direction_middle_text = aim_direction_middle_text
        self.aim_direction_right_text = aim_direction_right_text

        self.footedness_column_title = footedness_column_title
        self.aim_direction_column_title = aim_direction_column_title
        self.chances_column_title = chances_column_title
        self.table_width = table_width
        self.table_height = table_height
        self.table_autosize_mode = table_autosize_mode
        self.table_visibility = table_visibility
#</editor-fold>
#<editor-fold layout_configs:
class Layout_configs:
    def __init__(self, automate_button_row_max_width = 400,
                 automate_button_row_sizing_mode = 'stretch_width',
                 strategy_dropdown_row_max_width = 400,
                 strategy_dropdown_row_sizing_mode = 'stretch_width',
                 start_automate_row_max_width = 400,
                 start_automate_row_sizing_mode = 'stretch_width',
                 automate_aim_rows_max_width = 400,
                 automate_aim_rows_sizing_mode = 'stretch_width',
                 game_stats_row_1_max_width = 600,
                 game_stats_row_1_sizing_mode = 'stretch_width',
                 game_stats_row_2_max_width = 600,
                 game_stats_row_2_sizing_mode = 'stretch_width',
                 gui_column1_max_width = 600,
                 gui_column1_sizing_mode = 'stretch_width',
                 gui_column2_min_width = 761, gui_column2_max_width = 761,
                 gui_column2_sizing_mode = 'stretch_width',
                 gui_row_max_width = 1400,
                 gui_row_sizing_mode = 'stretch_width',
                 plot_width = 1200, plot_height = 480,
                 b_fig_rows_max_width = 400,
                 b_fig_rows_sizing_mode = 'stretch_width'):
        self.automate_button_row_max_width = automate_button_row_max_width
        self.automate_button_row_sizing_mode = automate_button_row_sizing_mode
        self.strategy_dropdown_row_max_width = strategy_dropdown_row_max_width
        self.strategy_dropdown_row_sizing_mode = strategy_dropdown_row_sizing_mode
        self.start_automate_row_max_width = start_automate_row_max_width
        self.start_automate_row_sizing_mode = start_automate_row_sizing_mode
        self.automate_aim_rows_max_width = automate_aim_rows_max_width
        self.automate_aim_rows_sizing_mode = automate_aim_rows_sizing_mode
        self.game_stats_row_1_max_width = game_stats_row_1_max_width
        self.game_stats_row_1_sizing_mode = game_stats_row_1_sizing_mode
        self.game_stats_row_2_max_width = game_stats_row_2_max_width
        self.game_stats_row_2_sizing_mode = game_stats_row_2_sizing_mode
        self.gui_column1_max_width = gui_column1_max_width
        self.gui_column1_sizing_mode = gui_column1_sizing_mode
        self.gui_column2_min_width = gui_column2_min_width
        self.gui_column2_max_width = gui_column2_max_width
        self.gui_column2_sizing_mode = gui_column2_sizing_mode
        self.gui_row_max_width = gui_row_max_width
        self.gui_row_sizing_mode = gui_row_sizing_mode
        self.plot_width = plot_width
        self.plot_height = plot_height
        self.b_fig_rows_max_width = b_fig_rows_max_width
        self.b_fig_rows_sizing_mode = b_fig_rows_sizing_mode
#</editor-fold>

#<editor-fold make_game():
#Needs:
#    from main_game_figure import game_figure_setup, Game_fig_configs
#    from game_stats_figure_1 import stats_figure_1_setup, Stats_fig_1_configs
#    from game_stats_figure_2 import stats_figure_2_setup, Stats_fig_2_configs
#    from game_stats_figure_3 import stats_figure_3_setup, Stats_fig_3_configs
#<editor-fold Define defaults:
default_game_fig_configs = figs.game_fig.Game_fig_configs()
default_fig_1_configs = figs.stats_fig_1.Stats_fig_1_configs()
default_fig_2_configs = figs.stats_fig_2.Stats_fig_2_configs()
default_fig_3_configs = figs.stats_fig_3.Stats_fig_3_configs()
default_fig_4_configs = figs.stats_fig_4.Stats_fig_4_configs()
default_scr_text_and_labels_configs = Scr_text_and_labels_configs()
default_gamestate_divs_configs = Gamestate_divs_configs()
default_button_configs = Button_configs()
default_slider_configs = Slider_configs()
default_strategy_dropdown_configs = Strategy_dropdown_configs()
default_distribution_table_configs = Distribution_table_configs()
default_automation_table_configs = Automation_table_configs()
default_layout_configs = Layout_configs()
#</editor-fold>

class Game_parts:
    def __init__(self):
        self.buttons = {}
        self.divs = {}
        self.dropdowns = {}
        self.labels = {}
        self.sliders = {}
        self.tables = {}
        self.sources = {}
        self.texts = {}
        self.textinputs = {}
        self.figures = {}
        self.glyphs = {}
def make_game(game_figure_configs = default_game_fig_configs,
              stats_figure_1_configs = default_fig_1_configs,
              stats_figure_2_configs = default_fig_2_configs,
              stats_figure_3_configs = default_fig_3_configs,
              stats_figure_4_configs = default_fig_4_configs,
              scrtxt_labels_configs = default_scr_text_and_labels_configs,
              divs_configs = default_gamestate_divs_configs,
              button_configs = default_button_configs,
              slider_configs = default_slider_configs,
              strategy_dropdown_configs = default_strategy_dropdown_configs,
              distribution_table_configs = default_distribution_table_configs,
              automation_table_configs = default_automation_table_configs,
              layout_configs = default_layout_configs):
    game_parts = {}
    game_parts = Game_parts()
    #<editor-fold create objects used in game:
    figs.game_fig.game_figure_setup(game_figure_configs, game_parts)
    figs.stats_fig_1.stats_figure_1_setup(stats_figure_1_configs, game_parts)
    figs.stats_fig_2.stats_figure_2_setup(stats_figure_2_configs, game_parts)
    figs.stats_fig_3.stats_figure_3_setup(stats_figure_3_configs, game_parts)
    figs.stats_fig_4.stats_figure_4_setup(stats_figure_4_configs, game_parts)

    components.text.scr_text.create(game_parts)
    components.labels.scr_labels.create(game_parts)

    game_parts.figures['game_figure'].add_glyph(game_parts.texts['scr_text'],
                                                game_parts.labels['scr_text'])

    components.divs.iterations_to_run.create(game_parts)
    components.divs.strategy_to_use.create(game_parts)
    components.divs.nround.create(game_parts)
    components.divs.score.create(game_parts)
    components.divs.kicker_foot.create(game_parts)
    components.divs.kicker_kick.create(game_parts)
    components.divs.cpu_selected.create(game_parts)
    components.divs.chances_valid.create(game_parts)
    components.divs.counter_made.create(game_parts)

    components.buttons.b_automate.create(game_parts)
    components.buttons.b_start_automate.create(game_parts)
    components.buttons.b_auto_next.create(game_parts)
    components.buttons.b_make_counter.create(game_parts)
    components.buttons.b_fig_1.create(game_parts)
    components.buttons.b_fig_2.create(game_parts)
    components.buttons.b_fig_3.create(game_parts)
    components.buttons.b_fig_4.create(game_parts)

    components.sliders.iterations_slider.create(game_parts)

    components.textinputs.aim_text_input.create(game_parts = game_parts,
                                                name = "ll")
    components.textinputs.aim_text_input.create(game_parts = game_parts,
                                                name = "lm")
    components.textinputs.aim_text_input.create(game_parts = game_parts,
                                                name = "lr")
    components.textinputs.aim_text_input.create(game_parts = game_parts,
                                                name = "rl")
    components.textinputs.aim_text_input.create(game_parts = game_parts,
                                                name = "rm")
    components.textinputs.aim_text_input.create(game_parts = game_parts,
                                                name = "rr")

    components.dropdowns.cpu_strategy_dropdown.create(game_parts)

    components.tablesources.distribution_table_source.create(game_parts)
    components.tables.distribution_table.create(game_parts)

    components.tablesources.automation_table_source.create(game_parts)
    components.tables.automation_table.create(game_parts)
    #</editor-fold>

    #<editor-fold setup created objects:
    components.buttons.b_automate.setup(game_parts)

    components.divs.cpu_selected.setup(game_parts)
    components.divs.chances_valid.setup(game_parts)
    components.divs.counter_made.setup(game_parts)

    components.buttons.b_make_counter.setup(game_parts)

    components.buttons.b_fig_1.setup(game_parts)
    components.buttons.b_fig_2.setup(game_parts)
    components.buttons.b_fig_3.setup(game_parts)
    components.buttons.b_fig_4.setup(game_parts)

    components.buttons.b_start_automate.setup(game_parts)

    components.buttons.b_auto_next.setup(game_parts)

    components.sliders.iterations_slider.setup(game_parts)

    components.textinputs.aim_text_input.setup(name = "ll",
                                               game_parts = game_parts)
    components.textinputs.aim_text_input.setup(name = "lm",
                                               game_parts = game_parts)
    components.textinputs.aim_text_input.setup(name = "lr",
                                               game_parts = game_parts)
    components.textinputs.aim_text_input.setup(name = "rl",
                                               game_parts = game_parts)
    components.textinputs.aim_text_input.setup(name = "rm",
                                               game_parts = game_parts)
    components.textinputs.aim_text_input.setup(name = "rr",
                                               game_parts = game_parts)

    components.dropdowns.cpu_strategy_dropdown.setup(game_parts)
    #</editor-fold>

    grid1 = game_layout.format(game_parts)

    return grid1
#</editor-fold>
