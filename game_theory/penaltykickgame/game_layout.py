from bokeh.layouts import row, column, gridplot

INDENT = "    "

#<editor-fold format():
def format(game_parts, config, log_steps=False):
    divs = game_parts.divs
    text_inputs = game_parts.textinputs
    figs = game_parts.figures
    buttons = game_parts.buttons

    # Order does not really matter for most parameters below. Only requirement
    # is that the dist table is located after the game fig.
    figs_col = column(
        figs["game_figure"], figs["stats_1"], figs["stats_2"], figs["stats_3"],
        figs["stats_4"], game_parts.tables['distribution'],
        min_width=config.figs_col_min_width,
        max_width=config.figs_col_max_width,
        sizing_mode=config.figs_col_sizing_mode
    )

    if (log_steps):
        print(INDENT + "Figures layout column creation completed.")

    # Order matters for the parameters below. The order of the game game parts
    # below is the vertical order that they will appear in the column.
    # As such, the vertical order matters between parts that are capable of
    # being seen at the same time.
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

    if (log_steps):
        print(INDENT + "Interactables layout column creation completed.")

    #This plots the complete figure.
    grid1 = gridplot(
        [[figs_col, interactables_col]], sizing_mode="stretch_width",
        plot_width=config.plot_width, plot_height=config.plot_height
    )

    if (log_steps):
        print(INDENT + "Game gridplot creation completed.")

    return grid1
#</editor-fold>
