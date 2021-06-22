from bokeh.plotting import figure
from bokeh.models import Circle, Rect

#<editor-fold game_fig_configs:
class Game_fig_configs():
    def __init__(self, tools = "", toolbar_location = None,
                 title = 'FIFA 2020 Penalty Simulator', plot_width = 600,
                 plot_height = 400, x_range = (0, 100), y_range = (0, 90),
                 title_text_font_size = '15pt', xaxis_visible = False,
                 yaxis_visible = False, xgrid_line_color = None,
                 ygrid_line_color = None, outline_line_color = None,
                 background_fill_color = 'green',
                 mline_penaltybox_xs_1 = [24, 76, 78, 22, 24],
                 mline_penaltybox_xs_2 = [3,  12, 88, 97, 3 ],
                 mline_goal_xs = [34, 34, 66, 66],
                 mline_penaltybox_ys_1 = [63, 63, 47, 47, 63],
                 mline_penaltybox_ys_2 = [15, 63, 63, 15, 15],
                 mline_goal_ys = [63, 82, 82, 63],
                 mline_penaltybox_color_1 = "lightgreen",
                 mline_penaltybox_color_2 = "lightgreen",
                 mline_goal_color = "whitesmoke",
                 mline_penaltybox_alpha_1 = 1, mline_penaltybox_alpha_2 = 1,
                 mline_goal_alpha = 1, mline_line_width = 4,
                 penaltyarc_quad_x1 = 33, penaltyarc_quad_y1 = 15,
                 penaltyarc_quad_x2 = 67, penaltyarc_quad_y2 = 15,
                 penaltyarc_quad_c1 = 50, penaltyarc_quad_c2 = 2,
                 penaltyarc_quad_color = 'lightgreen',
                 penaltyarc_quad_line_width = 4, goalie_head_x = 50,
                 goalie_head_y = 69, goalie_head_color = "red",
                 goalie_head_line_width = 2, goalie_head_size = 17,
                 goalie_body_x = 50, goalie_body_y = 65,
                 goalie_body_width = 3, goalie_body_height = 4,
                 goalie_body_angle = 0, goalie_body_color = "red",
                 goalie_body_line_width = 2, ball_x = 50, ball_y = 13,
                 ball_fill_color = "whitesmoke", ball_line_width = 2,
                 ball_size = 17, striker_head_x = 50, striker_head_y = 16,
                 striker_head_color = "lightblue", striker_head_line_width = 2,
                 striker_head_size = 21, striker_body_x = 50,
                 striker_body_y = 11, striker_body_width = 4,
                 striker_body_height = 6, striker_body_angle = 0,
                 striker_body_color = 'lightblue', striker_body_line_width = 2
                 ):
        #<editor-fold Main:
        self.tools = tools
        self.toolbar_location = toolbar_location
        self.title = title
        self.plot_width = plot_width
        self.plot_height = plot_height
        self.x_range = x_range
        self.y_range = y_range
        self.title_text_font_size = title_text_font_size
        self.xaxis_visible = xaxis_visible
        self.yaxis_visible = yaxis_visible
        self.xgrid_line_color = xgrid_line_color
        self.ygrid_line_color = ygrid_line_color
        self.outline_line_color = outline_line_color
        self.background_fill_color = background_fill_color
        #</editor-fold>
        #<editor-fold mline:
        self.mline_penaltybox_xs_1 = mline_penaltybox_xs_1
        self.mline_penaltybox_xs_2 = mline_penaltybox_xs_2
        self.mline_goal_xs = mline_goal_xs
        self.mline_penaltybox_ys_1 = mline_penaltybox_ys_1
        self.mline_penaltybox_ys_2 = mline_penaltybox_ys_2
        self.mline_goal_ys = mline_goal_ys
        self.mline_penaltybox_color_1 = mline_penaltybox_color_1
        self.mline_penaltybox_color_2 = mline_penaltybox_color_2
        self.mline_goal_color = mline_goal_color
        self.mline_penaltybox_alpha_1 = mline_penaltybox_alpha_1
        self.mline_penaltybox_alpha_2 = mline_penaltybox_alpha_2
        self.mline_goal_alpha = mline_goal_alpha
        self.mline_line_width = mline_line_width
        #</editor-fold>
        #<editor-fold penaltyarc:
        self.penaltyarc_quad_x1 = penaltyarc_quad_x1
        self.penaltyarc_quad_y1 = penaltyarc_quad_y1
        self.penaltyarc_quad_x2 = penaltyarc_quad_x2
        self.penaltyarc_quad_y2 = penaltyarc_quad_y2
        self.penaltyarc_quad_c1 = penaltyarc_quad_c1
        self.penaltyarc_quad_c2 = penaltyarc_quad_c2
        self.penaltyarc_quad_color = penaltyarc_quad_color
        self.penaltyarc_quad_line_width = penaltyarc_quad_line_width
        #</editor-fold>
        #<editor-fold goalie:
        self.goalie_head_x = goalie_head_x
        self.goalie_head_y = goalie_head_y
        self.goalie_head_color = goalie_head_color
        self.goalie_head_line_width = goalie_head_line_width
        self.goalie_head_size = goalie_head_size
        self.goalie_body_x = goalie_body_x
        self.goalie_body_y = goalie_body_y
        self.goalie_body_width = goalie_body_width
        self.goalie_body_height = goalie_body_height
        self.goalie_body_angle = goalie_body_angle
        self.goalie_body_color = goalie_body_color
        self.goalie_body_line_width = goalie_body_line_width
        #</editor-fold>
        #<editor-fold ball:
        self.ball_x = ball_x
        self.ball_y = ball_y
        self.ball_fill_color = ball_fill_color
        self.ball_line_width = ball_line_width
        self.ball_size = ball_size
        #</editor-fold>
        #<editor-fold striker:
        self.striker_head_x = striker_head_x
        self.striker_head_y = striker_head_y
        self.striker_head_color = striker_head_color
        self.striker_head_line_width = striker_head_line_width
        self.striker_head_size = striker_head_size
        self.striker_body_x = striker_body_x
        self.striker_body_y = striker_body_y
        self.striker_body_width = striker_body_width
        self.striker_body_height = striker_body_height
        self.striker_body_angle = striker_body_angle
        self.striker_body_color = striker_body_color
        self.striker_body_line_width = striker_body_line_width
        #</editor-fold>
#</editor-fold>

#<editor-fold game_figure_setup:
def game_figure_setup(fig_configs):

    game_figure = figure(tools = fig_configs.tools,
                         toolbar_location = fig_configs.toolbar_location,
                         title = fig_configs.title,
                         plot_width = fig_configs.plot_width,
                         plot_height = fig_configs.plot_height,
                         x_range = fig_configs.x_range,
                         y_range = fig_configs.y_range)

    game_figure.title.text_font_size = fig_configs.title_text_font_size
    #Hide Axes and Gridlines
    game_figure.xaxis.visible = fig_configs.xaxis_visible
    game_figure.yaxis.visible = fig_configs.yaxis_visible
    game_figure.xgrid.grid_line_color = fig_configs.xgrid_line_color
    game_figure.ygrid.grid_line_color = fig_configs.ygrid_line_color
    game_figure.outline_line_color = fig_configs.outline_line_color
    #Background Color
    game_figure.background_fill_color = fig_configs.background_fill_color
    #Goal Posts and Lines
    game_figure.multi_line([fig_configs.mline_penaltybox_xs_1,
                            fig_configs.mline_penaltybox_xs_2,
                            fig_configs.mline_goal_xs],
                           [fig_configs.mline_penaltybox_ys_1,
                            fig_configs.mline_penaltybox_ys_2,
                            fig_configs.mline_goal_ys],
                           color = [fig_configs.mline_penaltybox_color_1,
                                    fig_configs.mline_penaltybox_color_2,
                                    fig_configs.mline_goal_color],
                           alpha = [fig_configs.mline_penaltybox_alpha_1,
                                    fig_configs.mline_penaltybox_alpha_2,
                                    fig_configs.mline_goal_alpha],
                           line_width = fig_configs.mline_line_width)

    #Striker Box
    game_figure.quadratic(fig_configs.penaltyarc_quad_x1,
                          fig_configs.penaltyarc_quad_y1,
                          fig_configs.penaltyarc_quad_x2,
                          fig_configs.penaltyarc_quad_y2,
                          fig_configs.penaltyarc_quad_c1,
                          fig_configs.penaltyarc_quad_c2,
                          color = fig_configs.penaltyarc_quad_color,
                          line_width = fig_configs.penaltyarc_quad_line_width)
    #Goalie Sprite
    goalie_head = Circle(x = fig_configs.goalie_head_x,
                         y = fig_configs.goalie_head_y,
                         fill_color = fig_configs.goalie_head_color,
                         line_width = fig_configs.goalie_head_line_width,
                         size = fig_configs.goalie_head_size)
    goalie_body = Rect(x = fig_configs.goalie_body_x,
                       y = fig_configs.goalie_body_y,
                       width = fig_configs.goalie_body_width,
                       height = fig_configs.goalie_body_height,
                       angle = fig_configs.goalie_body_angle,
                       fill_color = fig_configs.goalie_body_color,
                       line_width = fig_configs.goalie_body_line_width)
    game_figure.add_glyph(goalie_head)
    game_figure.add_glyph(goalie_body)

    #Ball
    ball = Circle(x = fig_configs.ball_x, y = fig_configs.ball_y,
                  fill_color = fig_configs.ball_fill_color,
                  line_width = fig_configs.ball_line_width,
                  size = fig_configs.ball_size)
    game_figure.add_glyph(ball);

    #Striker Sprite
    game_figure.add_glyph(Circle(x = fig_configs.striker_head_x,
                                 y = fig_configs.striker_head_y,
                                 fill_color = fig_configs.striker_head_color,
                                 line_width = fig_configs.striker_head_line_width,
                                 size = fig_configs.striker_head_size)) # head
    game_figure.add_glyph(Rect(x = fig_configs.striker_body_x,
                               y = fig_configs.striker_body_y,
                               width = fig_configs.striker_body_width,
                               height = fig_configs.striker_body_height,
                               angle = fig_configs.striker_body_angle,
                               fill_color = fig_configs.striker_body_color,
                               line_width =  fig_configs.striker_body_line_width)); #body

    return game_figure, goalie_head, goalie_body, ball
#</editor-fold>
