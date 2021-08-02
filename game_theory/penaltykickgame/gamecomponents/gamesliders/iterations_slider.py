from bokeh.models import Slider, CustomJS

#<editor-fold create():
def create(game_parts, config):
    iterations_slider = Slider(
        start = config.start, end = config.end, value = config.value,
        step = config.step, title = config.title, disabled = config.disabled,
        visible = config.visible
    )
    game_parts.sliders['iterations'] = iterations_slider
#</editor-fold>
