from bokeh.models import Toggle, CustomJS

#<editor-fold create():
def create(game_parts, config):
    toggleButton = Toggle(
        label=config.label, button_type=config.button_type,
        sizing_mode=config.sizing_mode, width_policy=config.width_policy,
        disabled=config.disabled, visible=config.visible
    )
    game_parts.buttons["auto_advance"] = toggleButton
#</editor-fold>
