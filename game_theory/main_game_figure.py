from bokeh.plotting import figure
from bokeh.models import Circle, Rect

def game_figure_setup(tools = "", toolbar_location = None,
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
                      mline_penaltybox_alpha_1 = 1,
                      mline_penaltybox_alpha_2 = 1, mline_goal_alpha = 1,
                      mline_line_width = 4, penaltyarc_quad_x1 = 33,
                      penaltyarc_quad_y1 = 15, penaltyarc_quad_x2 = 67,
                      penaltyarc_quad_y2 = 15, penaltyarc_quad_c1 = 50,
                      penaltyarc_quad_c2 = 2,
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
                      striker_head_color = 'lightblue',
                      striker_head_line_width = 2, striker_head_size = 21,
                      striker_body_x = 50, striker_body_y = 11,
                      striker_body_width = 4, striker_body_height = 6,
                      striker_body_angle = 0, striker_body_color = 'lightblue',
                      striker_body_line_width = 2):

    game_figure = figure(tools = tools, toolbar_location = toolbar_location,
                         title = title, plot_width = plot_width,
                         plot_height = plot_height,
                         x_range = x_range, y_range = y_range)

    game_figure.title.text_font_size = title_text_font_size
    #Hide Axes and Gridlines
    game_figure.xaxis.visible = xaxis_visible
    game_figure.yaxis.visible = yaxis_visible
    game_figure.xgrid.grid_line_color = xgrid_line_color
    game_figure.ygrid.grid_line_color = ygrid_line_color
    game_figure.outline_line_color = outline_line_color
    #Background Color
    game_figure.background_fill_color = background_fill_color
    #Goal Posts and Lines
    game_figure.multi_line([mline_penaltybox_xs_1, mline_penaltybox_xs_2,
                            mline_goal_xs],
                           [mline_penaltybox_ys_1, mline_penaltybox_ys_2,
                            mline_goal_ys],
                           color = [mline_penaltybox_color_1,
                                    mline_penaltybox_color_2,
                                    mline_goal_color],
                           alpha = [mline_penaltybox_alpha_1,
                                    mline_penaltybox_alpha_2,
                                    mline_goal_alpha],
                           line_width = mline_line_width)

    #Striker Box
    game_figure.quadratic(penaltyarc_quad_x1, penaltyarc_quad_y1,
                          penaltyarc_quad_x2, penaltyarc_quad_y2,
                          penaltyarc_quad_c1, penaltyarc_quad_c2,
                          color = penaltyarc_quad_color,
                          line_width = penaltyarc_quad_line_width)
    #Goalie Sprite
    goalie_head = Circle(x = goalie_head_x, y = goalie_head_y,
                         fill_color = goalie_head_color,
                         line_width = goalie_head_line_width,
                         size = goalie_head_size)
    goalie_body = Rect(x = goalie_body_x, y = goalie_body_y,
                       width = goalie_body_width, height = goalie_body_height,
                       angle = goalie_body_angle,
                       fill_color = goalie_body_color,
                       line_width = goalie_body_line_width)
    game_figure.add_glyph(goalie_head)
    game_figure.add_glyph(goalie_body)

    #Ball
    ball = Circle(x = ball_x, y = ball_y, fill_color = ball_fill_color,
                  line_width = ball_line_width, size = ball_size)
    game_figure.add_glyph(ball);

    #Striker Sprite
    game_figure.add_glyph(Circle(x = striker_head_x, y = striker_head_y,
                                 fill_color = striker_head_color,
                                 line_width = striker_head_line_width,
                                 size = striker_head_size)) # head
    game_figure.add_glyph(Rect(x = striker_body_x, y = striker_body_y,
                               width = striker_body_width,
                               height = striker_body_height,
                               angle = striker_body_angle,
                               fill_color = striker_body_color,
                               line_width =  striker_body_line_width)); #body

    return game_figure, goalie_head, goalie_body, ball
