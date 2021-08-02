from bokeh.models.widgets import Div
def create(game_parts):
    chances_gt_1_tip = Div(
        text = "Chances cannot be greater than 1", visible = False
    )
    game_parts.divs['chances_gt_1_tip'] = chances_gt_1_tip
