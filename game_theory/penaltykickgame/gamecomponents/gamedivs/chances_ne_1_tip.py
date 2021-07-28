from bokeh.models.widgets import Div
def create(game_parts):
    chances_ne_1_tip = Div(text = "Chances must add up to 1",
                           visible = False)
    game_parts.divs['chances_ne_1_tip'] = chances_ne_1_tip
