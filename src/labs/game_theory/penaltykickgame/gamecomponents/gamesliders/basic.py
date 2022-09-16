from bokeh.models import Slider

#<editor-fold create():
def create(game_parts, config, name):
    """Creates a basic Bokeh Slider that does not require a javascript callback,
    according to the passed in configs. Following its completion, the Slider is
    then added to the _GameParts object being used to collect the game
    components under name.


    Arguments:
    game_parts -- The _GameParts object being used to collect the
      game components.
    config -- The config object being used to configure the Slider.
    name -- A string containing the name to add the slider under.
    """
    slider = Slider(
        start=config.start, end=config.end, value=config.value,
        step=config.step, title=config.title, disabled=config.disabled,
        visible=config.visible
    )
    game_parts.sliders[name] = slider
#</editor-fold>
