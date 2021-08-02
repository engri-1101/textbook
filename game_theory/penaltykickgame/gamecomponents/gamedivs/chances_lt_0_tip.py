from bokeh.models.widgets import Div
def create(game_parts):
    chances_lt_0_tip = Div(
        text = "Chances cannot be less than 0", visible = False
    )
    game_parts.divs['chances_lt_0_tip'] = chances_lt_0_tip
