from . import gamecomponents as components
from . import game_layout
from . import gamefigures as figs
import asyncio

# File-wide constant used for indenting consistently across logs:
INDENT = "    "
# File-wide constant used for iterating through figure button names:
B_FIG_NAMES = ["game_fig", "fig_1", "fig_2", "fig_3", "fig_4"]

#<editor-fold _GameParts:
class _GameParts:
    """A class used to store the game components during the game creation
    process.


    Attributes:
    buttons -- A dict containing the game buttons.
    divs -- A dict containing the game divs.
    dropdowns -- A dict containing the game dropdowns.
    lables -- A dict containing the game labels.
    sliders -- A dict containing the game sliders.
    tables -- A dict containing the game tables.
    sources -- A dict containing the game sources.
    texts -- A dict containing the game texts.
    textinputs -- A dict containing the game textInputs.
    figures -- A dict containing the game figures.
    glyphs -- A dict containing the game glyphs.
    """

    def __init__(self):
        """Initializer for _GameParts. Instantiates a _GameParts object with
        empty game component storing dicts.
        """
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
    #<editor-fold _TextConfig:
class _TextConfig:
    """A class used for configuring the game texts.


    Attributes:
    xs -- A list of x coords to use for the locations of the lines of text.
    ys -- A list of y coords to use for the locations of the lines of text.
    text_lines -- A list of strings to use as the text for the lines of text.
    """

    def __init__(self, xs, ys, text_lines):
        """Initializer for _TextConfig. Instantiates a _TextConfig object with
        the specified xs, ys, and text_lines lists.


        Keyword Arguments:
        xs -- the list of ints to set self.xs to.
        ys -- the list of ints to set self.ys to.
        text_lines -- the list of strings to set self.text_lines to.
        """
        self.xs = xs
        self.ys = ys
        self.text_lines = text_lines
    #</editor-fold>
    #<editor-fold _LabelsConfig:
class _LabelsConfig:
    """A class used for configuring the game labels.


    Attributes:
    text_color -- A string representing the text color. Must be Bokeh compatible.
    text_font_size -- A string representing the text font size. Must be Bokeh
      compatible.
    text_x_offset -- An int to use as the x offset for the text.
    text_y_offset -- An int to use as the y offset for the text.
    text_baseline -- A string to use to indicate the text baseline. Must be
      Bokeh compatible.
    text_align -- A string to use to indicate the text align style. Must be
      Bokeh compatible.
    """
    def __init__(
            self, text_color, text_font_size, text_x_offset, text_y_offset,
            text_baseline, text_align
        ):
        """Initializer for _LabelsConfig. Instantiates a _LabelsConfig object
        with the specified text_color, text_font_size, text_x_offset,
        text_y_offset, text_baseline, text_align.


        Keyword Arguments:
        text_color -- A string used to set self.text_color. Must be Bokeh
          compatible.
        text_font_size -- A string used to set self.text_font_size. Must be
          Bokeh compatible.
        text_x_offset -- An int to used to set self.text_x_offset.
        text_y_offset -- An int to used to set self.text_y_offset.
        text_baseline -- A string to use to set self.text_baseline. Must be
          Bokeh compatible.
        text_align -- A string to use to set self.text_align. Must be Bokeh
          compatible.
        """
        self.text_color = text_color
        self.text_font_size = text_font_size
        self.text_x_offset = text_x_offset
        self.text_y_offset = text_y_offset
        self.text_baseline = text_baseline
        self.text_align = text_align
    #</editor-fold>
    #<editor-fold _ButtonConfig:
class _ButtonConfig:
    """A class used for configuring game buttons.


    Attributes:
    label -- A string containing the text for the button's label.
    button_type -- A string to use for setting the button type. Must be Bokeh
      compatible.
    sizing_mode -- A string to use for setting the button sizing mode. Must be
      Bokeh compatible.
    width_policy -- A string to use for setting the button width policy. Must be
      Bokeh compatible.
    disabled -- A bool to use for whether or not the button should be disabled.
    visible -- A bool to use for whether or not the button should be visible.
    """
    def __init__(
            self, label, button_type, sizing_mode, width_policy, disabled,
            visible
        ):
        """Initializer for _ButtonConfig. Instantiates a _ButtonConfig object
        with the specified label, button_type, sizing_mode, width_policy,
        disabled, and visible values.


        Keyword Arguments:
        label -- A string used to set self.label. Must be Bokeh compatible.
        button_type -- A string used to set self.button_type. Must be Bokeh
          compatible.
        sizing_mode -- A string used to set self.sizing_mode. Must be Bokeh
          compatible.
        width_policy -- An string used to set self.width_policy. Must be Bokeh
          compatible.
        disabled -- A bool used to set self.disabled.
        visible -- A bool used to set self.visible.
        """
        self.label = label
        self.button_type = button_type
        self.sizing_mode = sizing_mode
        self.width_policy = width_policy
        self.disabled = disabled
        self.visible = visible
    #</editor-fold>
    #<editor-fold _DivConfig:
class _DivConfig:
    """A class used for configuring game divs.


    Attributes:
    text -- A string to use for setting the div text.
    visible -- A bool to use for setting whether the div should be visible.
    """
    def __init__(self, text, visible):
        """Initializer for _DivConfig. Instantiates a _DivConfig object with the
        specified text and visible values.


        Keyword Arguments:
        text -- A string used to set self.text.
        visible -- A bool used to set self.visible
        """
        self.text = text
        self.visible = visible
    #</editor-fold>
    #<editor-fold _SliderConfig:
class _SliderConfig:
    """A class used for configuring sliders.


    Attributes:
    start -- An int or float for setting the minimum slider value.
    end -- An int or float for setting the maximum slider value.
    value -- An int or float for setting the initial slider value.
    step -- An int or float for setting the slider value increments.
    title -- A string for setting the slider title.
    disabled -- A bool for setting whether the slider should be disabled.
    visible -- A bool for setting whether the slider should be visible.
    """
    def __init__(self, start, end, value, step, title, disabled, visible):
        """Initializer for _SliderConfig. Instantiates a _SliderConfig object
        with the specified start, end, value, step, title, disabled and visible
        values.


        Keyword Arguments:
        start -- An int or float to set self.start to.
        end -- An int or float to set self.end to.
        value -- An int or float to set self.value to.
        step -- An int or float to set self.step to.
        title -- A string to set self.title to.
        disabled -- A bool for setting self.disabled to.
        visible -- A bool for setting self.visible to.
        """
        self.start = start
        self.end = end
        self.value = value
        self.step = step
        self.title = title
        self.disabled = disabled
        self.visible = visible
    #</editor-fold>
    #<editor-fold _TextInputConfig:
class _TextInputConfig:
    """A class used for configuring text inputs.


    Attributes:
    value -- A string to set the initial text input value to.
    visible -- A bool for setting whether the text input should be visible.
    """
    def __init__(self, value, visible):
        """Initializer for _TextInputConfig. Instantiates a _TextInputConfig
        object with the specified value and visible values.


        Keyword Arguments:
        value -- A string to set self.value to.
        visible -- A bool to set self.visible to.
        """
        self.value = value
        self.visible = visible
    #</editor-fold>
    #<editor-fold _DropdownConfig:
class _DropdownConfig:
    """A class used for configuring dropdowns.


    Attributes:
    items -- A list of (string, string) pairs to use for setting the dropdown's
      items.
    label -- A string to use for setting the dropdown's label.
    button_type -- A string for setting the dropdown's button type. Must be
      Bokeh compatible.
    disabled -- A bool for setting whether the dropdown should be disabled.
    visible -- A bool for setting whether the dropdown should be visible.
    """
    def __init__(self, items, label, button_type, disabled, visible):
        """Initializer for _DropdownConfig. Instantiates a _DropdownConfig
        object with the specified items, label, button_type, disabled, and
        visible values.


        Keyword Arguments:
        items -- A list of strings to use as the selectable items. Both the item
          name and values will be set to the values in the list. self.items will
          be set to a list containing those items.
        label -- A string to use for setting self.label.
        button_type -- A string to use for setting self.button_type. Must be
          Bokeh compatible.
        disabled -- A bool for setting self.disabled.
        visible -- A bool for setting self.visible.
        """
        new_items = []
        for item in items:
            new_items.append((item, item))
        self.items = new_items
        self.label = label
        self.button_type = button_type
        self.disabled = disabled
        self.visible = visible
    #</editor-fold>
    #<editor-fold _TableFootednessConfig:
class _TableFootednessConfig:
    """A class used for configuring the strings used by game tables for
    footedness and aim direction texts.


    Attributes:
    footedness_left_text -- A string used to represent left footed kicker's
      footedness direction.
    footedness_right_text -- A string used to represent right footed kicker's
      footedness direction.
    aim_direction_left_text -- A string used to represent left aimed shot's
      aim direction.
    aim_direction_middle_text -- A string used to represent middle aimed shot's
      aim direction.
    aim_direction_right_text -- A string used to represent right aimed shot's
      aim direction.
    """
    def __init__(
            self, footedness_left_text, footedness_right_text,
            aim_direction_left_text, aim_direction_middle_text,
            aim_direction_right_text
        ):
        """Initializer for _TableFootednessConfig. Instantiates a
        _TableFootednessConfig object with the specified footedness_left_text,
        footedness_right_text, aim_direction_left_text,
        aim_direction_middle_text, and aim_direction_right_text.


        Keyword Arguments:
        footedness_left_text -- A string used to set self.footedness_left_text.
        footedness_right_text -- A string used to set self.footedness_right_text.
        aim_direction_left_text -- A string used to set
          self.aim_direction_left_text.
        aim_direction_middle_text -- A string used to set
          self.aim_direction_middle_text.
        aim_direction_right_text -- A string used to set
          self.aim_direction_right_text.
        """
        self.footedness_left_text = footedness_left_text
        self.footedness_right_text = footedness_right_text
        self.aim_direction_left_text = aim_direction_left_text
        self.aim_direction_middle_text = aim_direction_middle_text
        self.aim_direction_right_text = aim_direction_right_text
    #</editor-fold>
    #<editor-fold _DistTableConfig:
class _DistTableConfig:
    """A class used to configure the game distribution_table.


    Attributes:
    titles -- A list of strings used to set the table column titles.
    width -- An int to use as the table width.
    height -- An int to use as the table height.
    autosize_mode -- A string used to set the table autosizing mode. Must be
      Bokeh compatible.
    sizing_mode -- A string used to set the table sizing mode. Must be Bokeh
      compatible.
    visible -- A string used to set whether the table should be visible.
    fit_columns -- A bool used to set whether or not to fit the columns.
    column_widths -- A list of ints to set the column widths to.
    """
    def __init__(
            self, titles, width, height, autosize_mode, sizing_mode, visible,
            fit_columns, column_widths
        ):
        """Initializer for _DistTableConfig. Instantiates a _DistTableConfig
        object with the specified titles, width, height, autosize_mode,
        sizing_mode, visible, fit_columns, and column_widths values.


        Keyword Arguments:
        titles -- A list of strings used to set self.titles.
        width -- An int used to set self.width.
        height -- An int used to set self.height.
        autosize_mode -- A string used to set self.autosize_mode. Must be Bokeh
          compatible.
        sizing_mode -- A string used to set self.sizing_mode. Must be Bokeh
          compatible.
        visible -- A string used to set self.visible.
        fit_columns -- A bool used to set self.fit_columns.
        column_widths -- A list of ints to set self.column_widths.
        """
        self.titles = titles
        self.width = width
        self.height = height
        self.autosize_mode = autosize_mode
        self.sizing_mode = sizing_mode
        self.visible = visible
        self.fit_columns = fit_columns
        self.column_widths = column_widths
    #</editor-fold>
    #<editor-fold _AutoTableConfig:
class _AutoTableConfig:
    """A class used to configure the game automation_table.


    Attributes:
    titles -- A list of strings used to set the table column titles.
    width -- An int to use as the table width.
    height -- An int to use as the table height.
    autosize_mode -- A string used to set the table autosizing mode. Must be
      Bokeh compatible.
    visible -- A string used to set whether the table should be visible.
    """
    def __init__(self, titles, width, height, autosize_mode, visible):
        """Initializer for _AutoTableConfig. Instantiates a _AutoTableConfig
        object with the specified titles, width, height, autosize_mode and
        visible values.


        Keyword Arguments:
        titles -- A list of strings used to set self.titles.
        width -- An int used to set self.width.
        height -- An int used to set self.height.
        autosize_mode -- A string used to set self.autosize_mode. Must be Bokeh
          compatible.
        visible -- A string used to set self.visible.
        """
        self.titles = titles
        self.width = width
        self.height = height
        self.autosize_mode = autosize_mode
        self.visible = visible
    #</editor-fold>
#</editor-fold>

#<editor-fold MainGame:
class MainGame:
    """A class containing the game's components and configuration objects.
    Through use of the method make_game(), it is possible to make configured
    versions of the demo.


    Attributes:
    game_parts -- The _GameParts object being used to organize the game's
      components.
    stats_fig_1 -- The figs.stats_fig_1.Configs object being used to configure
      Stats Figure 1.
    stats_fig_2 -- The figs.stats_fig_2.Configs object being used to configure
      Stats Figure 2.
    stats_fig_3 -- The figs.stats_fig_3.Configs object being used to configure
      Stats Figure 3.
    stats_fig_4 -- The figs.stats_fig_4.Configs object being used to configure
      Stats Figure 4.
    game_fig -- The figs.game_fig.Configs object being used to configure the
      main game figure.
    b_automate -- The _ButtonConfig object being used to configure the automate
      button.
    b_start_automate -- The _ButtonConfig object being used to configure the
      start button.
    b_auto_next -- The _ButtonConfig object being used to configure the next
      button.
    b_make_counter -- The _ButtonConfig object being used to configure the make
      counter button.
    b_auto_advance -- The _ButtonConfig object being used to configure the auto
      advance toggle button.
    b_fig_configs -- The list of _ButtonConfig objects being used to configure
      the figure view selection buttons.
    scr_text -- The _TextConfig object being used to configure the game's
      scr_text.
    scr_labels -- The _LabelsConfig object being used to configure the game's
      scr_labels.
    select_cpu_tip -- The _DivConfig object being used to configure the game's
      div for a tip that selecting a cpu strategy is required.
    chances_gt_1_tip -- The _DivConfig object being used to configure the game's
      div for a tip that all pure strategy chances must be set to a value less
      than 1.
    chances_lt_0_tip -- The _DivConfig object being used to configure the game's
      div for a tip that all pure strategy chances must be set to a value
      greater than 0.
    chances_ne_1_tip -- The _DivConfig object being used to configure the game's
      div for a tip that all pure strategy chances must add up to 1.
    iterations_slider -- The _SliderConfig object being used to configure the
      game's slider for selecting the number of iterations to run.
    auto_advance_speed_slider -- The _SliderConfig object being used to
      configure the game's slider for selecting the speed at which to
      automatically advance between iterations when auto advancing is enabled.
    aim_text_inputs -- The _TextInputConfig object being used to configure the
      game's text inputs for selecting each pure strategy's execution
      chance.
    cpu_strategy_dropdown -- The _DropdownConfig being used to configure the
      game's dropdown for selecting the keeper's strategy.
    footedness_config -- The _TableFootednessConfig being used to configure some
      of the direction texts for the game's tables.
    distribution_table -- The _DistTableConfig being used to configure the
      game's distribution table.
    automation_table -- The _AutoTableConfig being used to configure the game's
      automation table.
    layout -- The _LayoutConfig being used to configure the game's layout.


    Methods:
    make_game -- An asynchronous method used to create an actual version of the
      game from the object's attributes. Calling make game will create and
      prepare all game components before adding them to the game layout and
      returning a copy of the completed game. The game will be put together
      according to the object's attributes, and the passed arguments.
    """
    #SYNC FUNCTION:
    #<editor-fold __init__():
    def __init__(self):
        """Initializer for MainGame. Creates a MainGame object with all of its
        attributes instantiated with default values. Configuration of this
        class' attributes is not done through its Initializer, so it has no
        arguments.
        """
        self.game_parts = _GameParts()
        #<editor-fold Fig Configs:
        self.stats_fig_1 = figs.stats_fig_1.Configs()
        self.stats_fig_2 = figs.stats_fig_2.Configs()
        self.stats_fig_3 = figs.stats_fig_3.Configs()
        self.stats_fig_4 = figs.stats_fig_4.Configs()
        self.game_fig = figs.game_fig.Configs()
        #</editor-fold>
        #<editor-fold Button Configs:
        self.b_automate = _ButtonConfig(
            label="Automate", button_type="success", sizing_mode="scale_width",
            width_policy="fit", disabled=False, visible=True
        )
        self.b_start_automate = _ButtonConfig(
            label="Start", button_type="success", sizing_mode="scale_width",
            width_policy="fit", disabled=False, visible=False
        )
        self.b_auto_next = _ButtonConfig(
            label="Next", button_type="success", sizing_mode="scale_width",
            width_policy="fit", disabled=False, visible=False
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
        self.aim_text_inputs = _TextInputConfig(value="0", visible=False)
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
        self.layout = game_layout.Config(
            figs_col_min_width=600, figs_col_max_width=600,
            figs_col_sizing_mode="stretch_width",
            interactables_col_min_width=350, interactables_col_max_width=350,
            interactables_col_sizing_mode="stretch_width", plot_width=950,
            plot_height=480
        )
        #</editor-fold>
    #</editor-fold>

    #ASYNC FUNCTIONS:
    #<editor-fold __make_game_components():
    async def __make_game_components(self, text_queue):
        """Asynchronous helper used by the make_game() method to make all of the
        game components by passing the necessary arguments to all of the
        component creation functions while continuously passing in
        self.game_parts to collect the created components. Following successful
        component creations, progress messages are added to text_queue so that.


        Keyword Argument:
        text_queue -- An asyncio.Queue object being used to add progress message
          strings to.
        """
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
            None, components.divs.start_checks.create, self.game_parts
        )
        await text_queue.put(
            INDENT + INDENT + "Game start condition enforcing divs created."
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
        ids = ["ll", "lm", "lr", "rl", "rm", "rr"]
        for id in ids:
            await loop.run_in_executor(
                None, components.textinputs.aim_text_input.create,
                self.game_parts, id, self.aim_text_inputs
            )
            await text_queue.put(
                INDENT + INDENT + id + "_aim text input created"
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
            self.game_parts, self.footedness_config
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
            self.game_parts, self.footedness_config
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

        #Function End.
    #</editor-fold>

    #<editor-fold __setup_game_components():
    async def __setup_game_components(
        self, text_queue, CPU_strategy, allow_fast_forward, force_fast_forward,
        force_fast_forward_spd, iterations_to_run, stats_fig_1_enabled,
        stats_fig_2_enabled, stats_fig_3_enabled, stats_fig_4_enabled,
        show_dist_table
    ):
        """Asynchronous helper used by the make_game() method to set up all of
        the game components. It does this by calling setup functions on the game
        components from self.game_parts and passing in the necessary parameters
        for configuring their behaviour.


        Keyword Arguments:
        text_queue -- An asyncio.Queue object being used to add progress message
          strings to.
        CPU_strategy -- A string used to set the keeper's strategy in advance.
          Doing so prevents cpu_strategy_dropdown from being shown, in order to
          prevent the player from changing their strategy. CPU_strategy must be
          set to 'Fictitious_Play', 'Mixed_Strategy', 'Random', 'Goalie_Cheats',
          or None.
        allow_fast_forward -- A bool used to set whether or not the auto advance
          feature can be enabled. Setting this to False will prevent
          b_auto_advance from being shown to the player, so that they cannot
          toggle auto advancing.
        force_fast_forward -- A bool used to set whether or not the auto advance
          feature should be forced. If allow_fast_forward is set to True, then
          setting this to True will toggle b_auto_advance to be active before
          preventing it from being shown, so that auto advancing is activated
          without the player being able to turn it off.
        force_fast_forward_spd -- An int representing the delay to use (in
          miliseconds) in between iterations. force_fast_forward_spd can be any
          int greater than 0, or None. Setting a value for this will change the
          value of the auto_advance_speed_slider accordingly, and prevent it
          from being shown in order to stop the player from being able to
          change it.
        iterations_to_run -- None, or an int greater than 0. If set to an int,
          the value of the iterations_to_run slider will be set accordingly, and
          it will be prevented from being shown to the player in order to stop
          them from changing its value.
        stats_fig_1_enabled -- A bool used to set whether or not to include
          Stats Figure 1. If False, Stats Figure 1 and its view selection button
          will both be prevented from being shown or updated.
        stats_fig_2_enabled -- A bool used to set whether or not to include
          Stats Figure 2. If False, Stats Figure 2 and its view selection button
          will both be prevented from being shown or updated.
        stats_fig_3_enabled -- A bool used to set whether or not to include
          Stats Figure 3. If False, Stats Figure 3 and its view selection button
          will both be prevented from being shown or updated.
        stats_fig_4_enabled -- A bool used to set whether or not to include
          Stats Figure 4. If False, Stats Figure 4 and its view selection button
          will both be prevented from being shown or updated.
        show_dist_table -- A bool used to set whether or not to show the
          distribution_table to the player. This should only be turned on for
          the purpose of asserting that the demo is running correctly.
        """
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
            None, components.divs.start_checks.setup, self.game_parts
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
        await loop.run_in_executor(
            None, components.buttons.b_figs.setup, self.game_parts
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
        await loop.run_in_executor(
            None, components.textinputs.aim_text_input.setup, self.game_parts
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
        """Asynchronous helper for the make_game() method. This will format the
        game by passing all of its game parts and necessary arguments to
        game_layout.format(). It will then return the game.


        Keyword Argument:
        text_queue -- An asyncio.Queue object being used to add progress message
          strings to.
        """
        grid1 = await game_layout.format(
            self.game_parts, self.layout, text_queue
        )
        return grid1
    #</editor-fold>

    #<editor-fold __log_step():
    async def __log_step(self, text_queue, log_steps):
        """Asynchronous helper for the make_game() method. This will process the
        text_queue, printing the items within the queue if log_steps is True.


        Keyword Arguments:
        text_queue -- An asyncio.Queue object being used to add progress message
          strings to. __log_step processes the progress message strings added to
          the queue.
        log_steps -- A bool used to set whether or not to print the progress
          messages added to the queue.
        """
        keep_running = log_steps
        while keep_running:
            val = await text_queue.get()
            if (val == "Finished making game"):
                keep_running = False
            print(val)
    #</editor-fold>

    #<editor-fold make_game():
    async def make_game(
        self, log_steps=False, CPU_strategy=None, allow_fast_forward=True,
        force_fast_forward=False, force_fast_forward_spd=None,
        iterations_to_run=None, stats_fig_1_enabled=True,
        stats_fig_2_enabled=True, stats_fig_3_enabled=True,
        stats_fig_4_enabled=True, show_dist_table=False,
    ):
        """Asynchronous method used to make the demo from the object's
        attributes and the input arguments. Running this method will return a
        full version of the penalty_kick_game, configured according to the
        previously mentioned values. It does this by calling on its helpers.


        Keyword Arguments:
        log_steps -- A bool, whether or not to print progress messages.
        CPU_strategy -- A string used to set the keeper's strategy in advance.
          Doing so prevents cpu_strategy_dropdown from being shown, in order to
          prevent the player from changing their strategy. CPU_strategy must be
          set to 'Fictitious_Play', 'Mixed_Strategy', 'Random', 'Goalie_Cheats',
          or None.
        allow_fast_forward -- A bool used to set whether or not the auto advance
          feature can be enabled. Setting this to False will prevent
          b_auto_advance from being shown to the player, so that they cannot
          toggle auto advancing.
        force_fast_forward -- A bool used to set whether or not the auto advance
          feature should be forced. If allow_fast_forward is set to True, then
          setting this to True will toggle b_auto_advance to be active before
          preventing it from being shown, so that auto advancing is activated
          without the player being able to turn it off.
        force_fast_forward_spd -- An int representing the delay to use (in
          miliseconds) in between iterations. force_fast_forward_spd can be any
          int greater than 0, or None. Setting a value for this will change the
          value of the auto_advance_speed_slider accordingly, and prevent it
          from being shown in order to stop the player from being able to
          change it.
        iterations_to_run -- None, or an int greater than 0. If set to an int,
          the value of the iterations_to_run slider will be set accordingly, and
          it will be prevented from being shown to the player in order to stop
          them from changing its value.
        stats_fig_1_enabled -- A bool used to set whether or not to include
          Stats Figure 1. If False, Stats Figure 1 and its view selection button
          will both be prevented from being shown or updated.
        stats_fig_2_enabled -- A bool used to set whether or not to include
          Stats Figure 2. If False, Stats Figure 2 and its view selection button
          will both be prevented from being shown or updated.
        stats_fig_3_enabled -- A bool used to set whether or not to include
          Stats Figure 3. If False, Stats Figure 3 and its view selection button
          will both be prevented from being shown or updated.
        stats_fig_4_enabled -- A bool used to set whether or not to include
          Stats Figure 4. If False, Stats Figure 4 and its view selection button
          will both be prevented from being shown or updated.
        show_dist_table -- A bool used to set whether or not to show the
          distribution_table to the player. This should only be turned on for
          the purpose of asserting that the demo is running correctly.
        """
        text_queue = asyncio.Queue()

        log_steps_task = asyncio.create_task(
            self.__log_step(text_queue, log_steps)
        )

        await text_queue.put("Starting game component creation:")
        await self.__make_game_components(text_queue)
        await text_queue.put("Game component creation completed")
        await text_queue.put("")
        await text_queue.put("")
        await text_queue.put("Starting game component setup")
        await self.__setup_game_components(
            text_queue, CPU_strategy, allow_fast_forward, force_fast_forward,
            force_fast_forward_spd, iterations_to_run, stats_fig_1_enabled,
            stats_fig_2_enabled, stats_fig_3_enabled, stats_fig_4_enabled,
            show_dist_table
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
                    + " counter_made div to 0 to indicate a goalie counter is"
                    + " needed."
                )
            await text_queue.put("Finished adjustments.")
            await text_queue.put("")

        await text_queue.put("Finished making game")
        await log_steps_task
        return grid1
    #</editor-fold>
#</editor-fold>
