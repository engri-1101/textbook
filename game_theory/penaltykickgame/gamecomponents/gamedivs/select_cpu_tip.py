from bokeh.models.widgets import Div
def create(game_parts):
    select_cpu_tip = Div(text = "Select A CPU Strategy From the Dropdown",
                         visible = False)
    game_parts.divs['select_cpu_tip'] = select_cpu_tip
