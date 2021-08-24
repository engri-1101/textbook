from bokeh.models import ColumnDataSource

def create(game_parts, config):
    """Creates a ColumnDataSource to use for text to put on the game figure,
    then adds it to the passed in _GameParts object being used to collect the
    game components.


    Arguments:
    game_parts -- The _GameParts object being used to collect the game
      components.
    config -- The config object being used to configure scr_text.
    """
    data = {"x" : config.xs, "y" : config.ys, "text" : config.text_lines}
    text = ColumnDataSource(data)
    game_parts.texts["scr_text"] = text
