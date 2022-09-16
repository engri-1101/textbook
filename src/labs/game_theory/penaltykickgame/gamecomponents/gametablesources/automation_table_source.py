from bokeh.models import ColumnDataSource

#<editor-fold create():
def create(game_parts, config):
    """Creates the ColumnDataSource for the game's automation table, then adds
    it to the passed in _GameParts object being used to collect the game
    components.


    Arguments:
    game_parts -- The _GameParts object being used to collect the
      game components.
    config -- The config object being used to configure the distribution
      table source.
    """
    f_left = config.footedness_left_text
    f_right = config.footedness_right_text
    ad_left = config.aim_direction_left_text
    ad_middle = config.aim_direction_middle_text
    ad_right = config.aim_direction_right_text
    footedness = [f_left, f_left, f_left, f_right, f_right, f_right]
    aim_direction = [
        ad_left, ad_middle, ad_right, ad_left, ad_middle, ad_right
    ]
    chances = [0, 0, 0, 0, 0, 0]

    data = {
        "footedness" : footedness,
        "aim_direction" : aim_direction,
        "chances" : chances
    }

    table_src = ColumnDataSource(data)
    game_parts.sources["automation_table"] = table_src
#</editor-fold>
