from bokeh.models.glyphs import Text

#<editor-fold create():
def create(game_parts, config):
    label = Text(
        x="x", y="y", text="text", text_color=config.text_color,
        text_font_size=config.text_font_size, x_offset=config.text_x_offset,
        y_offset=config.text_y_offset, text_baseline=config.text_baseline,
        text_align=config.text_align
    )
    game_parts.labels["scr_text"] = label
#</editor-fold>
