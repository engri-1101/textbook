from bokeh.models import Slider

#<editor-fold create():
#Needs:
#   from bokeh.models import Slider
def create(game_parts, config):
    auto_advance_speed_slider = Slider(start = config.start, end = config.end,
                                       value = config.value,
                                       step = config.step, title = config.title,
                                       disabled = config.disabled,
                                       visible = config.visible)
    game_parts.sliders['auto_advance_speed'] = auto_advance_speed_slider
#</editor-fold>
