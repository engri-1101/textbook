from bokeh.models import ColumnDataSource
#<editor-fold create():
def create(game_parts, xs = [2, 70, 2, 14, 14], ys = [86, 86, 5, 40, 32],
           ln_1 = 'Rounds played: 0', ln_2 = 'Total score: 0', ln_3 = '',
           ln_4 = '', ln_5 = ''):

    scr_text = ColumnDataSource({'x' : xs,
                                 'y' : ys,
                                 'text' : [ln_1, ln_2, ln_3, ln_4, ln_5]})
    game_parts.texts['scr_text'] = scr_text
#</editor-fold>
