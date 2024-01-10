from bokeh.layouts import row, column, gridplot
import asyncio

# File-wide constant used for indenting consistently across logs:
INDENT = "    "

#<editor-fold Config:
class Config:
    """A class used to configure the game layout.


    Attributes:
    figs_col_min_width -- An int for setting the minimum width of the figures
      column.
    figs_col_max_width -- An int for setting the maximum width of the figures
      column.
    figs_col_sizing_mode -- A string for setting the sizing mode of the figures
      column. Must be Bokeh compatible.
    interactables_col_min_width -- An int for setting the minimum width of the
      interactables column.
    interactables_col_max_width -- An int for setting the maximum width of the
      interactables column.
    interactables_col_sizing_mode -- A string for setting the sizing mode of the
      interactables column. Must be Bokeh compatible.
    plot_width -- An int for setting the width of the full game.
    plot_height -- An int for setting the height of the full game.
    """
    def __init__(
            self, figs_col_min_width, figs_col_max_width, figs_col_sizing_mode,
            interactables_col_min_width, interactables_col_max_width,
            interactables_col_sizing_mode, plot_width, plot_height
        ):
        """Initializer for Config. Instantiates a Config object with the
        specified figs_col_min_width, figs_col_max_width,
        figs_col_sizing_mode, interactables_col_max_width,
        interactables_col_min_width, interactables_col_sizing_mode, plot_width,
        and plot_height values.


        Attributes:
        figs_col_min_width -- An int for setting self.figs_col_min_width.
        figs_col_max_width -- An int for setting self.figs_col_max_width.
        figs_col_sizing_mode -- A string for setting self.figs_col_sizing_mode.
          Must be Bokeh compatible.
        interactables_col_min_width -- An int for setting
          self.interactables_col_min_width.
        interactables_col_max_width -- An int for setting
          self.interactables_col_max_width.
        interactables_col_sizing_mode -- A string for setting
          self.interactables_col_sizing_mode. Must be Bokeh compatible.
        plot_width -- An int for setting self.plot_width.
        plot_height -- An int for setting self.plot_height.
        """
        self.figs_col_min_width = figs_col_min_width
        self.figs_col_max_width = figs_col_max_width
        self.figs_col_sizing_mode = figs_col_sizing_mode

        self.interactables_col_min_width = interactables_col_min_width
        self.interactables_col_max_width = interactables_col_max_width
        self.interactables_col_sizing_mode = interactables_col_sizing_mode

        self.plot_width = plot_width
        self.plot_height = plot_height
    #</editor-fold>

#SYNC FUNCTIONS:
#<editor-fold __create_figs_col():
def __create_figs_col(game_parts, config):
    """Asynchronous helper for the format() function. Returns a column
    containing the game figures and game distribution_table.


    Keyword Arguments:
    game_parts -- The _GameParts object that contains the game components.
    config -- The _LayoutConfig object being used to configure the game layout.
    """
    figs = game_parts.figures
    figs_col = column(
        figs["game_figure"], figs["stats_1"], figs["stats_2"], figs["stats_3"],
        figs["stats_4"], game_parts.tables['distribution'],
        min_width=config.figs_col_min_width,
        max_width=config.figs_col_max_width,
        sizing_mode=config.figs_col_sizing_mode
    )
    return figs_col
#</editor-fold>

#<editor-fold __create_interactables_col():
def __create_interactables_col(game_parts, config):
    """Asynchronous helper for the format() function. Returns a column
    containing the game's interactable components (such as buttons and sliders).


    Keyword Arguments:
    game_parts -- The _GameParts object that contains the game components.
    config -- The _LayoutConfig object being used to configure the game layout.
    """
    buttons = game_parts.buttons
    divs = game_parts.divs
    text_inputs = game_parts.textinputs

    interactables_col = column(
        buttons["automate"], game_parts.sliders["iterations"],
        game_parts.dropdowns["cpu_strategy"], divs["select_cpu_tip"],
        buttons["start"], buttons["next"], buttons["make_counter"],
        buttons["auto_advance"], game_parts.sliders["auto_advance_speed"],
        divs["chances_lt_0_tip"], divs["chances_gt_1_tip"],
        divs["chances_ne_1_tip"], text_inputs["ll_aim"], text_inputs["lm_aim"],
        text_inputs["lr_aim"], text_inputs["rl_aim"], text_inputs["rm_aim"],
        text_inputs["rr_aim"], buttons["game_fig"], buttons["fig_1"],
        buttons["fig_2"], buttons["fig_3"], buttons["fig_4"],
        min_width=config.interactables_col_min_width,
        max_width=config.interactables_col_max_width,
        sizing_mode=config.interactables_col_sizing_mode
    )
    return interactables_col
#</editor-fold>

#<editor-fold __create_grid():
def __create_grid(figs_col, interactables_col, config):
    """Asynchronous helper for the format() function. Returns a gridplot
    containing the figures and interactables column. This gridplot functions as
    the game.


    Keyword Arguments:
    figs_col -- The figures column.
    interactables_col -- The interactable components column.
    config -- The _LayoutConfig object being used to configure the game layout.
    """
    grid1 = gridplot(
        [[figs_col, interactables_col]], sizing_mode="stretch_width",
        width=config.plot_width, height=config.plot_height
    )
    return grid1
#</editor-fold>


#ASYNC FUNCTION:
#<editor-fold format():
async def format(game_parts, config, text_queue):
    """Asynchronous function used to create and return a gridplot that functions
    as the game. It does this by calling on its helper functions. As it runs, it
    also adds progress messages to text_queue.


    Keyword Argument:
    game_parts -- The _GameParts object that contains the game components.
    config -- The Config object being used to configure the game layout.
    text_queue -- The asyncio.Queue being used to collect the game creation
      progress messages.
    """
    loop = asyncio.get_event_loop()
    figs_col = await loop.run_in_executor(
        None, __create_figs_col, game_parts, config
    )
    await text_queue.put(INDENT + "Figures layout column creation completed.")
    interactables_col = await loop.run_in_executor(
        None, __create_interactables_col, game_parts, config
    )
    await text_queue.put(
        INDENT + "Interactables layout column creation completed."
    )
    #This generates the complete game figure:
    grid1 = await loop.run_in_executor(
        None, __create_grid, figs_col, interactables_col, config
    )
    await text_queue.put(INDENT + "Game gridplot creation completed.")
    return grid1
#</editor-fold>
