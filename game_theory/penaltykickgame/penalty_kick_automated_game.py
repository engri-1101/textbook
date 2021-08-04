from . import gamecomponents as components
from . import game_layout
from . import gamefigures as figs
import asyncio
INDENT = "    "
B_FIG_NAMES = ["game_fig", "fig_1", "fig_2", "fig_3", "fig_4"]
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
    def __init__(
            self, text_color, text_font_size, text_x_offset, text_y_offset,
            text_baseline, text_align
        ):
        self.text_color = text_color
        self.text_font_size = text_font_size
        self.text_x_offset = text_x_offset
        self.text_y_offset = text_y_offset
        self.text_baseline = text_baseline
        self.text_align = text_align

class _ButtonConfig:
    def __init__(
            self, label, button_type, sizing_mode, width_policy, disabled,
            visible
        ):
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
    def __init__(
            self, footedness_left_text, footedness_right_text,
            aim_direction_left_text, aim_direction_middle_text,
            aim_direction_right_text
        ):
        self.footedness_left_text = footedness_left_text
        self.footedness_right_text = footedness_right_text
        self.aim_direction_left_text = aim_direction_left_text
        self.aim_direction_middle_text = aim_direction_middle_text
        self.aim_direction_right_text = aim_direction_right_text

class _DistTableConfig:
    def __init__(
            self, titles, width, height, autosize_mode, sizing_mode, visible,
            fit_columns, column_widths
        ):
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
    def __init__(
            self, figs_col_min_width, figs_col_max_width, figs_col_sizing_mode,
            interactables_col_min_width, interactables_col_max_width,
            interactables_col_sizing_mode, plot_width, plot_height
        ):

        self.figs_col_min_width = figs_col_min_width
        self.figs_col_max_width = figs_col_max_width
        self.figs_col_sizing_mode = figs_col_sizing_mode

        self.interactables_col_min_width = interactables_col_min_width
        self.interactables_col_max_width = interactables_col_max_width
        self.interactables_col_sizing_mode = interactables_col_sizing_mode

        self.plot_width = plot_width
        self.plot_height = plot_height
#</editor-fold>

#<editor-fold MainGame:
class MainGame:
    def __init__(self):
        self.stats_fig_1 = figs.stats_fig_1.Configs()
        self.stats_fig_2 = figs.stats_fig_2.Configs()
        self.stats_fig_3 = figs.stats_fig_3.Configs()
        self.stats_fig_4 = figs.stats_fig_4.Configs()
        self.game_fig = figs.game_fig.Configs()
        self.game_parts = _GameParts()
        #<editor-fold Button Configs:
        self.b_automate = _ButtonConfig(
            label="Automate", button_type="success", sizing_mode="scale_width",
            width_policy="fit", disabled=False, visible=True
        )
        self.b_start_automate = _ButtonConfig(
            label="Start", button_type="success",
            sizing_mode="scale_width", width_policy="fit", disabled=False,
            visible=False
        )
        self.b_auto_next = _ButtonConfig(
            label="Next", button_type="success",
            sizing_mode="scale_width", width_policy="fit", disabled=False,
            visible=False
        )
        self.b_make_counter = _ButtonConfig(
            label="Make Counter", button_type="success",
            sizing_mode="scale_width", width_policy="fit", disabled=False,
            visible=False
        )
        self.b_auto_advance = _ButtonConfig(
            label="Fast Forward", button_type="success",
            sizing_mode="scale_width", width_policy="fit", disabled=False,
            visible=False
        )

        b_fig_labels = [
            "Game Figure", "Figure 1", "Figure 2", "Figure 3", "Figure 4"
        ]
        b_fig_disableds = [True, False, False, False, False]
        self.b_fig_configs = []
        for i in range(len(B_FIG_NAMES)):
            button_config = _ButtonConfig(
                label=b_fig_labels[i], button_type="success",
                sizing_mode="scale_width", width_policy="fit",
                disabled=b_fig_disableds[i], visible=False
            )
            self.b_fig_configs.append(button_config)
        #</editor-fold>

        #<editor-fold Gameview Configs:
        self.scr_text = _TextConfig(
            xs=[2, 70, 2, 14, 14], ys=[86, 86, 5, 40, 32],
            text_lines=["Rounds played: 0", "Total score: 0", "", "", ""]
        )
        self.scr_labels = _LabelsConfig(
            text_color="whitesmoke", text_font_size="15pt", text_x_offset=0,
            text_y_offset=9, text_baseline="ideographic", text_align="left"
        )
        #</editor-fold>

        #<editor-fold Div Configs:
        self.select_cpu_tip = _DivConfig(
            text="Select A CPU Strategy From the Dropdown", visible=False
        )
        self.chances_gt_1_tip = _DivConfig(
            text="Chances cannot be greater than 1", visible=False
        )
        self.chances_lt_0_tip = _DivConfig(
            text="Chances cannot be less than 0", visible=False
        )
        self.chances_ne_1_tip = _DivConfig(
            text="Chances must add up to 1", visible=False
        )
        #</editor-fold>

        #<editor-fold Slider Configs:
        self.iterations_slider = _SliderConfig(
            start=10, end=500, value=50, step=10, title="Iterations To Run",
            disabled=False, visible=False
        )
        self.auto_advance_speed_slider = _SliderConfig(
            start=50, end=1000, value=300, step=10,
            title="Auto Advance Delay (ms)", disabled=False, visible=False
        )
        #</editor-fold>

        #<editor-fold TextInput Configs:
        self.aim_text_inputs = _TextInputConfig(
            value="0", title_addition="_aim_chance", visible=False
        )
        #</editor-fold>

        #<editor-fold Dropdown Configs:
        dropdown_items = [
            "Fictitious_Play", "Mixed_Strategy", "Random", "Goalie_Cheats"
        ]
        self.cpu_strategy_dropdown = _DropdownConfig(
            items=dropdown_items, label="CPU strategy to Use",
            button_type="warning", disabled=False, visible=False
        )
        #</editor-fold>

        #<editor-fold Table Configs:
        self.footedness_config = _TableFootednessConfig(
            footedness_left_text="Left", footedness_right_text="Right",
            aim_direction_left_text="Left", aim_direction_middle_text="Middle",
            aim_direction_right_text="Right"
        )
        self.base_chances = [0, 0, 0, 0, 0, 0]
        self.initial_stats = {
            "freq" : [0, 0, 0, 0, 0, 0],
            "decisions" : [0, 0, 0, 0, 0, 0],
            "perceived_risks" : [0, 0, 0, 0, 0, 0],
            "score_chance" : [0, 0, 0, 0, 0, 0],
            "score_roll" : [0, 0, 0, 0, 0, 0],
        }
        dist_table_titles = [
            "Footedness", "Aim Direction", "Frequency", "Decisions",
            "Perceived Risks", "Score Chance", "Score Roll"
        ]

        self.distribution_table = _DistTableConfig(
            titles=dist_table_titles, width=600, height=280,
            autosize_mode="fit_columns", sizing_mode="stretch_width",
            visible=False, fit_columns=False,
            column_widths=[77, 84, 69, 64, 97, 88, 74]
        )

        self.automation_table = _AutoTableConfig(
            titles=["Striker Footedness", "Striker Aim Direction", "Chance"],
            width=600, height=280, autosize_mode="force_fit", visible=False
        )
        #</editor-fold>

        #<editor-fold Layout Configs:
        self.layout = _LayoutConfig(
            figs_col_min_width=600, figs_col_max_width=600,
            figs_col_sizing_mode="stretch_width",
            interactables_col_min_width=300, interactables_col_max_width=300,
            interactables_col_sizing_mode="stretch_width", plot_width=900,
            plot_height=480
        )
        #</editor-fold>

    #<editor-fold __make_game_components():
    async def __make_game_components(self, text_queue, log_steps=False):
        loop = asyncio.get_running_loop()
        #<editor-fold Game Figs:
        await text_queue.put(INDENT + "Creating game figs:")
        await loop.run_in_executor(
            None, figs.game_fig.create, self.game_parts, self.game_fig
        )
        await text_queue.put(INDENT + INDENT + "Main game fig created")
        await loop.run_in_executor(
            None, figs.stats_fig_1.create, self.game_parts, self.stats_fig_1
        )
        await text_queue.put(INDENT + INDENT + "Game stats fig 1 created")
        await loop.run_in_executor(
            None, figs.stats_fig_2.create, self.game_parts, self.stats_fig_2
        )
        await text_queue.put(INDENT + INDENT + "Game stats fig 2 created")
        await loop.run_in_executor(
            None, figs.stats_fig_3.create, self.game_parts, self.stats_fig_3
        )
        await text_queue.put(INDENT + INDENT + "Game stats fig 3 created")
        await loop.run_in_executor(
            None, figs.stats_fig_4.create, self.game_parts, self.stats_fig_4
        )
        await text_queue.put(INDENT + INDENT + "Game stats fig 4 created")
        await text_queue.put(INDENT + "Game fig creation completed")
        #</editor-fold>

        #<editor-fold Gameview Text:
        await text_queue.put("")
        await text_queue.put(INDENT + "Creating game fig screen text:")
        await loop.run_in_executor(
            None, components.text.scr_text.create, self.game_parts,
            self.scr_text
        )
        await text_queue.put(INDENT + INDENT + "scr_text created")
        await loop.run_in_executor(
            None, components.labels.scr_labels.create, self.game_parts,
            self.scr_labels
        )
        await text_queue.put(INDENT + INDENT + "scr_labels created")

        self.game_parts.figures["game_figure"].add_glyph(
            self.game_parts.texts["scr_text"],
            self.game_parts.labels["scr_text"]
        )

        await text_queue.put(
            INDENT + INDENT + "Added scr_text and scr_labels to main game fig"
        )
        await text_queue.put(INDENT + "Game fig screen text creation completed")
        #</editor-fold>

        #<editor-fold Divs:
        await text_queue.put("")
        await text_queue.put(INDENT + "Creating game divs:")
        await loop.run_in_executor(
            None, components.divs.basic.create_game_vars, self.game_parts
        )
        await text_queue.put(INDENT + "Basic game value tracking divs created")
        await loop.run_in_executor(
            None, components.divs.basic.create_configurable, self.game_parts,
            self.select_cpu_tip, "select_cpu_tip"
        )
        await loop.run_in_executor(
            None, components.divs.basic.create_configurable, self.game_parts,
            self.chances_lt_0_tip, "chances_lt_0_tip"
        )
        await loop.run_in_executor(
            None, components.divs.basic.create_configurable, self.game_parts,
            self.chances_gt_1_tip, "chances_gt_1_tip"
        )
        await loop.run_in_executor(
            None, components.divs.basic.create_configurable, self.game_parts,
            self.chances_ne_1_tip, "chances_ne_1_tip"
        )
        await text_queue.put(INDENT + INDENT + "Game input tip divs created")
        await loop.run_in_executor(
            None, components.divs.cpu_selected.create, self.game_parts
        )
        await text_queue.put(
            INDENT + INDENT + "CPU selection status tracking div created"
        )
        await loop.run_in_executor(
            None, components.divs.chances_valid.create, self.game_parts
        )
        await text_queue.put(
            INDENT + INDENT + "User strategy validity tracking div created"
        )
        await loop.run_in_executor(
            None, components.divs.counter_made.create, self.game_parts
        )
        await text_queue.put(
            INDENT + INDENT + "Goalie cheats counter creation status"
            + " tracking div created"
        )
        await loop.run_in_executor(
            None, components.divs.in_an_iter.create, self.game_parts
        )
        await text_queue.put(
            INDENT + INDENT
            + "Game iteration running status tracking div created"
        )
        await text_queue.put(INDENT + "Game div creation completed")
        #</editor-fold>

        #<editor-fold Buttons:
        await text_queue.put("")
        await text_queue.put(INDENT + "Creating buttons:")
        await loop.run_in_executor(
            None, components.buttons.b_automate.create, self.game_parts,
            self.b_automate
        )
        await text_queue.put(
            INDENT + INDENT
            + "Game automate track selection button created"
        )
        await loop.run_in_executor(
            None, components.buttons.b_start_automate.create, self.game_parts,
            self.b_start_automate
        )
        await text_queue.put(
            INDENT + INDENT + "Game automate track start button created"
        )
        await loop.run_in_executor(
            None, components.buttons.b_auto_next.create, self.game_parts,
            self.b_auto_next
        )
        await text_queue.put(
            INDENT + INDENT + "Game automate track next button created"
        )
        await loop.run_in_executor(
            None, components.buttons.b_make_counter.create, self.game_parts,
            self.b_make_counter
        )
        await text_queue.put(
            INDENT + INDENT + "Goalie make counter button created"
        )
        for i in range(len(B_FIG_NAMES)):
            await loop.run_in_executor(
                None, components.buttons.b_figs.create, self.game_parts,
                self.b_fig_configs[i], B_FIG_NAMES[i]
            )
        await text_queue.put(
            INDENT + INDENT + "figure view selection buttons created"
        )
        await loop.run_in_executor(
            None, components.buttons.b_auto_advance.create, self.game_parts,
            self.b_auto_advance
        )
        await text_queue.put(
            INDENT + INDENT + "Game automation track auto advance iterations"
            + " toggle button created"
        )
        await text_queue.put(INDENT + "Button creation completed")
        #</editor-fold>

        #<editor-fold Sliders:
        await text_queue.put("")
        await text_queue.put(INDENT + "Creating sliders:")
        await loop.run_in_executor(
            None, components.sliders.basic.create, self.game_parts,
            self.iterations_slider, "iterations"
        )
        await text_queue.put(
            INDENT + INDENT + "Game iteration length selection slider created"
        )
        await loop.run_in_executor(
            None, components.sliders.basic.create, self.game_parts,
            self.auto_advance_speed_slider, "auto_advance_speed"
        )
        await text_queue.put(
            INDENT + INDENT + "Game automation track auto advance iteration"
            + " speed selection slider created"
        )
        await text_queue.put(INDENT + "Slider creation completed")
        #</editor-fold>

        #<editor-fold TextInputs:
        await text_queue.put("")
        await text_queue.put(INDENT + "Creating text inputs:")
        names = ["ll", "lm", "lr", "rl", "rm", "rr"]
        for name in names:
            await loop.run_in_executor(
                None, components.textinputs.aim_text_input.create,
                self.game_parts, name, self.aim_text_inputs
            )
            await text_queue.put(
                INDENT + INDENT + name + "_aim_text_input created"
            )
        await text_queue.put(INDENT + "Text input creation completed")
        #</editor-fold>

        #<editor-fold Dropdowns:
        await text_queue.put("")
        await text_queue.put(INDENT + "Creating dropdowns:")
        await loop.run_in_executor(
            None, components.dropdowns.cpu_strategy_dropdown.create,
            self.game_parts, self.cpu_strategy_dropdown
        )
        await text_queue.put(
            INDENT + INDENT + "CPU strategy to use dropdown created"
        )
        await text_queue.put(INDENT + "Dropdown creation completed")
        #</editor-fold>

        #<editor-fold Stat Tables:
        await text_queue.put("")
        await text_queue.put(INDENT + "Creating game tables:")
        await loop.run_in_executor(
            None, components.tablesources.distribution_table_source.create,
            self.game_parts, self.footedness_config, self.initial_stats
        )
        await text_queue.put(
            INDENT + INDENT + "Distribution table source created"
        )
        await loop.run_in_executor(
            None, components.tables.distribution_table.create, self.game_parts,
            self.distribution_table
        )
        await text_queue.put(INDENT + INDENT + "Distribution table created")
        await loop.run_in_executor(
            None, components.tablesources.automation_table_source.create,
            self.game_parts, self.footedness_config, self.base_chances
        )
        await text_queue.put(
            INDENT + INDENT + "Automation table source created"
        )
        await loop.run_in_executor(
            None, components.tables.automation_table.create, self.game_parts,
            self.automation_table
        )
        await text_queue.put(INDENT + INDENT + "Automation table created")
        await text_queue.put(INDENT + "Game table creation completed")
        #</editor-fold>
    #</editor-fold>

    #<editor-fold __setup_game_components():
    async def __setup_game_components(
        self, text_queue, log_steps=False, CPU_strategy=None,
        allow_fast_forward=True, force_fast_forward=False,
        force_fast_forward_spd=None, iterations_to_run=None,
        stats_fig_1_enabled=True, stats_fig_2_enabled=True,
        stats_fig_3_enabled = True, stats_fig_4_enabled=True,
        show_dist_table=False
    ):
        loop = asyncio.get_running_loop()
    # Click callback depends on CPU_strategy, allow_fast_forward,
    # force_fast_forward, force_fast_forward_spd, iterations_to_run:
        await loop.run_in_executor(
            None, components.buttons.b_automate.setup, self.game_parts,
            CPU_strategy, allow_fast_forward, force_fast_forward,
            force_fast_forward_spd, iterations_to_run
        )
        await text_queue.put(INDENT + "b_automate setup completed")
        if (CPU_strategy != None):
            await text_queue.put(
                INDENT + INDENT + "b_automate callback was adjusted to reflect"
                + " the pre-designated CPU Strategy."
            )
        if (allow_fast_forward == False):
            await text_queue.put(
                INDENT + INDENT + "b_automate callback was adjusted to reflect"
                + " that auto advancing should be disabled."
            )
        else:
            if (force_fast_forward == True):
                await text_queue.put(
                    INDENT + INDENT + "b_automate callback was adjusted to"
                    + " reflect that auto advancing should be forced."
                )
            if (force_fast_forward_spd != None):
                await text_queue.put(
                    INDENT + INDENT + "b_automate callback was adjusted to"
                    + " reflect that the auto advancing speed should be"
                    + " forcibly set to " + str(force_fast_forward_spd) + "."
                )
        if (iterations_to_run != None):
            await text_queue.put(
                INDENT + INDENT + "b_automate callback was adjusted to reflect"
                + " that the game should be forcibly set to "
                + str(iterations_to_run) + " iterations."
            )
        await loop.run_in_executor(
            None, components.divs.cpu_selected.setup, self.game_parts
        )
        await loop.run_in_executor(
            None, components.divs.chances_valid.setup, self.game_parts
        )
        await loop.run_in_executor(
            None, components.divs.counter_made.setup, self.game_parts
        )
        await text_queue.put(
            INDENT + "Start button prerequisite Div setups completed"
        )
        await loop.run_in_executor(
            None, components.divs.in_an_iter.setup, self.game_parts
        )
        await text_queue.put(
            INDENT + "Iteration running status tracking div setup completed"
        )
        await loop.run_in_executor(
            None, components.buttons.b_make_counter.setup, self.game_parts
        )
        await text_queue.put(INDENT + "Make counter button setup completed")
        for i in range(len(B_FIG_NAMES)):
            await loop.run_in_executor(
                None, components.buttons.b_figs.setup, self.game_parts,
                B_FIG_NAMES[i]
            )
        await text_queue.put(
            INDENT + "Game stat figure view selection button setups completed"
        )
        # Click callback depends on stats_fig_1_enabled, stats_fig_2_enabled,
        # stats_fig_3_enabled, stats_fig_4_enabled, show_dist_table:
        await loop.run_in_executor(
            None, components.buttons.b_start_automate.setup, self.game_parts,
            stats_fig_1_enabled, stats_fig_2_enabled, stats_fig_3_enabled,
            stats_fig_4_enabled, show_dist_table
        )
        await text_queue.put(
            INDENT + "Start automate track selection button setup completed"
        )
        if (stats_fig_1_enabled == False):
            await text_queue.put(
                INDENT + INDENT + "b_start_automate callback was adjusted to"
                + " reflect that stats fig 1 should be disabled."
            )
        if (stats_fig_2_enabled == False):
            await text_queue.put(
                INDENT + INDENT + "b_start_automate callback was adjusted to"
                + " reflect that stats fig 2 should be disabled."
            )
        if (stats_fig_3_enabled == False):
            await text_queue.put(
                INDENT + INDENT + "b_start_automate callback was adjusted to"
                + " reflect that stats fig 3 should be disabled."
            )
        if (stats_fig_4_enabled == False):
            await text_queue.put(
                INDENT + INDENT + "b_start_automate callback was adjusted to"
                + " reflect that stats fig 4 should be disabled."
            )
        if (show_dist_table == True):
            await text_queue.put(
                INDENT + INDENT + "b_automate callback was adjusted to reflect"
                + " that the distribution table should be shown."
            )
        # Click callback depends on stats_fig_1_enabled, stats_fig_2_enabled,
        # stats_fig_3_enabled, stats_fig_4_enabled:
        await loop.run_in_executor(
            None, components.buttons.b_auto_next.setup, self.game_parts,
            stats_fig_1_enabled, stats_fig_2_enabled, stats_fig_3_enabled,
            stats_fig_4_enabled
        )
        await text_queue.put(
            INDENT + "Automate track next button setup completed"
        )
        if (stats_fig_1_enabled == False):
            await text_queue.put(
                INDENT + INDENT + "b_auto_next callback was adjusted to reflect"
                + " that stats fig 1 should be disabled."
        )
        if (stats_fig_2_enabled == False):
            await text_queue.put(
                INDENT + INDENT + "b_auto_next callback was adjusted to reflect"
                + " that stats fig 2 should be disabled."
        )
        if (stats_fig_3_enabled == False):
            await text_queue.put(
                INDENT + INDENT + "b_auto_next callback was adjusted to reflect"
                + " that stats fig 3 should be disabled."
        )
        if (stats_fig_4_enabled == False):
            await text_queue.put(
                INDENT + INDENT + "b_auto_next callback was adjusted to reflect"
                + " that stats fig 4 should be disabled."
        )
        names = ["ll", "lm", "lr", "rl", "rm", "rr"]
        for name in names:
            await loop.run_in_executor(
                None, components.textinputs.aim_text_input.setup, name,
                self.game_parts
            )
        await text_queue.put(INDENT + "Aim text input setups completed")
        await loop.run_in_executor(
            None, components.dropdowns.cpu_strategy_dropdown.setup,
            self.game_parts
        )
        await text_queue.put(
            INDENT + "CPU strategy selection dropdown setup completed"
        )
    #</editor-fold>

    #<editor-fold __format_game_layout():
    async def __format_game_layout(self, text_queue, log_steps):
        grid1 = await game_layout.format(
            self.game_parts, self.layout, text_queue, log_steps
        )
        return grid1
    #</editor-fold>

    #<editor-fold make_game():
    async def log_step(self, text_queue, log_steps, CPU_strategy):
        keep_running = log_steps
        while keep_running:
            val = await text_queue.get()
            print(val)
            if (val == "Finished adjustments."):
                keep_running = False
                print("Done.")
            elif(CPU_strategy == None
                 and val == "Game layout formatting completed"):
                keep_running = False
                print("Done.")

    async def make_game(
        self, log_steps=False, CPU_strategy=None, allow_fast_forward=True,
        force_fast_forward=False, force_fast_forward_spd=None,
        iterations_to_run=None, stats_fig_1_enabled=True,
        stats_fig_2_enabled=True, stats_fig_3_enabled=True,
        stats_fig_4_enabled=True, show_dist_table=False,
    ):
        text_queue = asyncio.Queue()

        log_steps_task = asyncio.create_task(
            self.log_step(text_queue, log_steps, CPU_strategy)
        )

        await text_queue.put("Starting game component creation:")
        await self.__make_game_components(text_queue, log_steps)
        await text_queue.put("Game component creation completed")
        await text_queue.put("")
        await text_queue.put("")
        await text_queue.put("Starting game component setup")
        await self.__setup_game_components(
            text_queue, log_steps, CPU_strategy, allow_fast_forward,
            force_fast_forward, force_fast_forward_spd, iterations_to_run,
            stats_fig_1_enabled, stats_fig_2_enabled, stats_fig_3_enabled,
            stats_fig_4_enabled, show_dist_table
        )
        await text_queue.put("Game component setup completed")
        await text_queue.put("")
        await text_queue.put("")
        await text_queue.put("Starting game layout formatting")
        grid1 = await self.__format_game_layout(text_queue, log_steps)
        await text_queue.put("Game layout formatting completed")
        if (CPU_strategy != None):
            await text_queue.put("")
            await text_queue.put(
                "CPU strategy was pre-designated, making value adjustments:"
            )
            self.game_parts.divs["cpu_selected"].text = "1"
            await text_queue.put(INDENT + "Changed cpu_selected div to 1.")
            self.game_parts.divs["strategy_to_use"].text = CPU_strategy
            await text_queue.put(
                INDENT + "Changed strategy_to_use div to " + CPU_strategy + "."
            )
            if (CPU_strategy == "Goalie_Cheats"):
                self.game_parts.divs["counter_made"].text = "0"
                await text_queue.put(
                    INDENT + "As CPU strategy is set to goalie cheats, changed"
                    + "counter_made div to 0 to indicate a goalie counter is"
                    + " needed."
                )
            await text_queue.put("Finished adjustments.")
        await log_steps_task
        return grid1
    #</editor-fold>
#</editor-fold>
