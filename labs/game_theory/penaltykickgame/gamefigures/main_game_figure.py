from bokeh.plotting import figure
from bokeh.models import Circle, Rect
from . import figure_creation as fig_creation

#<editor-fold Configs:
class Configs:
    """A class used to configure the main game figure.


    Attributes:
    main_fig -- A figure_creation.FigureConfigs object used to configure the
      main figure.
    penalty_box_line_sets -- A list _FigLineSetConfigs objects used to configure
      the figure's penalty box lines.
    goal_lines -- A _FigLineSetConfigs object used to configure the figure's
      goal.
    penalty_arc -- A _PenaltyArcConfigs object used to configure the figure's
      penalty arc.
    keeper -- A _PlayerGlyphConfigs object used to configure the keeper glyphs.
    striker -- A _PlayerGlyphConfigs object used to configure the
      striker glyphs.
    ball -- A _BallConfigs object used to configure the ball glyph.


    Inner Classes:
    _FigLineSetConfigs -- A class for configuring sets of lines present on the
      figure.
    _PenaltyArcConfigs -- A class for configuring the penalty arc on the figure.
    _PlayerGlyphConfigs -- A class for configuring the player glyphs.
    _BallConfigs -- A class for configuring the ball glyph.
    """
    #<editor-fold __init__():
    def __init__(
        self, fig_base_tools="", fig_toolbar_loc=None, fig_toolbar_sticky=False,
        fig_title="FIFA 2020 Penalty Simulator", fig_width=600, fig_height=400,
        fig_x_range=(0, 100), fig_y_range=(0, 90), fig_visibility=True,
        fig_sizing_mode="stretch_width", fig_outline_line_color="black",
        fig_background_color="green", fig_title_font_size="15pt",
        fig_x_axis_visibility=False, fig_y_axis_visibility=False,
        fig_x_axis_line_color="black", fig_y_axis_line_color="black",
        fig_x_grid_visibility=False, fig_y_grid_visibility=False,
        fig_x_grid_line_color="black", fig_y_grid_line_color="black",
        pbox_line_set_xs=[[24, 76, 78, 22, 24], [3, 12, 88, 97, 3]],
        pbox_line_set_ys=[[63, 63, 47, 47, 63], [15, 63, 63, 15, 15]],
        pline_color="lightgreen",  pline_alpha=1, pline_width=4,
        goal_xs=[34, 34, 66, 66], goal_ys=[63, 82, 82, 63],
        goal_color="whitesmoke", goal_alpha=1, goal_line_width=4,
        penalty_arc_x0=33, penalty_arc_y0=15, penalty_arc_x1=67,
        penalty_arc_y1=15, penalty_arc_cx=50, penalty_arc_cy=2,
        keeper_head_x=50, keeper_head_y=69, keeper_head_color="red",
        keeper_head_line_width=2, keeper_head_size=17, keeper_body_x=50,
        keeper_body_y=65, keeper_body_width=3, keeper_body_height=4,
        keeper_body_angle=0, keeper_body_color="red", keeper_body_line_width=2,
        striker_head_x=50, striker_head_y=16, striker_head_color="lightblue",
        striker_head_line_width=2, striker_head_size=21, striker_body_x=50,
        striker_body_y=11, striker_body_width=4, striker_body_height=6,
        striker_body_angle=0, striker_body_color="lightblue",
        striker_body_line_width=2, ball_x=50, ball_y=13,
        ball_fill_color="whitesmoke", ball_line_width=2, ball_size=17
    ):
        """Initializer for the class Configs. Creates a Configs object
        containing the relevant information for creating the figure with the
        input argument values.


        Keyword Arguments:
        fig_base_tools -- A string containing the base tools to add to the
          figure. Must be Bokeh compatible.
        fig_toolbar_loc -- A string containing the location to use for the
          figure toolbar. Must be Bokeh compatible.
        fig_toolbar_sticky -- A bool for whether or not to make the figure tool
          bar sticky.
        fig_title -- A string. The title to use for the figure.
        fig_width -- An int. The width to use for the figure.
        fig_height -- An int. The width to use for the figure.
        fig_x_range -- An (int, int) or (float, float) pair containing the
          x range to use for the figure.
        fig_y_range -- An (int, int) or (float, float) pair cointaining the
          y range to use for the figure.
        fig_visibility -- A bool for setting the figure's initial visibility.
        fig_sizing_mode -- A string containing how the figure should be sized.
          Must be Bokeh compatible.
        fig_outline_line_color -- A string containing the color to use for the
          figure outline. Must be Bokeh compatible.
        fig_background_color -- A string containing the color to use for the
          figure background. Must be Bokeh compatible.
        fig_title_font_size -- A string containing the font size to use for the
          figure title. Must be Bokeh compatible.
        fig_x_axis_visibility -- A bool for setting the figure's
          x axis' visibility.
        fig_y_axis_visibility -- A bool for setting the figure's
          y axis' visibility.
        fig_x_axis_line_color -- A string containing the color to use for the
          figure's x axis. Must be Bokeh compatible.
        fig_y_axis_line_color -- A string containing the color to use for the
          figure's y axis. Must be Bokeh compatible.
        fig_x_grid_visibility -- A bool for setting the figure's
          x grid's visibility.
        fig_y_grid_visibility -- A bool for setting the figure's
          y grid's visibility.
        fig_x_grid_line_color -- A string containing the color to use for the
          figure's x grid. Must be Bokeh compatible.
        fig_y_grid_line_color -- A string containing the color to use for the
          figure's y grid. Must be Bokeh compatible.
        pbox_line_set_xs -- A list containing lists of ints to use as the xs for
          the sets of lines for the penalty box.
        pbox_line_set_ys -- A list containing lists of ints to use as the ys for
          the sets of lines for the penalty box.
        pline_color -- A string containing the color to use for the figure's
          penalty area lines. Must be Bokeh compatible.
        pline_alpha -- An int or float between 0 and 1 to use for the penalty
          area lines' alphas.
        pline_width -- An int or float to use as the width for the penalty
          area lines.
        goal_xs -- A list of ints to use as the xs for the set of lines for
          the goal.
        goal_ys -- A list of ints to use as the ys for the set of lines for
          the goal.
        goal_color -- A string containing the color to use for the figure's goal
          lines. Must be Bokeh compatible.
        goal_alpha -- An int or float between 0 and 1 to use as the alpha for
          the figure's goal lines.
        goal_line_width -- An int or float to use as the width for the figure's
          goal lines.
        penalty_arc_x0 -- An int or float to use as the x0 coordinate for the
          figure's penalty arc quad.
        penalty_arc_y0 -- An int or float to use as the y0 coordinate for the
          figure's penalty arc quad.
        penalty_arc_x1 -- An int or float to use as the x1 coordinate for the
          figure's penalty arc quad.
        penalty_arc_y1 -- An int or float to use as the y1 coordinate for the
          figure's penalty arc quad.
        penalty_arc_cx -- An int or float to use as the cx coordinate for the
          figure's penalty arc quad.
        penalty_arc_cy -- An int or float to use as the cy coordinate for the
          figure's penalty arc quad.
        keeper_head_x -- An int or float to use as the x coordinate for the
          keeper's head glyph.
        keeper_head_y -- An int or float to use as the y coordinate for the
          keeper's head glyph.
        keeper_head_color -- A string containing the color to use for the
          keeper's head glyph.
        keeper_head_line_width -- An int or float to use as the line width for
          the keeper's head glyph.
        keeper_head_size -- An int or float to use as the size for the keeper's
          head glyph.
        keeper_body_x -- An int or float to use as the x coordinate for the
          keeper's body glyph.
        keeper_body_y -- An int or float to use as the y coordinate for the
          keeper's body glyph.
        keeper_body_width -- An int or float to use as the width for the
          keeper's body glyph.
        keeper_body_height -- An int or float to use as the height for the
          keeper's body glyph.
        keeper_body_angle -- An int or float to use as the angle (rad) for the
          keeper's body glyph.
        keeper_body_color -- A string containing the color to use for the
          keeper's body glyph.
        keeper_body_line_width -- An int or float to use as the line width for
          the keeper's body glyph.
        striker_head_x -- An int or float to use as the x coordinate for the
          striker's head glyph.
        striker_head_y -- An int or float to use as the y coordinate for the
          striker's head glyph.
        striker_head_color -- A string containing the color to use for the
          striker's head glyph.
        striker_head_line_width -- An int or float to use as the line width for
          the striker's head glyph.
        striker_head_size -- An int or float to use as the size for the
          striker's head glyph.
        striker_body_x -- An int or float to use as the x coordinate for the
          striker's body glyph.
        striker_body_y -- An int or float to use as the y coordinate for the
          striker's body glyph.
        striker_body_width -- An int or float to use as the width for the
          striker's body glyph.
        striker_body_height -- An int or float to use as the height for the
          striker's body glyph.
        striker_body_angle -- An int or float to use as the angle (rad) for the
          striker's body glyph.
        striker_body_color -- A string containing the color to use for the
          striker's body glyph.
        striker_body_line_width -- An int or float to use as the line width for
          the striker's body glyph.
        ball_x -- An int or float to use as the x coordinate of the ball glyph.
        ball_y -- An int or float to use as the y coordinate of the ball glyph.
        ball_fill_color -- A string containing the color to use for the ball's
          glyph. Must be Bokeh compatible.
        ball_line_width -- An int or float to use as the line width for the
          ball's glyph.
        ball_size -- An int or float to use as the size for the ball's glyph.
        """
        self.main_fig = fig_creation.FigureConfigs(
            fig_base_tools, fig_toolbar_loc, fig_toolbar_sticky, fig_title,
            fig_width, fig_height, fig_x_range, fig_y_range, fig_visibility,
            fig_sizing_mode, fig_outline_line_color, fig_background_color,
            fig_title_font_size, fig_x_axis_visibility, fig_y_axis_visibility,
            fig_x_axis_line_color, fig_y_axis_line_color, fig_x_grid_visibility,
            fig_y_grid_visibility, fig_x_grid_line_color, fig_y_grid_line_color
        )
        self.penalty_box_line_sets = []
        for i in range(len(pbox_line_set_xs)):
            line_set = self._FigLineSetConfigs(
                pbox_line_set_xs[i], pbox_line_set_ys[i], pline_color,
                pline_alpha, pline_width
            )
            self.penalty_box_line_sets.append(line_set)
        self.goal_lines = self._FigLineSetConfigs(
            goal_xs, goal_ys, goal_color, goal_alpha, goal_line_width
        )
        self.penalty_arc = self._PenaltyArcConfigs(
            penalty_arc_x0, penalty_arc_y0, penalty_arc_x1, penalty_arc_y1,
            penalty_arc_cx, penalty_arc_cy, pline_color, pline_alpha,
            pline_width
        )
        self.keeper = self._PlayerGlyphConfigs(
            keeper_head_x, keeper_head_y, keeper_head_color,
            keeper_head_line_width, keeper_head_size, keeper_body_x,
            keeper_body_y, keeper_body_width, keeper_body_height,
            keeper_body_angle, keeper_body_color, keeper_body_line_width
        )
        self.striker = self._PlayerGlyphConfigs(
            striker_head_x, striker_head_y, striker_head_color,
            striker_head_line_width, striker_head_size, striker_body_x,
            striker_body_y, striker_body_width, striker_body_height,
            striker_body_angle, striker_body_color, striker_body_line_width
        )
        self.ball = self._BallConfigs(
            ball_x, ball_y, ball_fill_color, ball_line_width, ball_size
        )
    #</editor-fold>

    #<editor-fold _FigLineSetConfigs:
    class _FigLineSetConfigs:
        """A class used to configure a set of lines present within the game
        figure.


        Attributes:
        xs -- A list of ints or floats. The values to use as the x coordinates
          of the points that define the set of lines.
        ys -- A list of ints or floats. The values to use as the y coordinates
          of the points that define the set of lines.
        color -- A string containing a color to use for the set of lines. Must
          be Bokeh compatible.
        alpha -- An int or float between 0 and 1. The alpha value to use for
          the set of lines.
        width -- An int or float. The value to use as the line_width of
          the set of lines.
        """
        #<editor-fold __init__():
        def __init__(self, xs, ys, color, alpha, width):
            """Initializer for the private inner class _FigLineSetConfigs.
            Creates a _FigLineSetConfigs object with the input argument values.


            Arguments:
            xs -- A list of ints or floats. The value to set self.xs to.
            ys -- A list of ints or floats. The value to set self.ys to.
            color -- A string containing a color. The value to set self.color
              to. Must be Bokeh compatible.
            alpha -- An int or float between 0 and 1. The value to set
              self.alpha to.
            width -- An int or float. The value to set self.width to.
            """
            self.xs = xs
            self.ys = ys
            self.color = color
            self.alpha = alpha
            self.width = width
        #</editor-fold>
    #</editor-fold>

    #<editor-fold _PenaltyArcConfigs:
    class _PenaltyArcConfigs:
        """A class used to configure the quad used for the penalty arc in the
        main game figure.


        Attributes:
        x0 -- An int or float. The x0 coord to use for the penalty arc quad.
        y0 -- An int or float. The y0 coord to use for the penalty arc quad.
        x1 -- An int or float. The x1 coord to use for the penalty arc quad.
        y1 -- An int or float. The y1 coord to use for the penalty arc quad.
        cx -- An int or float. The cx coord to use for the penalty arc quad.
        cy -- An int or float. The cy coord to use for the penalty arc quad.
        color -- A string containing a color to use for the penalty arc quad.
          Must be Bokeh compatible.
        alpha -- An int or float between 0 and 1. The alpha to use for the
          penalty arc quad.
        line_width -- An int or float. The line width to use for the penalty
          arc quad.
        """
        #<editor-fold __init__():
        def __init__(self, x0, y0, x1, y1, cx, cy, color, alpha, line_width):
            """Initializer for the private inner class _PenaltyArcConfigs.
            Creates a _PenaltyArcConfigs object with the input argument values.


            Arguments:
            x0 -- An int or float. The value to use for self.x0
            y0 -- An int or float. The value to use for self.y0
            x1 -- An int or float. The value to use for self.x1
            y1 -- An int or float. The value to use for self.y1
            cx -- An int or float. The value to use for self.cx
            cy -- An int or float. The value to use for self.cy
            color -- A string containing a color. The value to use for
              self.color. Must be Bokeh compatible.
            alpha -- An int or float between 0 and 1. The value to use
              for self.alpha.
            line_width -- An int or float. The value to use for self.line_width.
            """
            self.x0 = x0
            self.y0 = y0
            self.x1 = x1
            self.y1 = y1
            self.cx = cx
            self.cy = cy
            self.color = color
            self.alpha = alpha
            self.line_width = line_width
        #</editor-fold>
    #</editor-fold>

    #<editor-fold _PlayerGlyphConfigs:
    class _PlayerGlyphConfigs:
        """A class used to configure the player glyphs of the main game figure.


        Attributes:
        head -- The _Head object containing the values to use for the head glyph
          for the player.
        body -- the _Body object containing the values to use for the body glyph
          for the player.
        """
        #<editor-fold __init__():
        def __init__(
            self, head_x, head_y, head_color, head_line_width, head_size,
            body_x, body_y, body_width, body_height, body_angle, body_color,
            body_line_width
        ):
            """Initializer for the private inner class _PlayerGlyphConfigs.
            Creates a _PlayerGlyphConfigs with a head and body that use the
            input values from the arguments.


            Arguments:
            head_x -- An int or float. The x coordinate to use for the player's
              head glyph.
            head_y -- An int or float. The y coordinate to use for the player's
              head glyph.
            head_color -- A string containing a color to use for the player's
              head glyph. Must be Bokeh compatible.
            head_line_width -- An int or float. The line width to use for the
              player's head glyph.
            head_size -- An int or float. The size to use for the player's head
              glyph.
            body_x -- An int or float. The x coordinate to use for the player's
              body glyph.
            body_y -- An int or float. The y coordinate to use for the player's
              body glyph.
            body_width -- An int or float. The width to use for the player's
              body glyph.
            body_height -- An int or float. The color to use for the player's
              body glyph.
            body_angle -- An int or float. The angle (rad) to use for the
              player's body glyph.
            body_color -- A string containing a color to use for the player's
              body glyph. Must be Bokeh compatible.
            body_line_width -- An int or float. The line width to use for the
              player's body glyph.
            """
            self.head = self._Head(
                head_x, head_y, head_color, head_line_width, head_size
            )
            self.body = self._Body(
                body_x, body_y, body_width, body_height, body_angle, body_color,
                body_line_width
            )
        #</editor-fold>

        #<editor-fold _Head:
        class _Head:
            """A class used to configure the head glyph of a player within the
            main game figure.


            Attributes:
            x -- An int or float. The x coordinate of the head.
            y -- An int or float. The y coordinate of the head.
            color -- A string containing a color to use for the head. Must be
              Bokeh compatible.
            line_width -- An int or float. The line width of the head.
            size -- An int or float. The size of the head.
            """
            #<editor-fold __init__():
            def __init__(self, x, y, color, line_width, size):
                """Initializer for the private inner class _Head. Creates a
                _Head object with the input values.


                Arguments:
                x -- An int or float. The value to set self.x to.
                y -- An int or float. The value to set self.y to.
                color -- A string containing a color to set self.color to. Must
                  be Bokeh compatible.
                line_width -- An int or float. The value to set
                  self.line_width to.
                size -- An int or float. The value to set self.size to.
                """
                self.x = x
                self.y = y
                self.color = color
                self.line_width = line_width
                self.size = size
            #</editor-fold>
        #</editor-fold>

        #<editor-fold _Body:
        class _Body:
            """A class used to configure the body glyph of a player within the
            main game figure.


            Attributes:
            x -- An int or float. The x coordinate of the body.
            y -- An int or float. The y coordinate of the body.
            width -- An int or float. The width of the body.
            height -- An int or float. The height of the body.
            angle -- An int or float. The angle in radians that the body is
              rotated to.
            color -- A string containing a color to use for the body. Must be
              Bokeh compatible.
            line_width -- An int or float. The line width of the body.
            """
            #<editor-fold __init__():
            def __init__(self, x, y, width, height, angle, color, line_width):
                """Initializer for the private inner class _Head. Creates a
                _Head object with the input values.


                Arguments:
                x -- An int or float. The value to set self.x to.
                y -- An int or float. The value to set self.y to.
                width -- An int or float. The value to set self.width to.
                height -- An int or float. The value to set self.height to.
                angle -- An int or float. The value to set self.angle to.
                color -- A string containing a color to set self.color to. Must
                  be Bokeh compatible.
                line_width -- An int or float. The value to set
                  self.line_width to.
                """
                self.x = x
                self.y = y
                self.width = width
                self.height = height
                self.angle = angle
                self.color = color
                self.line_width = line_width
            #</editor-fold>
        #</editor-fold>
    #</editor-fold>

    #<editor-fold _BallConfigs:
    class _BallConfigs:
        """A class used to configure the glyph of a ball within the main game
        figure.


        Attributes:
        x -- An int or float. The x coordinate to use for the ball's glyph.
        y -- An int or float. The y coordinate to use for the ball's glyph.
        color -- A string containing a color to use for the ball's glyph. Must
          be Bokeh compatible.
        line_width -- An int or float. The line width to use for the
          ball's glyph.
        size -- An int or float. The size to use for the ball's glyph.
        """
        def __init__(self, x, y, color, line_width, size):
            """Initialize for the private inner class _BallConfigs. Creates a
            _BallConfigs object with the input values from the arguments.


            Arguments:
            x -- An int or float. The value to set self.x to.
            y -- An int or float. The value to set self.y to.
            color -- A string containing a color to set self.color to. Must be
              Bokeh compatible
            line_width -- An int or float. The value to set self.line_width to.
            size -- An int or float. The value to set self.size to.
            """
            self.x = x
            self.y = y
            self.color = color
            self.line_width = line_width
            self.size = size
    #</editor-fold>
#</editor-fold>

#<editor-fold create():
def create(game_parts, configs):
    """Creates the main game figure according to the passed in Configs object's
    attributes. Also draws the necessary lines and shapes for the main game
    figure, and adds any necessary parts into game_parts.


    Arguments:
    game_parts -- The penalty_kick_automated_game._GameParts object being used
      to collect the game components.
    configs -- The Configs object being used to configure the figure.
    """

    fig = fig_creation.make_fig(configs.main_fig)

    for line_set in configs.penalty_box_line_sets:
        fig.line(
            x=line_set.xs, y=line_set.ys, color=line_set.color,
            alpha=line_set.alpha, line_width=line_set.width
        )
    fig.line(
        x=configs.goal_lines.xs, y=configs.goal_lines.ys,
        color=configs.goal_lines.color, alpha=configs.goal_lines.alpha,
        line_width=configs.goal_lines.width
    )

    fig.quadratic(
        x0=configs.penalty_arc.x0, y0=configs.penalty_arc.y0,
        x1=configs.penalty_arc.x1, y1=configs.penalty_arc.y1,
        cx=configs.penalty_arc.cx, cy=configs.penalty_arc.cy,
        color=configs.penalty_arc.color, alpha =configs.penalty_arc.alpha,
        line_width=configs.penalty_arc.line_width
    )

    keeper_head = Circle(
        x=configs.keeper.head.x, y=configs.keeper.head.y,
        fill_color=configs.keeper.head.color,
        line_width=configs.keeper.head.line_width, size=configs.keeper.head.size
    )
    keeper_body = Rect(
        x=configs.keeper.body.x, y=configs.keeper.body.y,
        width=configs.keeper.body.width, height=configs.keeper.body.height,
        angle=configs.keeper.body.angle, fill_color=configs.keeper.body.color,
        line_width=configs.keeper.body.line_width
    )

    ball = Circle(
        x=configs.ball.x, y=configs.ball.y, fill_color=configs.ball.color,
        line_width=configs.ball.line_width, size=configs.ball.size
    )

    striker_head=Circle(
        x=configs.striker.head.x, y=configs.striker.head.y,
        fill_color=configs.striker.head.color,
        line_width=configs.striker.head.line_width,
        size=configs.striker.head.size
    )
    striker_body = Rect(
        x=configs.striker.body.x, y=configs.striker.body.y,
        width=configs.striker.body.width, height=configs.striker.body.height,
        angle=configs.striker.body.angle, fill_color=configs.striker.body.color,
        line_width=configs.striker.body.line_width
    )

    fig.add_glyph(keeper_head)
    fig.add_glyph(keeper_body)
    fig.add_glyph(ball)
    fig.add_glyph(striker_head)
    fig.add_glyph(striker_body)

    game_parts.figures["game_figure"] = fig
    game_parts.glyphs["goalie_head"] = keeper_head
    game_parts.glyphs["goalie_body"] = keeper_body
    game_parts.glyphs['ball'] = ball
#</editor-fold>
