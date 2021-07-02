from bokeh.layouts import row, column, gridplot

#<editor-fold format():
def format(game_parts, config):

    automate_button_row = row(game_parts.buttons['automate'],
                              game_parts.sliders['iterations'],
                              game_parts.buttons['next'],
                              max_width = config.automate_button_row_max_width,
                              sizing_mode = config.automate_button_row_sizing_mode)

    strategy_dropdown_row = row(game_parts.dropdowns['cpu_strategy'],
                                max_width = config.strategy_dropdown_row_max_width,
                                sizing_mode = config.strategy_dropdown_row_sizing_mode)

    start_automate_row = row(game_parts.buttons['start'],
                             game_parts.buttons['make_counter'],
                             max_width = config.start_automate_row_max_width,
                             sizing_mode = config.start_automate_row_sizing_mode)

    automate_LL_aim_row = row(game_parts.textinputs['ll_aim'],
                              max_width = config.automate_aim_rows_max_width,
                              sizing_mode = config.automate_aim_rows_sizing_mode)
    automate_LM_aim_row = row(game_parts.textinputs['lm_aim'],
                              max_width = config.automate_aim_rows_max_width,
                              sizing_mode = config.automate_aim_rows_sizing_mode)
    automate_LR_aim_row = row(game_parts.textinputs['lr_aim'],
                              max_width = config.automate_aim_rows_max_width,
                              sizing_mode = config.automate_aim_rows_sizing_mode)
    automate_RL_aim_row = row(game_parts.textinputs['rl_aim'],
                              max_width = config.automate_aim_rows_max_width,
                              sizing_mode = config.automate_aim_rows_sizing_mode)
    automate_RM_aim_row = row(game_parts.textinputs['rm_aim'],
                              max_width = config.automate_aim_rows_max_width,
                              sizing_mode = config.automate_aim_rows_sizing_mode)
    automate_RR_aim_row = row(game_parts.textinputs['rr_aim'],
                              max_width = config.automate_aim_rows_max_width,
                              sizing_mode = config.automate_aim_rows_sizing_mode)

    game_stats_row_1 = row(game_parts.figures['stats_1'],
                           game_parts.figures['stats_2'],
                           max_width = config.game_stats_row_1_max_width,
                           sizing_mode = config.game_stats_row_1_sizing_mode)
    game_stats_row_2 = row(game_parts.figures['stats_3'],
                           game_parts.figures['stats_4'],
                           max_width = config.game_stats_row_2_max_width,
                           sizing_mode = config.game_stats_row_2_sizing_mode)

    b_fig_1_row = row(game_parts.buttons['fig_1'],
                      max_width = config.b_fig_rows_max_width,
                      sizing_mode = config.b_fig_rows_sizing_mode)
    b_fig_2_row = row(game_parts.buttons['fig_2'],
                      max_width = config.b_fig_rows_max_width,
                      sizing_mode = config.b_fig_rows_sizing_mode)
    b_fig_3_row = row(game_parts.buttons['fig_3'],
                      max_width = config.b_fig_rows_max_width,
                      sizing_mode = config.b_fig_rows_sizing_mode)
    b_fig_4_row = row(game_parts.buttons['fig_4'],
                      max_width = config.b_fig_rows_max_width,
                      sizing_mode = config.b_fig_rows_sizing_mode)

    gui_column1 = column(game_parts.figures['game_figure'], game_stats_row_1,
                         game_stats_row_2,
                         max_width = config.gui_column1_max_width,
                         sizing_mode = config.gui_column1_sizing_mode)
    gui_column2 = column(b_fig_1_row, b_fig_2_row, b_fig_3_row, b_fig_4_row,
                         automate_button_row, strategy_dropdown_row,
                         start_automate_row, automate_LL_aim_row,
                         automate_LM_aim_row, automate_LR_aim_row,
                         automate_RL_aim_row, automate_RM_aim_row,
                         automate_RR_aim_row,
                         game_parts.tables['automation'],
                         game_parts.tables['distribution'],
                         min_width = config.gui_column2_min_width,
                         max_width = config.gui_column2_max_width,
                         sizing_mode = config.gui_column2_sizing_mode)

    gui_row = row(gui_column1, gui_column2,
                  max_width = config.gui_row_max_width,
                  sizing_mode = config.gui_row_sizing_mode)

    grid1 = gridplot([[gui_row]], plot_width = config.plot_width,
                     plot_height = config.plot_height)
    return grid1
