from bokeh.models import Button, CustomJS
from . import gameloop_codestrings

#<editor-fold create():
def create(game_parts, config):
    """Creates the next button, then adds it into the passed in _GameParts
    object being used to collect the game components.


    Arguments:
    game_parts -- The _GameParts object being used to collect the
      game components.
    config -- The config object being used to configure the button.
    """
    button = Button(
        label=config.label, button_type=config.button_type,
        sizing_mode=config.sizing_mode, width_policy=config.width_policy,
        disabled=config.disabled, visible=config.visible
    )
    game_parts.buttons["next"] = button
#</editor-fold>

#<editor-fold setup():
def setup(
    game_parts, stats_fig_1_enabled, stats_fig_2_enabled, stats_fig_3_enabled,
    stats_fig_4_enabled
):
    """Sets up the next button to be able to run its on click javascript code.
    This is done by customizing the on click code to attach to the button
    according to the passed arguments.


    Arguments:
    game_parts -- The _GameParts object containing the game components.
    stats_fig_1_enabled -- A bool, whether or not the game should use
      Stats Figure 1.
    stats_fig_2_enabled -- A bool, whether or not the game should use
      Stats Figure 2.
    stats_fig_3_enabled -- A bool, whether or not the game should use
      Stats Figure 3.
    stats_fig_4_enabled -- A bool, whether or not the game should use
      Stats Figure 4.
    """
    divs = game_parts.divs
    srcs = game_parts.sources
    buttons = game_parts.buttons
    figs = game_parts.figures
    glyphs = game_parts.glyphs
    sliders = game_parts.sliders
    b_next = buttons["next"]

    args_dict = {
        "chancesSrc" : srcs["automation_table"],
        "distTableSrc" : srcs["distribution_table"],
        "stratToUseDiv" : divs["strategy_to_use"],
        "nround" : divs["nround"],
        "iterSlider" : sliders["iterations"],
        "txt" : game_parts.texts["scr_text"],
        "nextButton" : b_next,
        "gameFig" : figs["game_figure"],
        "distTable" : game_parts.tables["distribution"],
        "goalieHead" : glyphs["goalie_head"],
        "goalieBody" : glyphs["goalie_body"],
        "counterSrc" : srcs["goalie_counter"],
        "ball" : glyphs["ball"],
        "score" : divs["score"],
        "statsFig1" : figs["stats_1"],
        "statsFig2" : figs["stats_2"],
        "statsFig3" : figs["stats_3"],
        "statsFig4" : figs["stats_4"],
        "statsFig1Src" : srcs["stats_fig_1"],
        "statsFig2Src" : srcs["stats_fig_2"],
        "statsFig3Src" : srcs["stats_fig_3"],
        "statsFig4Src" : srcs["stats_fig_4"],
        "autoAdvButton" : buttons["auto_advance"],
        "inAnIter" : divs["in_an_iter"],
        "advSpdSlider" : sliders["auto_advance_speed"],
        "gameFigButton" : buttons["game_fig"],
        "statsFig1Butto" : buttons["fig_1"],
        "statsFig2Butto" : buttons["fig_2"],
        "statsFig3Butto" : buttons["fig_3"],
        "statsFig4Butto" : buttons["fig_4"]
    }

    gameCode = gameloop_codestrings.make_gameCode(
        stats_fig_1_enabled, stats_fig_2_enabled, stats_fig_3_enabled,
        stats_fig_4_enabled
    )

    b_auto_next_click = CustomJS(args=args_dict, code=gameCode)
    b_next.js_on_click(b_auto_next_click)
#</editor-fold>
