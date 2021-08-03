from bokeh.models import Button, CustomJS

#<editor-fold __make_figButtonCode():
def __make_figButtonCode(index):
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
    button = Button(
        label=config.label, button_type=config.button_type,
        sizing_mode=config.sizing_mode, width_policy=config.width_policy,
        disabled=config.disabled, visible=config.visible
    )
    game_parts.buttons[name] = button
#</editor-fold>

#<editor-fold setup():
def setup(game_parts, name):
    buttons = game_parts.buttons
    figs = game_parts.figures
    args_dict = dict(
        gameFigButton = buttons["game_fig"],
        fig1Button = buttons["fig_1"],
        fig2Button = buttons["fig_2"],
        fig3Button = buttons["fig_3"],
        fig4Button = buttons["fig_4"],
        gameFig = figs["game_figure"],
        statsFig1 = figs["stats_1"],
        statsFig2 = figs["stats_2"],
        statsFig3 = figs["stats_3"],
        statsFig4 = figs["stats_4"]
    )
    index = ["game_fig", "fig_1", "fig_2", "fig_3", "fig_4"].index(name)
    code = __make_figButtonCode(index)
    b_fig_click = CustomJS(args=args_dict, code=code)
    buttons[name].js_on_click(b_fig_click)
#</editor-fold>
