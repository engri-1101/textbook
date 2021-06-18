from bokeh.models import (Button, Slider, Dropdown)
from bokeh.models.widgets import Div

#<editor-fold create_buttons():
def create_buttons(b_automate_label = "Automate",
                   b_automate_button_type = "success",
                   b_automate_sizing_mode = "scale_width",
                   b_automate_width_policy = "fit",
                   b_automate_disabled = False,
                   b_automate_visibility = True,
                   b_start_automate_label = "Start",
                   b_start_automate_button_type = "success",
                   b_start_automate_sizing_mode = "scale_width",
                   b_start_automate_width_policy = "fit",
                   b_start_automate_disabled = False,
                   b_start_automate_visibility = False,
                   b_auto_next_label = "Next",
                   b_auto_next_button_type = "success",
                   b_auto_next_sizing_mode = "scale_width",
                   b_auto_next_width_policy = "fit",
                   b_auto_next_disabled = False,
                   b_auto_next_visibility = False):

    b_automate = Button(label = b_automate_label,
                        button_type = b_automate_button_type,
                        sizing_mode = b_automate_sizing_mode,
                        width_policy = b_automate_width_policy,
                        disabled = b_automate_disabled,
                        visible = b_automate_visibility)

    b_start_automate = Button(label = b_start_automate_label,
                              button_type = b_start_automate_button_type,
                              sizing_mode = b_start_automate_sizing_mode,
                              width_policy = b_start_automate_width_policy,
                              disabled = b_start_automate_disabled,
                              visible = b_start_automate_visibility)

    b_auto_next = Button(label = b_auto_next_label,
                         button_type = b_auto_next_button_type,
                         sizing_mode = b_auto_next_sizing_mode,
                         width_policy = b_auto_next_width_policy,
                         disabled = b_auto_next_disabled,
                         visible = b_auto_next_visibility)

    return b_automate, b_start_automate, b_auto_next
#</editor-fold>
#<editor-fold create_sliders():
def create_sliders(ll_aim_slider_start = 0, ll_aim_slider_end = 1,
                   ll_aim_slider_value = 1/6, ll_aim_slider_step = 0.01,
                   ll_aim_slider_title = "LL Aim Weight",
                   ll_aim_slider_disabled = False,
                   ll_aim_slider_visibility = False,
                   lm_aim_slider_start = 0, lm_aim_slider_end = 1,
                   lm_aim_slider_value = 1/6, lm_aim_slider_step = 0.01,
                   lm_aim_slider_title = "LM Aim Weight",
                   lm_aim_slider_disabled = False,
                   lm_aim_slider_visibility = False,
                   lr_aim_slider_start = 0, lr_aim_slider_end = 1,
                   lr_aim_slider_value = 1/6, lr_aim_slider_step = 0.01,
                   lr_aim_slider_title = "LR Aim Weight",
                   lr_aim_slider_disabled = False,
                   lr_aim_slider_visibility = False,
                   rl_aim_slider_start = 0, rl_aim_slider_end = 1,
                   rl_aim_slider_value = 1/6, rl_aim_slider_step = 0.01,
                   rl_aim_slider_title = "RL Aim Weight",
                   rl_aim_slider_disabled = False,
                   rl_aim_slider_visibility = False,
                   rm_aim_slider_start = 0, rm_aim_slider_end = 1,
                   rm_aim_slider_value = 1/6, rm_aim_slider_step = 0.01,
                   rm_aim_slider_title = "RM Aim Weight",
                   rm_aim_slider_disabled = False,
                   rm_aim_slider_visibility = False,
                   rr_aim_slider_start = 0, rr_aim_slider_end = 1,
                   rr_aim_slider_value = 1/6, rr_aim_slider_step = 0.01,
                   rr_aim_slider_title = "RR Aim Weight",
                   rr_aim_slider_disabled = False,
                   rr_aim_slider_visibility = False,
                   iterations_slider_start = 10, iterations_slider_end = 500,
                   iterations_slider_value = 50,
                   iterations_slider_title = "Iterations To Run",
                   iterations_slider_disabled = False,
                   iterations_slider_visibility = False):

    ll_aim_slider = Slider(start = ll_aim_slider_start,
                           end = ll_aim_slider_end,
                           value = ll_aim_slider_value,
                           step = ll_aim_slider_step,
                           title = ll_aim_slider_title,
                           disabled = ll_aim_slider_disabled,
                           visible = ll_aim_slider_visibility)
    lm_aim_slider = Slider(start = lm_aim_slider_start,
                           end = lm_aim_slider_end,
                           value = lm_aim_slider_value,
                           step = lm_aim_slider_step,
                           title = lm_aim_slider_title,
                           disabled = lm_aim_slider_disabled,
                           visible = lm_aim_slider_visibility)
    lr_aim_slider = Slider(start = lr_aim_slider_start,
                           end = lr_aim_slider_end,
                           value = lr_aim_slider_value,
                           step = lr_aim_slider_step,
                           title = lr_aim_slider_title,
                           disabled = lr_aim_slider_disabled,
                           visible = lr_aim_slider_visibility)
    rl_aim_slider = Slider(start = rl_aim_slider_start,
                           end = rl_aim_slider_end,
                           value = rl_aim_slider_value,
                           step = rl_aim_slider_step,
                           title = rl_aim_slider_title,
                           disabled = rl_aim_slider_disabled,
                           visible = rl_aim_slider_visibility)
    rm_aim_slider = Slider(start = rm_aim_slider_start,
                           end = rm_aim_slider_end,
                           value = rm_aim_slider_value,
                           step = rm_aim_slider_step,
                           title = rm_aim_slider_title,
                           disabled = rm_aim_slider_disabled,
                           visible = rm_aim_slider_visibility)
    rr_aim_slider = Slider(start = rr_aim_slider_start,
                           end = rr_aim_slider_end,
                           value = rr_aim_slider_value,
                           step = rr_aim_slider_step,
                           title = rr_aim_slider_title,
                           disabled = rr_aim_slider_disabled,
                           visible = rr_aim_slider_visibility)

    iterations_slider = Slider(start = iterations_slider_start,
                               end = iterations_slider_end,
                               value = iterations_slider_value, step = 1,
                               title = iterations_slider_title,
                               disabled = iterations_slider_disabled,
                               visible = iterations_slider_visibility)

    return (ll_aim_slider, lm_aim_slider, lr_aim_slider,
            rl_aim_slider, rm_aim_slider, rr_aim_slider,
            iterations_slider)
#</editor-fold>
#<editor-fold create_gamestate_divs():
def create_gamestate_divs(iterations_to_run_start_text = "50",
                          iterations_to_run_visibility = False,
                          strategy_to_use_start_text = "Not Set",
                          strategy_to_use_visibility = False,
                          ll_scored_start_text = "0",
                          lm_scored_start_text = "0",
                          lr_scored_start_text = "0",
                          rl_scored_start_text = "0",
                          rm_scored_start_text = "0",
                          rr_scored_start_text = "0",
                          ll_scored_visibility = False,
                          lm_scored_visibility = False,
                          lr_scored_visibility = False,
                          rl_scored_visibility = False,
                          rm_scored_visibility = False,
                          rr_scored_visibility = False,
                          ll_blocked_left_start_text = "0",
                          lm_blocked_left_start_text = "0",
                          lr_blocked_left_start_text = "0",
                          rl_blocked_left_start_text = "0",
                          rm_blocked_left_start_text = "0",
                          rr_blocked_left_start_text = "0",
                          ll_blocked_left_visibility = False,
                          lm_blocked_left_visibility = False,
                          lr_blocked_left_visibility = False,
                          rl_blocked_left_visibility = False,
                          rm_blocked_left_visibility = False,
                          rr_blocked_left_visibility = False,
                          ll_blocked_middle_start_text = "0",
                          lm_blocked_middle_start_text = "0",
                          lr_blocked_middle_start_text = "0",
                          rl_blocked_middle_start_text = "0",
                          rm_blocked_middle_start_text = "0",
                          rr_blocked_middle_start_text = "0",
                          ll_blocked_middle_visibility = False,
                          lm_blocked_middle_visibility = False,
                          lr_blocked_middle_visibility = False,
                          rl_blocked_middle_visibility = False,
                          rm_blocked_middle_visibility = False,
                          rr_blocked_middle_visibility = False,
                          ll_blocked_right_start_text = "0",
                          lm_blocked_right_start_text = "0",
                          lr_blocked_right_start_text = "0",
                          rl_blocked_right_start_text = "0",
                          rm_blocked_right_start_text = "0",
                          rr_blocked_right_start_text = "0",
                          ll_blocked_right_visibility = False,
                          lm_blocked_right_visibility = False,
                          lr_blocked_right_visibility = False,
                          rl_blocked_right_visibility = False,
                          rm_blocked_right_visibility = False,
                          rr_blocked_right_visibility = False):

    iterations_to_run = Div(text = iterations_to_run_start_text,
                            visible = iterations_to_run_visibility)

    strategy_to_use = Div(text = strategy_to_use_start_text,
                          visible = strategy_to_use_visibility)

    ll_scored = Div(text = ll_scored_start_text,
                    visible = ll_scored_visibility)
    lm_scored = Div(text = lm_scored_start_text,
                    visible = lm_scored_visibility)
    lr_scored = Div(text = lr_scored_start_text,
                    visible = lr_scored_visibility)
    rl_scored = Div(text = rl_scored_start_text,
                    visible = rl_scored_visibility)
    rm_scored = Div(text = rm_scored_start_text,
                    visible = rm_scored_visibility)
    rr_scored = Div(text = rr_scored_start_text,
                    visible = rr_scored_visibility)

    ll_blocked_left = Div(text = ll_blocked_left_start_text,
                          visible = ll_blocked_left_visibility)
    lm_blocked_left = Div(text = lm_blocked_left_start_text,
                          visible = lm_blocked_left_visibility)
    lr_blocked_left = Div(text = lr_blocked_left_start_text,
                          visible = lr_blocked_left_visibility)
    rl_blocked_left = Div(text = rl_blocked_left_start_text,
                          visible = rl_blocked_left_visibility)
    rm_blocked_left = Div(text = rm_blocked_left_start_text,
                          visible = rm_blocked_left_visibility)
    rr_blocked_left = Div(text = rr_blocked_left_start_text,
                          visible = rr_blocked_left_visibility)

    ll_blocked_middle = Div(text = ll_blocked_middle_start_text,
                            visible = ll_blocked_middle_visibility)
    lm_blocked_middle = Div(text = lm_blocked_middle_start_text,
                            visible = lm_blocked_middle_visibility)
    lr_blocked_middle = Div(text = lr_blocked_middle_start_text,
                            visible = lr_blocked_middle_visibility)
    rl_blocked_middle = Div(text = rl_blocked_middle_start_text,
                            visible = rl_blocked_middle_visibility)
    rm_blocked_middle = Div(text = rm_blocked_middle_start_text,
                            visible = rm_blocked_middle_visibility)
    rr_blocked_middle = Div(text = rr_blocked_middle_start_text,
                            visible = rr_blocked_middle_visibility)

    ll_blocked_right = Div(text = ll_blocked_right_start_text,
                           visible = ll_blocked_right_visibility)
    lm_blocked_right = Div(text = lm_blocked_right_start_text,
                           visible = lm_blocked_right_visibility)
    lr_blocked_right = Div(text = lr_blocked_right_start_text,
                           visible = lr_blocked_right_visibility)
    rl_blocked_right = Div(text = rl_blocked_right_start_text,
                           visible = rl_blocked_right_visibility)
    rm_blocked_right = Div(text = rm_blocked_right_start_text,
                           visible = rm_blocked_right_visibility)
    rr_blocked_right = Div(text = rr_blocked_right_start_text,
                           visible = rr_blocked_right_visibility)

    return (iterations_to_run, strategy_to_use,
            ll_scored, lm_scored, lr_scored,
            rl_scored, rm_scored, rr_scored,
            ll_blocked_left, lm_blocked_left, lr_blocked_left,
            rl_blocked_left, rm_blocked_left, rr_blocked_left,
            ll_blocked_middle, lm_blocked_middle, lr_blocked_middle,
            rl_blocked_middle, rm_blocked_middle, rr_blocked_middle,
            ll_blocked_right, lm_blocked_right, lr_blocked_right,
            rl_blocked_right, rm_blocked_right, rr_blocked_right)
#</editor-fold>
#<editor-fold create_strategy_dropdown():
def create_strategy_dropdown(fictitious_play_text = "Fictitious_Play",
                             mixed_strategy_text = "Mixed_Strategy",
                             dropdown_label = "CPU strategy to Use",
                             dropdown_button_type = "warning",
                             dropdown_disabled = False,
                             dropdown_visibility = False):
    #CPU Strategy to Use Dropdown:
    menu = [(fictitious_play_text, fictitious_play_text),
            (mixed_strategy_text, mixed_strategy_text)]
    strategy_dropdown = Dropdown(label = dropdown_label, menu = menu,
                                 button_type = dropdown_button_type,
                                 disabled = dropdown_disabled,
                                 visible = dropdown_visibility)
    return strategy_dropdown
#</editor-fold>
