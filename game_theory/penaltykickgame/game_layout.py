from bokeh.layouts import row, column, gridplot

INDENT = "    "

#<editor-fold format():
def format(game_parts, config, log_steps = False):
    dist_table_row = row(
        game_parts.tables['distribution'],
        min_width = config.figs_col_min_width,
        max_width = config.figs_col_max_width,
        sizing_mode = config.figs_col_sizing_mode
    )

    if (log_steps):
        print(INDENT + "Distribution table layout row creation completed.")

    # Order does not really matter for most parameters below. Only requirement
    # is that dist_table_row is located after game_figure.
    figures_column = column(
        game_parts.figures['game_figure'], game_parts.figures['stats_1'],
        game_parts.figures['stats_2'], game_parts.figures['stats_3'],
        game_parts.figures['stats_4'], dist_table_row,
        min_width = config.figs_col_min_width,
        max_width = config.figs_col_max_width,
        sizing_mode = config.figs_col_sizing_mode
    )

    if (log_steps):
        print(INDENT + "Figures layout column creation completed.")

    # Order matters for the parameters below. The order of the game game parts
    # below is the vertical order that they will appear in the column.
    # As such, the vertical order matters between parts that are capable of
    # being seen at the same time.
    interactables_column = column(
        game_parts.buttons['automate'], game_parts.sliders['iterations'],
        game_parts.dropdowns['cpu_strategy'], game_parts.divs['select_cpu_tip'],
        game_parts.buttons['start'], game_parts.buttons['next'],
        game_parts.buttons['make_counter'], game_parts.buttons['auto_advance'],
        game_parts.sliders['auto_advance_speed'],
        game_parts.divs['chances_lt_0_tip'],
        game_parts.divs['chances_gt_1_tip'],
        game_parts.divs['chances_ne_1_tip'], game_parts.textinputs['ll_aim'],
        game_parts.textinputs['lm_aim'], game_parts.textinputs['lr_aim'],
        game_parts.textinputs['rl_aim'], game_parts.textinputs['rm_aim'],
        game_parts.textinputs['rr_aim'], game_parts.buttons['game_fig'],
        game_parts.buttons['fig_1'], game_parts.buttons['fig_2'],
        game_parts.buttons['fig_3'], game_parts.buttons['fig_4'],
        min_width = config.interactables_col_min_width,
        max_width = config.interactables_col_max_width,
        sizing_mode = config.interactables_col_sizing_mode
    )

    if (log_steps):
        print(INDENT + "Interactables layout column creation completed.")

    #This plots the complete figure.
    grid1 = gridplot(
        [[figures_column, interactables_column]], sizing_mode = 'stretch_width',
        plot_width = config.plot_width, plot_height = config.plot_height
    )

    if (log_steps):
        print(INDENT + "Game gridplot creation completed.")

    return grid1
#</editor-fold>
