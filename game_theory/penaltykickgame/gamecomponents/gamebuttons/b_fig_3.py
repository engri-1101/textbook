from bokeh.models import Button, CustomJS

#<editor-fold Callback Code String:
fig3ButtonCode = """
fig1Button.disabled = false;
fig2Button.disabled = false;
fig3Button.disabled = true;
fig4Button.disabled = false;
statsFig1.visible = false;
statsFig2.visible = false;
statsFig3.visible = true;
statsFig4.visible = false;
"""
#</editor-fold>

#<editor-fold create():
def create(game_parts, config):
    b_fig_3 = Button(label = config.label, button_type = config.button_type,
                     sizing_mode = config.sizing_mode,
                     width_policy = config.width_policy,
                     disabled = config.disabled, visible = config.visible)
    game_parts.buttons['fig_3'] = b_fig_3
#</editor-fold>

#<editor-fold setup():
def setup(game_parts):
    args_dict = dict(fig1Button = game_parts.buttons['fig_1'],
                     fig2Button = game_parts.buttons['fig_2'],
                     fig3Button = game_parts.buttons['fig_3'],
                     fig4Button = game_parts.buttons['fig_4'],
                     statsFig1 = game_parts.figures['stats_1'],
                     statsFig2 = game_parts.figures['stats_2'],
                     statsFig3 = game_parts.figures['stats_3'],
                     statsFig4 = game_parts.figures['stats_4'])
    b_fig_3_click = CustomJS(args = args_dict, code = fig3ButtonCode)
    game_parts.buttons['fig_3'].js_on_click(b_fig_3_click)
#</editor-fold>
