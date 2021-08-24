from bokeh.models import Toggle, CustomJS

#<editor-fold create():
def create(game_parts, config):
    """Creates a Bokeh Toggle Button used to set whether or not the game should
    automatically advance between iterations, then adds it into the passed in
    _GameParts object being used to collect the game components.


    Arguments:
    game_parts -- The _GameParts object being used to collect the
      game components.
    config -- The config object being used to configure the toggle button.
    """
    toggleButton = Toggle(
        label=config.label, button_type=config.button_type,
        sizing_mode=config.sizing_mode, width_policy=config.width_policy,
        disabled=config.disabled, visible=config.visible
    )
    game_parts.buttons["auto_advance"] = toggleButton
#</editor-fold>
