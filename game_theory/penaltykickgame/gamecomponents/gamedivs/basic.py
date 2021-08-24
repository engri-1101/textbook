from bokeh.models.widgets import Div

#<editor-fold create_configurable():
def create_configurable(game_parts, config, name):
    """Creates a basic configurable div using the config object passed to it,
    then adds it to the _GameParts object being used to collect the game
    components under the provided name.


    Arguments:
    game_parts -- The _GameParts object being used to collect the
      game components.
    config -- The config object being used to configure the div.
    name -- A string containing the name to put the div under in game_parts.
    """
    div = Div(text=config.text, visible=config.visible)
    game_parts.divs[name] = div
#</editor-fold>

#<editor-fold create_game_vars():
def create_game_vars(game_parts):
    """Creates the basic divs used to track the selected kicker foot, the
    selected kicker kick direction, the iteration number of the game, the game
    score, and the strategy to use.


    Argument:
    game_parts -- The _GameParts object containing the game components.
    """
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
