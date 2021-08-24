from bokeh.models import Button, CustomJS

#<editor-fold __make_figButtonCode():
def __make_figButtonCode(index):
    """Returns a JavaScript code string for the specified figure view selection
    button. The code string for the button will make the button's corresponding
    figure visible, disable itself, hide all other figures, and enable all
    other buttons.


    Argument:
    index -- An int corresponding to the index of the button (0,1,2,3, or 4). 0
    is used for the game figure, all other indices are for their corresponding
    stats figures.


    Returns:
    string -- A string containing the javascript code for the button specified
    by index to execute on click.
    """
    vals = [
        """false;
"""
    ] * 5
    vals[index] = """true;
"""
    buttonDisableds = [
        """gameFigButton.disabled = """, """fig1Button.disabled = """,
        """fig2Button.disabled = """, """fig3Button.disabled = """,
        """fig4Button.disabled = """
    ]
    figVisibles = [
        """gameFig.visible = """, """statsFig1.visible = """,
        """statsFig2.visible = """, """statsFig3.visible = """,
        """statsFig4.visible = """
    ]

    figButtonCode = """"""
    for i in range(len(buttonDisableds)):
        figButtonCode += (buttonDisableds[i] + vals[i])
        figButtonCode += (figVisibles[i] + vals[i])

    return figButtonCode
#</editor-fold>

#<editor-fold create():
def create(game_parts, config, name):
    """Creates the figure button specified by name, then adds it to the passed
    _GameParts object being used to collect the game components under name.


    Arguments:
    game_parts -- The _GameParts object being used to collect the
      game components.
    config -- The config object being used to configure the button.
    name -- A string specifying the button the figure corresponds to.
    """
    button = Button(
        label=config.label, button_type=config.button_type,
        sizing_mode=config.sizing_mode, width_policy=config.width_policy,
        disabled=config.disabled, visible=config.visible
    )
    game_parts.buttons[name] = button
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    """Sets up the figure view selection buttons to be able to run their on
    click Javascript code.


    Argument:
    game_parts -- The _GameParts object containing the game components.
    """
    buttons = game_parts.buttons
    figs = game_parts.figures

    args_dict = {
        "gameFigButton" : buttons["game_fig"],
        "fig1Button" : buttons["fig_1"],
        "fig2Button" : buttons["fig_2"],
        "fig3Button" : buttons["fig_3"],
        "fig4Button" : buttons["fig_4"],
        "gameFig" : figs["game_figure"],
        "statsFig1" : figs["stats_1"],
        "statsFig2" : figs["stats_2"],
        "statsFig3" : figs["stats_3"],
        "statsFig4" : figs["stats_4"]
    }
    b_fig_names = ["game_fig", "fig_1", "fig_2", "fig_3", "fig_4"]
    for name in b_fig_names:
        code = __make_figButtonCode(b_fig_names.index(name))
        b_fig_click = CustomJS(args=args_dict, code=code)
        buttons[name].js_on_click(b_fig_click)
#</editor-fold>
