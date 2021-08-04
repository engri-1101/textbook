from bokeh.plotting import figure

#<editor-fold FigureConfigs:
class FigureConfigs():
    #<editor-fold __init__():
    def __init__(self,
        base_tools, toolbar_loc, toolbar_sticky, title, width, height,
        x_range, y_range, visibility, sizing_mode, outline_line_color,
        background_color, title_font_size, x_axis_visibility, y_axis_visibility,
        x_axis_line_color, y_axis_line_color, x_grid_visibility,
        y_grid_visibility, x_grid_line_color, y_grid_line_color
    ):
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
    fig = figure(
        tools=fig_configs.base_tools, toolbar_location=fig_configs.toolbar_loc,
        toolbar_sticky=fig_configs.toolbar_sticky, title=fig_configs.title,
        plot_width=fig_configs.width, plot_height=fig_configs.height,
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
