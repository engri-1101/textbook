from bokeh.models.widgets import Div

#<editor-fold create_configurable():
def create_configurable(game_parts, config, name):
    div = Div(text=config.text, visible=config.visible)
    game_parts.divs[name] = div
#</editor-fold>

#<editor-fold create_game_vars():
def create_game_vars(game_parts):
    kf_div = Div(text="", visible=False)
    game_parts.divs["kicker_foot"] = kf_div
    kk_div = Div(text="", visible=False)
    game_parts.divs["kicker_kick"] = kk_div
    nround_div = Div(text="0", visible=False)
    game_parts.divs["nround"] = nround_div
    score_div = Div(text="0", visible=False)
    game_parts.divs["score"] = score_div
    strat_div = Div(text="Not Set", visible=False)
    game_parts.divs["strategy_to_use"] = strat_div
#</editor-fold>
