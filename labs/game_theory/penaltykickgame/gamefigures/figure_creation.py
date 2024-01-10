from bokeh.plotting import figure

#<editor-fold FigureConfigs:
class FigureConfigs():
    """A class used to configure a basic Bokeh figure.


    Attributes:
    base_tools -- A string containing the base tools to add to the figure. Must
      be Bokeh compatible.
    toolbar_loc -- A string containing the location to use for the figure
      toolbar. Must be Bokeh compatible.
    toolbar_sticky -- A bool for whether or not to make the figure tool
      bar sticky.
    title -- A string. The title to use for the figure.
    width -- An int. The width to use for the figure.
    height -- An int. The width to use for the figure.
    x_range -- An (int, int) or (float, float) pair containing the x range to
      use for the figure.
    y_range -- An (int, int) or (float, float) pair cointaining the y range to
      use for the figure.
    visibility -- A bool for setting the figure's initial visibility.
    sizing_mode -- A string containing how the figure should be sized. Must be
      Bokeh compatible.
    outline_line_color -- A string containing the color to use for the figure
      outline. Must be Bokeh compatible.
    background_color -- A string containing the color to use for the figure
      background. Must be Bokeh compatible.
    title_font_size -- A string containing the font size to use for the figure
      title. Must be Bokeh compatible.
    x_axis_visibility -- A bool for setting the figure's x axis' visibility.
    y_axis_visibility -- A bool for setting the figure's y axis' visibility.
    x_axis_line_color -- A string containing the color to use for the figure's
      x axis. Must be Bokeh compatible.
    y_axis_line_color -- A string containing the color to use for the figure's
      y axis. Must be Bokeh compatible.
    x_grid_visibility -- A bool for setting the figure's x grid's visibility.
    y_grid_visibility -- A bool for setting the figure's y grid's visibility.
    x_grid_line_color -- A string containing the color to use for the figure's
      x grid. Must be Bokeh compatible.
    y_grid_line_color -- A string containing the color to use for the figure's
      y grid. Must be Bokeh compatible.
    """
    #<editor-fold __init__():
    def __init__(self,
        base_tools, toolbar_loc, toolbar_sticky, title, width, height,
        x_range, y_range, visibility, sizing_mode, outline_line_color,
        background_color, title_font_size, x_axis_visibility, y_axis_visibility,
        x_axis_line_color, y_axis_line_color, x_grid_visibility,
        y_grid_visibility, x_grid_line_color, y_grid_line_color
    ):
        """Initializer for the class FigureConfigs. Creates a FigureConfigs
        object containing the relevant information for creating the figure with
        the input argument values.


        Keyword Arguments:
        base_tools -- A string containing the base tools to set self.base_tools
          to. Must be Bokeh compatible.
        toolbar_loc -- A string containing the location to use to set
          self.toolbar_loc. Must be Bokeh compatible.
        toolbar_sticky -- A bool to set self.toolbar_sticky to.
        title -- A string to set self.title to.
        width -- An int to set self.width to.
        height -- An int to set self.height to.
        x_range -- An (int, int) or (float, float) pair to set self.x_range to.
        y_range -- An (int, int) or (float, float) pair to set self.y_range to.
        visibility -- A bool to set self.visibility to.
        sizing_mode -- A string containing the figure sizing method to set
          self.sizing_mode to. Must be Bokeh compatible.
        outline_line_color -- A string containing the color to set
          self.outline_line_color. Must be Bokeh compatible.
        background_color -- A string containing the color to set
          self.background_color. Must be Bokeh compatible.
        title_font_size -- A string containing the font size to set
          self.title_font_size. Must be Bokeh compatible.
        x_axis_visibility -- A bool to set self.x_axis_visibility to.
        y_axis_visibility -- A bool to set self.y_axis_visibility to.
        x_axis_line_color -- A string containing the color to set
          self.x_axis_line_color to. Must be Bokeh compatible.
        y_axis_line_color -- A string containing the color to set
          self.y_axis_line_color to. Must be Bokeh compatible.
        x_grid_visibility -- A bool to set self.x_grid_visibility to.
        y_grid_visibility -- A bool to set self.y_grid_visibility to.
        x_grid_line_color -- A string containing the color to set
          self.x_grid_line_color to. Must be Bokeh compatible.
        y_grid_line_color -- A string containing the color to set
          self.y_grid_line_color to. Must be Bokeh compatible.
        """
        self.base_tools = base_tools
        self.toolbar_loc = toolbar_loc
        self.toolbar_sticky = toolbar_sticky
        self.title = title
        self.width = width
        self.height = height
        self.x_range = x_range
        self.y_range = y_range
        self.visibility = visibility
        self.sizing_mode = sizing_mode
        self.title_font_size = title_font_size
        self.xaxis_visibility = x_axis_visibility
        self.yaxis_visibility = y_axis_visibility
        self.xaxis_line_color = x_axis_line_color
        self.yaxis_line_color = y_axis_line_color
        self.xgrid_visibility = x_grid_visibility
        self.ygrid_visibility = y_grid_visibility
        self.xgrid_line_color = x_grid_line_color
        self.ygrid_line_color = y_grid_line_color
        self.outline_line_color = outline_line_color
        self.background_color = background_color
    #</editor-fold>
#</editor-fold>

#<editor-fold make_fig():
def make_fig(fig_configs):
    """A function to make a base Bokeh figure off of the passed in FigureConfigs
    object.


    Argument:
    fig_configs -- The FigureConfigs object to use to set the values for the
      figure.


    Returns:
    figure -- A Bokeh figure.
    """
    fig = figure(
        tools=fig_configs.base_tools, toolbar_location=fig_configs.toolbar_loc,
        toolbar_sticky=fig_configs.toolbar_sticky, title=fig_configs.title,
        width=fig_configs.width, height=fig_configs.height,
        x_range=fig_configs.x_range, y_range=fig_configs.y_range,
        visible=fig_configs.visibility, sizing_mode=fig_configs.sizing_mode,
        outline_line_color=fig_configs.outline_line_color,
        background_fill_color=fig_configs.background_color
    )
    fig.title.text_font_size = fig_configs.title_font_size
    fig.xaxis.visible = fig_configs.xaxis_visibility
    fig.yaxis.visible = fig_configs.yaxis_visibility
    fig.xaxis.axis_line_color = fig_configs.xaxis_line_color
    fig.yaxis.axis_line_color =  fig_configs.yaxis_line_color
    fig.xgrid.visible = fig_configs.xgrid_visibility
    fig.ygrid.visible = fig_configs.ygrid_visibility
    fig.xgrid.grid_line_color = fig_configs.xgrid_line_color
    fig.ygrid.grid_line_color = fig_configs.ygrid_line_color

    return fig
#</editor-fold>
