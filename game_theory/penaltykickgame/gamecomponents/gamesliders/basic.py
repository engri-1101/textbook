from bokeh.models import Slider

#<editor-fold create():
def create(game_parts, config, name):
    slider = Slider(
        start=config.start, end=config.end, value=config.value,
        step=config.step, title=config.title, disabled=config.disabled,
        visible=config.visible
    )
    game_parts.sliders[name] = slider
#</editor-fold>
