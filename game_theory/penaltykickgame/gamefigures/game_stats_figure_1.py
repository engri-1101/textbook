from . import figure_creation as fig_creation
from bokeh.models import (CustomJSHover, ColumnDataSource, CustomJSTransform,
                          HoverTool, Legend)
from bokeh.transform import transform

# FILE-WIDE CONSTANT USED TO ITERATE THROUGH BAR SECTION NAMES:
BAR_NAMES = ["scored", "blockedl", "blockedm", "blockedr"]

#<editor-fold bar_ws_code():
def bar_ws_code(bar_name, bar_width):
    """A function for creating the JavaScript code strings for getting the
    proper widths for the bars.


    Arguments:
    bar_name -- A string containing the name of the bar section in question.
      Must be in BAR_NAMES.
    bar_width -- A float containing the default width to use for the bar
      section. Must be between 0 and 1.

    Returns:
    string -- A code string that when provided with the data column
      'hovered_widths' returns the proper width of the bar section specified by
      bar_name.
    """
    bar_value = str(BAR_NAMES.index(bar_name) + 1)

    codeString = """
const newXs = xs.map(
  (v) => ((v === """ + bar_value + """) ? 1 : """ + str(bar_width) + """)
)
return newXs;
"""
    return codeString
#</editor-fold>

#<editor-fold bar_cs_code():
def bar_cs_code(bar_name):
    """A function for creating the JavaScript code strings for getting the
    proper centers for the bars.


    Argument:
    bar_name -- A string containing the name of the bar section in question.
      Must be in BAR_NAMES.


    Returns:
    string -- A code string that when provided with the source of the figure,
    uses the data for the relevant bar section(bar setion refered to by
    bar_name) and all bar sections below it to calculate the correct
    y-coordinates for the relevant bar section.
    """
    bar_value = BAR_NAMES.index(bar_name) - 1
    calcNewXs = "newXs[i] = v/2"
    src_dats = [
        """ + src.data["scored_y"][i]""", """ + src.data["blockedl_y"][i]""",
        """ + src.data["blockedm_y"][i]""", """ + src.data["blockedr_y"][i]"""
    ]

    while(bar_value >= 0):
        calcNewXs += src_dats[bar_value]
        bar_value -= 1

    #Create and return the full code string:
    codeString = """
const newXs = new Array(xs.length);
xs.forEach(
  (v, i) => """ + calcNewXs + """
);
return newXs;
"""
    return codeString
#</editor-fold>

#<editor-fold xs code string:
# Returns a string representing the Kicker Footedness, Kicker Kick direction pair
xsCode = """
const kfkks = ['(L, L)', '(L, M)', '(L, R)', '(R, L)', '(R, M)', '(R, R)'];
return kfkks[special_vars.index];
"""
#</editor-fold>

#<editor-fold Bar height code string:
# Updates the 'hovered_widths' data column to indicate the hovered bar section,
# and returns the height of the hovered section.
barHeightCode = """
const barTypes = ['Scored', 'Blocked Left', 'Blocked Middle', 'Blocked Right'];
const columns = ['scored_y', 'blockedl_y', 'blockedm_y', 'blockedr_y'];
const wCodes = [1, 2, 3, 4];
const data = src.data;
const index = special_vars.index;
const selected = barTypes.indexOf(special_vars.name);

data['hovered_widths'].fill(0);
data['hovered_widths'][index] = wCodes[selected];
src.change.emit();

const val = data[columns[selected]][index];
return val.toString();
"""
#</editor-fold>

#<editor-fold Custom HoverTool tooltip code string:
# Code below is for how the custom HoverTool displays the information.
# Note: some of the columns used by the hovertool don't need to actually be
# those columns (scored_y, blockedl_y). They were used because the hovertool
# needs an actual column in the src.
custom_tooltip = """
<div>
  <font size="1pt"><p>Kicker (Foot, Kick): @x{custom}<br>
Hovered Bar: $name<br>
Bar Height: @blockedl_y{custom}</p></font>
</div>
"""
#</editor-fold>

#<editor-fold Configs:
class Configs:
    """A class used to configure Stats Figure 1.


    Attributes:
    fig -- The fig_creation.FigureConfigs object being used to configure the
      main figure.
    bars -- A list of _BarConfig objects being used to configure the bar
      sections within the figure.
    legs -- A list of _LegConfig objects being used to configure the legends
      within the figure.
    hitbox_alpha -- An int or float between 0 and 1 used to set the alphas of
      the plot's hitboxes.


    Inner Classes:
    _BarConfigs -- A class for configuring the bar sections within the plot.
    _LegConfigs -- A class for configuring the legends within the plot.
    """
    #<editor-fold __init__():
    leg_default_item_texts = [
        ["Scored", "Goalie Blocked By Going Left"],
        ["Goalie Blocked By Going Middle", "Goalie Blocked By Going Right"]
    ]
    def __init__(
        self, fig_base_tools="", fig_toolbar_loc=None, fig_toolbar_sticky=False,
        fig_title="Shot Status Statistics", fig_width=600, fig_height=360,
        fig_x_range=(0, 6), fig_y_range=(0, 50), fig_visibility=False,
        fig_sizing_mode="stretch_both", fig_outline_line_color=None,
        fig_background_color="white", fig_title_font_size="16pt",
        fig_x_axis_visibility=False, fig_y_axis_visibility=True,
        fig_x_axis_line_color="black", fig_y_axis_line_color="black",
        fig_x_grid_visibility=False, fig_y_grid_visibility=False,
        fig_x_grid_line_color="black", fig_y_grid_line_color="black",
        bar_colors=["#3F6750", "#64A580", "#8AD3AA", "#CBEBD9"],
        bar_widths=[0.8, 0.8, 0.8, 0.8], leg_widths=[308, 464], leg_ys=[20, 40],
        leg_item_texts=leg_default_item_texts, leg_font_size="10pt",
        leg_label_height=10, leg_padding=0, leg_border_alpha=0,
        leg_background_alpha=0, hitbox_alpha=0
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
        bar_colors -- A list of strings containing the colors to use for each of
          the figure's bar sections. Must be Bokeh compatible.
        bar_widths -- A list of floats between 0 and 1, containing the widths to
          use for bar sections not being hovered.
        leg_widths -- A list of ints to use as the widths of the legends.
        leg_ys -- A list of ints to use as the y coordinates of the legends.
        leg_item_texts -- A list of strings containing the texts for the legends
          to use to describe the bar sections.
        leg_font_size -- A string containing the font size to use for
          the legends.
        leg_label_height -- An int to use as the height for the labels of
          the legends.
        leg_padding -- An int to use for the padding on the legends.
        leg_border_alpha -- An int or float between 0 and 1 to use as the alpha
          of the legend borders.
        leg_background_alpha -- An int or float between 0 and 1 to use as the
          alpha of the legend backgrounds.
        hitbox_alpha -- An int or float between 0 and 1 to use as the alpha of
          the hitboxes.
        """
        self.fig = fig_creation.FigureConfigs(
            fig_base_tools, fig_toolbar_loc, fig_toolbar_sticky, fig_title,
            fig_width, fig_height, fig_x_range, fig_y_range, fig_visibility,
            fig_sizing_mode, fig_outline_line_color, fig_background_color,
            fig_title_font_size, fig_x_axis_visibility, fig_y_axis_visibility,
            fig_x_axis_line_color, fig_y_axis_line_color, fig_x_grid_visibility,
            fig_y_grid_visibility, fig_x_grid_line_color, fig_y_grid_line_color
        )
        self.bars=[]
        for i in range(len(bar_colors)):
            bar=self._BarConfig(bar_colors[i], bar_widths[i])
            self.bars.append(bar)

        self.legs=[]
        for i in range(len(leg_widths)):
            leg=self._LegConfig(
                leg_widths[i], leg_ys[i], leg_item_texts[i], leg_font_size,
                leg_label_height, leg_padding, leg_border_alpha,
                leg_background_alpha
            )
            self.legs.append(leg)

        self.hitbox_alpha = hitbox_alpha
    #</editor-fold>

    #<editor-fold _BarConfig:
    class _BarConfig:
        """A class for configuring the bar sections within the plot.


        Attributes:
            color -- A string containing the color to use for the bar section.
              Must be Bokeh compatible.
            width -- An int or float between 0 and 1, to use as the width of the
              bars within section when not being hovered.
        """
        #<editor-fold __init__():
        def __init__(self, color, width):
            """Initializer for the class _BarConfigs. Creates a _BarConfigs
            object with the input values from the arguments.


            Arguments:
            color -- A string containing the color to set self.color to. Must be
              Bokeh compatible.
            width -- An int or float between 0 and 1 to set self.width to.
            """
            self.color = color
            self.width = width
        #</editor-fold>
    #</editor-fold>

    #<editor-fold _LegConfig:
    class _LegConfig:
        """A class for configuring the legends within the plot.


        Attributes:
        width -- An int or float between 0 and 1, to use as the width
          of the legend.
        y -- An int to use as the y coordinate of the legend.
        item_texts -- A list of strings containing the text to use as the labels
          for the legend items.
        font_size -- A string containing the font size to use for the legend
          labels. Must be Bokeh compatible.
        label_height -- An int to use as the height of the legend label.
        padding -- An int to use as the padding of the label.
        border_alpha -- An int or float between 0 and 1 to use as the alpha of
          the legend border.
        background_alpha -- An int or float between 0 and 1 to use as the alpha
          of the legend background.
        """
        #<editor-fold __init__():
        def __init__(
            self, width, y, item_texts, font_size, label_height, padding,
            border_alpha, background_alpha
        ):
            """Initializer for the class _BarConfigs. Creates a _BarConfigs
            object with the input values from the arguments.


            Attributes:
            width -- An int or float between 0 and 1, to use for self.width.
            y -- An int to use for self.y
            item_texts -- A list of strings containing text to use
              for self.item_texts
            font_size -- A string containing a font size to set self.font_size
              to. Must be Bokeh compatible.
            label_height -- An int to set self.label_height to.
            padding -- An int to set self.padding to.
            border_alpha -- An int or float between 0 and 1 to set
              self.border_alpha to.
            background_alpha -- An int or float between 0 and 1 to set
              self.background_alpha to.
            """
            self.width = width
            self.y = y
            self.item_texts=item_texts
            self.font_size = font_size
            self.label_height = label_height
            self.padding = padding
            self.border_alpha = border_alpha
            self.background_alpha = background_alpha
        #</editor-fold>
    #</editor-fold>
#</editor-fold>

#<editor-fold create():
def create(game_parts, configs):
    """Creates Game Stats Figure 1 according to the passed in Configs object's
    attributes. Also creates Game Stats Figure 1's ColumnDataSource. Game Stats
    Figure 1 is then fully set up, before both the figure and its source are
    added to the passed in _GameParts object being used to collect the game
    components.


    Arguments:
    game_parts -- The penalty_kick_automated_game._GameParts object being used
      to collect the game components.
    configs -- The Configs object being used to configure the figure.
    """
    fig = fig_creation.make_fig(configs.fig)

    #<editor-fold Create Legend:
    #Add shapes to represent colors (Cannot be seen as radius=0):
    color_circles = []
    for bar in configs.bars:
        color_circle = fig.circle(x=0, y=0, radius=0, color=bar.color)
        color_circles.append(color_circle)

    #Create legends and add them to the layout:
    for i in range(len(configs.legs)):
        leg=configs.legs[i]
        items = []
        for j in range(len(leg.item_texts)):
            items.append(
                (leg.item_texts[j], [color_circles[len(leg.item_texts)*i + j]])
            )
        loc=(int((configs.fig.width-leg.width) / 2), leg.y)
        legend = Legend(
            items=items, orientation="horizontal", location=loc,
            label_text_font_size=leg.font_size, label_height=leg.label_height,
            padding=leg.padding, border_line_alpha=leg.border_alpha,
            background_fill_alpha=leg.background_alpha
        )
        fig.add_layout(legend, "below")
    #</editor-fold>

    #<editor-fold ColumnDataSource Creation:
    src_data = {
        "x" : [0.5, 1.5, 2.5, 3.5, 4.5, 5.5],
        "scored_y" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "blockedl_y" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "blockedm_y" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "blockedr_y" : [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "hovered_widths" : ["", "", "", "", "", ""]
    }
    fig_src = ColumnDataSource(src_data)
    #</editor-fold>

    #<editor-fold CustomJSTransform Creation:
    args_dict = {"src" : fig_src}

    gcs = []
    gws = []
    for i in range(4):
        gc = CustomJSTransform(
            v_func=bar_cs_code(BAR_NAMES[i]), args=args_dict
        )
        gw = CustomJSTransform(
            v_func=bar_ws_code(BAR_NAMES[i], configs.bars[i].width)
        )
        gcs.append(gc)
        gws.append(gw)
    #</editor-fold>

    #<editor-fold Plot Figure Elements:
    hb_ids = ["scored_y", "blockedl_y", "blockedm_y", "blockedr_y"]
    hb_names = ["Scored", "Blocked Left", "Blocked Middle", "Blocked Right"]

    hbs = []
    bars = []
    for i in range(4):
        hb = fig.rect(
            x="x", y=transform(hb_ids[i], gcs[i]), source=fig_src, width=1,
            height=hb_ids[i], alpha=configs.hitbox_alpha, fill_alpha=0,
            name=hb_names[i], color=configs.bars[i].color
        )
        bar = fig.rect(
            x="x", y=transform(hb_ids[i], gcs[i]), source=fig_src,
            width=transform("hovered_widths", gws[i]), height=hb_ids[i],
            color=configs.bars[i].color
        )
        hbs.append(hb)
        bars.append(bar)
    #</editor-fold>

    #<editor-fold Create HoverTool:
    xs_custom = CustomJSHover(code=xsCode)
    height_custom = CustomJSHover(code=barHeightCode, args={"src" : fig_src})
    hovertool_formatters = {"@x" : xs_custom, "@blockedl_y" : height_custom}
    hover_tool = HoverTool(
        tooltips=custom_tooltip, formatters=hovertool_formatters,
        mode="mouse", point_policy="follow_mouse", renderers=hbs
    )
    fig.add_tools(hover_tool)
    #</editor-fold>

    game_parts.figures["stats_1"] = fig
    game_parts.sources["stats_fig_1"] = fig_src
 #</editor-fold>
