from bokeh.layouts import row, column, gridplot

#<editor-fold format():
def format(game_parts, config):
    #These 3 items are never shown at the same time.
    automate_button_row = row(column(game_parts.buttons['automate'],
                                     game_parts.sliders['iterations'],
                                     game_parts.buttons['next'],
                                     game_parts.buttons['auto_advance']),
                              max_width = config.automate_button_row_max_width,
                              sizing_mode = config.automate_button_row_sizing_mode)

    #This row is exclusively for the strategy dropdown, and it will be hidden the
    #moment it is no longer needed. When hidden, the row should not take up any
    #space.
    strategy_dropdown_row = row(game_parts.dropdowns['cpu_strategy'],
                                max_width = config.strategy_dropdown_row_max_width,
                                sizing_mode = config.strategy_dropdown_row_sizing_mode)

    #This row is a little more complicated. Its formatted as a row that contains
    #a single column so that it contains all of its elements in a vertical order
    #while also being constrained in the same way as the other rows.
    start_automate_row = row(column(game_parts.buttons['start'],
                                    game_parts.divs['select_cpu_tip'],
                                    game_parts.divs['chances_lt_0_tip'],
                                    game_parts.divs['chances_gt_1_tip'],
                                    game_parts.divs['chances_ne_1_tip'],
                                    game_parts.buttons['make_counter']),
                             max_width = config.start_automate_row_max_width,
                             sizing_mode = config.start_automate_row_sizing_mode)

    #This section of code is to make the rows for the aim text input boxes for
    #use in a later column.
    textinputs = [game_parts.textinputs['ll_aim'],
                  game_parts.textinputs['lm_aim'],
                  game_parts.textinputs['lr_aim'],
                  game_parts.textinputs['rl_aim'],
                  game_parts.textinputs['rm_aim'],
                  game_parts.textinputs['rr_aim']]
    input_rows = []
    for i in textinputs:
        input_rows.append(row(i, max_width = config.automate_aim_rows_max_width,
                              sizing_mode = config.automate_aim_rows_sizing_mode))

    #This row is a little bit special in which at most one of its figures is
    #visible at a time. This means that even though the row contains four
    #figures, the figures are displayed in full size.
    game_stats_row = row(game_parts.figures['stats_1'],
                         game_parts.figures['stats_2'],
                         game_parts.figures['stats_3'],
                         game_parts.figures['stats_4'],
                         max_width = config.game_stats_row_max_width,
                         sizing_mode = config.game_stats_row_sizing_mode)

    #This section of code is to make the rows for the stat fig buttons for use
    #in a later column.
    b_figs = [game_parts.buttons['fig_1'],
              game_parts.buttons['fig_2'],
              game_parts.buttons['fig_3'],
              game_parts.buttons['fig_4']]
    b_fig_rows = []
    for i in b_figs:
        b_fig_rows.append(row(i, max_width = config.b_fig_rows_max_width,
                              sizing_mode = config.b_fig_rows_sizing_mode))

    #This column is for containing figures (the game figure and the stat figures).
    gui_column1 = column(game_parts.figures['game_figure'], game_stats_row,
                         max_width = config.gui_column1_max_width,
                         sizing_mode = config.gui_column1_sizing_mode)

    #This column is for containing most of the buttons, sliders, and other user
    #interactive components.
    gui_column2 = column(column(b_fig_rows),
                         automate_button_row, strategy_dropdown_row,
                         start_automate_row, column(input_rows),
                         game_parts.tables['distribution'],
                         min_width = config.gui_column2_min_width,
                         max_width = config.gui_column2_max_width,
                         sizing_mode = config.gui_column2_sizing_mode)

    #This row contains the two previous columns.
    gui_row = row(gui_column1, gui_column2,
                  max_width = config.gui_row_max_width,
                  sizing_mode = config.gui_row_sizing_mode)

    #This plots the complete figure.
    grid1 = gridplot([[gui_row]], plot_width = config.plot_width,
                     plot_height = config.plot_height)
    return grid1
#</editor-fold>
