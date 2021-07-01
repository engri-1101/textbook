from bokeh.models.glyphs import Text

#<editor-fold create():
def create(game_parts, text_color = "whitesmoke", text_font_size = "15pt",
           text_x_offset = 0, text_y_offset = +9, text_baseline = "ideographic",
           text_align = 'left'):
    scr_labels = Text(x = "x", y = "y", text = 'text',
                  text_color = text_color,
                  text_font_size = text_font_size,
                  x_offset = text_x_offset,
                  y_offset = text_y_offset,
                  text_baseline = text_baseline,
                  text_align = text_align)
    game_parts.labels['scr_text'] = scr_labels
#</editor-fold>
