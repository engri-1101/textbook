from . import gamecomponents as components
from collections import namedtuple
from . import game_layout
from . import gamefigures as figs

#<editor-fold _GameParts:
class _GameParts:
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
#</editor-fold>

#<editor-fold Config Classes:
class _TextConfig:
    def __init__(self, xs, ys, text_lines):
        self.xs = xs
        self.ys = ys
        self.text_lines = text_lines
class _LabelsConfig:
    def __init__(self,  text_color, text_font_size, text_x_offset,
                 text_y_offset, text_baseline, text_align):
        self.text_color = text_color
        self.text_font_size = text_font_size
        self.text_x_offset = text_x_offset
        self.text_y_offset = text_y_offset
        self.text_baseline = text_baseline
        self.text_align = text_align
class _ButtonConfig:
    def __init__(self, label, button_type, sizing_mode, width_policy, disabled,
                 visible):
        self.label = label
        self.button_type = button_type
        self.sizing_mode = sizing_mode
        self.width_policy = width_policy
        self.disabled = disabled
        self.visible = visible
class _DivConfig:
    def __init__(self, text, visible):
        self.text = text
        self.visible = visible
class _SliderConfig:
    def __init__(self, start, end, value, step, title, disabled, visible):
        self.start = start
        self.end = end
        self.value = value
        self.step = step
        self.title = title
        self.disabled = disabled
        self.visible = visible
class _TextInputConfig:
    def __init__(self, value, title_addition, visible):
        self.value = value
        self.title_addition = title_addition
        self.visible = visible
class _DropdownConfig:
    def __init__(self, items, label, button_type, disabled, visible):
        new_items = []
        for item in items:
            new_items.append((item, item))
        self.items = new_items
        self.label = label
        self.button_type = button_type
        self.disabled = disabled
        self.visible = visible
class _TableFootednessConfig:
    def __init__(self, footedness_left_text, footedness_right_text,
                 aim_direction_left_text, aim_direction_middle_text,
                 aim_direction_right_text):
        self.footedness_left_text = footedness_left_text
        self.footedness_right_text = footedness_right_text
        self.aim_direction_left_text = aim_direction_left_text
        self.aim_direction_middle_text = aim_direction_middle_text
        self.aim_direction_right_text = aim_direction_right_text
class _DistTableConfig:
    def __init__(self, titles, width, height, autosize_mode, sizing_mode,
                 visible, fit_columns, column_widths):
        self.titles = titles
        self.width = width
        self.height = height
        self.autosize_mode = autosize_mode
        self.sizing_mode = sizing_mode
        self.visible = visible
        self.fit_columns = fit_columns
        self.column_widths = column_widths
class _AutoTableConfig:
    def __init__(self, titles, width, height, autosize_mode, visible):
        self.titles = titles
        self.width = width
        self.height = height
        self.autosize_mode = autosize_mode
        self.visible = visible
class _LayoutConfig:
    def __init__(self, automate_button_row_max_width,
                 automate_button_row_sizing_mode,
                 strategy_dropdown_row_max_width,
                 strategy_dropdown_row_sizing_mode,
                 start_automate_row_max_width, start_automate_row_sizing_mode,
                 automate_aim_rows_max_width, automate_aim_rows_sizing_mode,
                 game_stats_row_max_width, game_stats_row_sizing_mode,
                 gui_column1_max_width, gui_column1_sizing_mode,
                 gui_column2_min_width, gui_column2_max_width,
                 gui_column2_sizing_mode, gui_row_max_width,
                 gui_row_sizing_mode, plot_width, plot_height,
                 b_fig_rows_max_width, b_fig_rows_sizing_mode):
        self.automate_button_row_max_width = start_automate_row_max_width
        self.automate_button_row_sizing_mode = start_automate_row_sizing_mode
        self.strategy_dropdown_row_max_width = strategy_dropdown_row_max_width
        self.strategy_dropdown_row_sizing_mode = strategy_dropdown_row_sizing_mode
        self.start_automate_row_max_width = start_automate_row_max_width
        self.start_automate_row_sizing_mode = start_automate_row_sizing_mode
        self.automate_aim_rows_max_width = automate_aim_rows_max_width
        self.automate_aim_rows_sizing_mode = automate_aim_rows_sizing_mode
        self.game_stats_row_max_width = game_stats_row_max_width
        self.game_stats_row_sizing_mode = game_stats_row_sizing_mode
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

#<editor-fold MainGame:
class MainGame:
    def __init__(self):
        self.game_parts = _GameParts()
        #<editor-fold Button Configs:
        self.b_automate = _ButtonConfig("Automate", "success", "scale_width",
                                        "fit", False, True)
        self.b_start_automate = _ButtonConfig("Start", "success", "scale_width",
                                              "fit", False, False)
        self.b_auto_next = _ButtonConfig("Next", "success", "scale_width",
                                         "fit", False, False)
        self.b_make_counter = _ButtonConfig("Make Counter", "success",
                                            "scale_width", "fit", False, False)
        self.b_fig_1 = _ButtonConfig("Figure 1", "success", "scale_width",
                                     "fit", True, False)
        self.b_fig_2 = _ButtonConfig("Figure 2", "success", "scale_width",
                                     "fit", False, False)
        self.b_fig_3 = _ButtonConfig("Figure 3", "success", "scale_width",
                                     "fit", False, False)
        self.b_fig_4 = _ButtonConfig("Figure 4", "success", "scale_width",
                                     "fit", False, False)
        self.b_auto_advance = _ButtonConfig("Fast Forward", "success",
                                            "scale_width", "fit", False, False)
        #</editor-fold>
        #<editor-fold Gameview Configs:
        self.scr_text = _TextConfig([2, 70, 2, 14, 14], [86, 86, 5, 40, 32],
                                    ['Rounds played: 0', 'Total score: 0', '',
                                     '', ''])
        self.scr_labels = _LabelsConfig(text_color = "whitesmoke",
                                        text_font_size = "15pt",
                                        text_x_offset = 0, text_y_offset = +9,
                                        text_baseline = "ideographic",
                                        text_align = 'left')
        #</editor-fold>
        #<editor-fold Div Configs:
        self.iterations_to_run = _DivConfig("50", False)
        self.strategy_to_use = _DivConfig("Not Set", False)
        self.nround = _DivConfig("0", False)
        self.score = _DivConfig("0", False)
        self.kicker_foot = _DivConfig("", False)
        self.kicker_kick = _DivConfig("", False)
        #</editor-fold>
        #<editor-fold Slider Configs:
        self.iterations_slider = _SliderConfig(start = 10, end = 500,
                                               value = 50, step = 10,
                                               title = "Iterations To Run",
                                               disabled = False,
                                               visible = False)
        #</editor-fold>
        #<editor-fold TextInput Configs:
        self.aim_text_inputs = _TextInputConfig(value = "0",
                                                title_addition = "_aim_chance",
                                                visible = False)
        #</editor-fold>
        #<editor-fold Dropdown Configs:
        self.cpu_strategy_dropdown = _DropdownConfig(["Fictitious_Play",
                                                      "Mixed_Strategy",
                                                      "Random",
                                                      "Goalie_Cheats"],
                                                     label = "CPU strategy to Use",
                                                     button_type = "warning",
                                                     disabled = False,
                                                     visible = False)
        #</editor-fold>
        #<editor-fold Table Configs:
        self.footedness_config = _TableFootednessConfig(footedness_left_text = "Left",
                                                        footedness_right_text = "Right",
                                                        aim_direction_left_text = "Left",
                                                        aim_direction_middle_text = "Middle",
                                                        aim_direction_right_text = "Right")
        self.base_chances = [0,0,0,0,0,0]
        self.initial_stats = {'freq' : [0,0,0,0,0,0],
                              'decisions' : [0,0,0,0,0,0],
                              'perceived_risks' : [0,0,0,0,0,0],
                              'score_chance' : [0,0,0,0,0,0],
                              'score_roll' : [0,0,0,0,0,0]}
        self.distribution_table = _DistTableConfig(["Striker Footedness",
                                                    "Striker Aim Direction",
                                                    "Frequency",
                                                    "Goalie Decisions",
                                                    "Goalie Perceived Risks",
                                                    "Striker's Score Chance",
                                                    "Striker's Score Roll"],
                                                   711, 280, "force_fit",
                                                   "scale_width", False, False,
                                                   [101, 107, 60, 90, 130, 120,
                                                    103])
        self.automation_table = _AutoTableConfig(["Striker Footedness",
                                                  "Striker Aim Direction",
                                                  "Chance"], 600, 280,
                                                 "force_fit", False)
        #</editor-fold>
        #<editor-fold Layout Configs:
        self.layout = _LayoutConfig(automate_button_row_max_width = 400,
                                    automate_button_row_sizing_mode = 'stretch_width',
                                    strategy_dropdown_row_max_width = 400,
                                    strategy_dropdown_row_sizing_mode = 'stretch_width',
                                    start_automate_row_max_width = 400,
                                    start_automate_row_sizing_mode = 'stretch_width',
                                    automate_aim_rows_max_width = 400,
                                    automate_aim_rows_sizing_mode = 'stretch_width',
                                    game_stats_row_max_width = 600,
                                    game_stats_row_sizing_mode = 'stretch_width',
                                    gui_column1_max_width = 600,
                                    gui_column1_sizing_mode = 'stretch_width',
                                    gui_column2_min_width = 761,
                                    gui_column2_max_width = 761,
                                    gui_column2_sizing_mode = 'stretch_width',
                                    gui_row_max_width = 1400,
                                    gui_row_sizing_mode = 'stretch_width',
                                    plot_width = 1200,
                                    plot_height = 480,
                                    b_fig_rows_max_width = 400,
                                    b_fig_rows_sizing_mode ='stretch_width')
        #</editor-fold>

    def __make_game_components(self):
        figs.game_fig.game_figure_setup(self.game_parts)
        figs.stats_fig_1.stats_figure_1_setup(self.game_parts)
        figs.stats_fig_2.stats_figure_2_setup(self.game_parts)
        figs.stats_fig_3.stats_figure_3_setup(self.game_parts)
        figs.stats_fig_4.stats_figure_4_setup(self.game_parts)

        #<editor-fold Gameview Text:
        components.text.scr_text.create(self.game_parts, self.scr_text)
        components.labels.scr_labels.create(self.game_parts, self.scr_labels)

        self.game_parts.figures['game_figure'].add_glyph(self.game_parts.texts['scr_text'],
                                                         self.game_parts.labels['scr_text'])
        #</editor-fold>

        #<editor-fold Divs:
        components.divs.iterations_to_run.create(self.game_parts,
                                                 self.iterations_to_run)
        components.divs.strategy_to_use.create(self.game_parts,
                                               self.strategy_to_use)
        components.divs.nround.create(self.game_parts, self.nround)
        components.divs.score.create(self.game_parts, self.score)
        components.divs.kicker_foot.create(self.game_parts, self.kicker_foot)
        components.divs.kicker_kick.create(self.game_parts, self.kicker_kick)
        components.divs.select_cpu_tip.create(self.game_parts)
        components.divs.chances_lt_0_tip.create(self.game_parts)
        components.divs.chances_gt_1_tip.create(self.game_parts)
        components.divs.chances_ne_1_tip.create(self.game_parts)
        components.divs.cpu_selected.create(self.game_parts)
        components.divs.chances_valid.create(self.game_parts)
        components.divs.counter_made.create(self.game_parts)
        components.divs.in_an_iter.create(self.game_parts)
        #</editor-fold>

        #<editor-fold Buttons
        components.buttons.b_automate.create(self.game_parts, self.b_automate)
        components.buttons.b_start_automate.create(self.game_parts,
                                                   self.b_start_automate)
        components.buttons.b_auto_next.create(self.game_parts, self.b_auto_next)
        components.buttons.b_make_counter.create(self.game_parts,
                                                 self.b_make_counter)
        components.buttons.b_fig_1.create(self.game_parts, self.b_fig_1)
        components.buttons.b_fig_2.create(self.game_parts, self.b_fig_2)
        components.buttons.b_fig_3.create(self.game_parts, self.b_fig_3)
        components.buttons.b_fig_4.create(self.game_parts, self.b_fig_4)
        components.buttons.b_auto_advance.create(self.game_parts,
                                                 self.b_auto_advance)
        #</editor-fold>

        components.sliders.iterations_slider.create(self.game_parts,
                                                    self.iterations_slider)

        #<editor-fold TextInputs:
        components.textinputs.aim_text_input.create(self.game_parts,
                                                    "ll", self.aim_text_inputs)
        components.textinputs.aim_text_input.create(self.game_parts,
                                                    "lm",self. aim_text_inputs)
        components.textinputs.aim_text_input.create(self.game_parts,
                                                    "lr", self.aim_text_inputs)
        components.textinputs.aim_text_input.create(self.game_parts,
                                                    "rl", self.aim_text_inputs)
        components.textinputs.aim_text_input.create(self.game_parts,
                                                    "rm", self.aim_text_inputs)
        components.textinputs.aim_text_input.create(self.game_parts,
                                                    "rr", self.aim_text_inputs)
        #</editor-fold>

        components.dropdowns.cpu_strategy_dropdown.create(self.game_parts,
                                                          self.cpu_strategy_dropdown)

        #<editor-fold Stat Tables:
        components.tablesources.distribution_table_source.create(self.game_parts,
                                                                 self.footedness_config,
                                                                 self.initial_stats)
        components.tables.distribution_table.create(self.game_parts,
                                                    self.distribution_table)

        components.tablesources.automation_table_source.create(self.game_parts,
                                                               self.footedness_config,
                                                               self.base_chances)
        components.tables.automation_table.create(self.game_parts,
                                                  self.automation_table)
        #</editor-fold>

    def __setup_game_components(self):

        components.buttons.b_automate.setup(self.game_parts)

        components.divs.cpu_selected.setup(self.game_parts)
        components.divs.chances_valid.setup(self.game_parts)
        components.divs.counter_made.setup(self.game_parts)

        components.divs.in_an_iter.setup(self.game_parts)

        components.buttons.b_make_counter.setup(self.game_parts)

        components.buttons.b_fig_1.setup(self.game_parts)
        components.buttons.b_fig_2.setup(self.game_parts)
        components.buttons.b_fig_3.setup(self.game_parts)
        components.buttons.b_fig_4.setup(self.game_parts)

        components.buttons.b_start_automate.setup(self.game_parts)

        components.buttons.b_auto_next.setup(self.game_parts)

        components.sliders.iterations_slider.setup(self.game_parts)

        components.textinputs.aim_text_input.setup(name = "ll",
                                                   game_parts = self.game_parts)
        components.textinputs.aim_text_input.setup(name = "lm",
                                                   game_parts = self.game_parts)
        components.textinputs.aim_text_input.setup(name = "lr",
                                                   game_parts = self.game_parts)
        components.textinputs.aim_text_input.setup(name = "rl",
                                                   game_parts = self.game_parts)
        components.textinputs.aim_text_input.setup(name = "rm",
                                                   game_parts = self.game_parts)
        components.textinputs.aim_text_input.setup(name = "rr",
                                                   game_parts = self.game_parts)

        components.dropdowns.cpu_strategy_dropdown.setup(self.game_parts)

    def __format_game_layout(self):
        grid1 = game_layout.format(self.game_parts, self.layout)
        return grid1

    def make_game(self):
        self.__make_game_components()
        self.__setup_game_components()
        grid1 = self.__format_game_layout()
        return grid1
#</editor-fold>
