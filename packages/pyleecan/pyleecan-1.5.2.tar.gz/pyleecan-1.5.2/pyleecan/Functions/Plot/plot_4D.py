from SciDataTool.Functions.Plot.plot_4D import plot_4D as plot_4D_fct
from ...definitions import config_dict

# Import values from config dict
COLOR_LIST = config_dict["PLOT"]["COLOR_DICT"]["COLOR_LIST"]
COLORMAP = config_dict["PLOT"]["COLOR_DICT"]["COLOR_MAP"]
FONT_NAME = config_dict["PLOT"]["FONT_NAME"]
FONT_SIZE_TITLE = config_dict["PLOT"]["FONT_SIZE_TITLE"]
FONT_SIZE_LABEL = config_dict["PLOT"]["FONT_SIZE_LABEL"]
FONT_SIZE_LEGEND = config_dict["PLOT"]["FONT_SIZE_LEGEND"]


def plot_4D(
    Xdata,
    Ydata,
    Zdata,
    Sdata=None,
    is_same_size=False,
    x_min=None,
    x_max=None,
    y_min=None,
    y_max=None,
    z_min=None,
    z_max=None,
    title="",
    xlabel="",
    ylabel="",
    zlabel="",
    xticks=None,
    yticks=None,
    xticklabels=None,
    yticklabels=None,
    annotations=None,
    color_list=None,
    colormap=None,
    fig=None,
    ax=None,
    is_logscale_x=False,
    is_logscale_y=False,
    is_logscale_z=False,
    is_disp_title=True,
    type_plot="scatter",
    save_path=None,
    is_show_fig=None,
    is_switch_axes=False,
    win_title=None,
    is_grid=False,
):
    """Plots a 4D graph

    Parameters
    ----------
    Xdata : ndarray
        array of x-axis values
    Ydata : ndarray
        array of y-axis values
    Zdata : ndarray
        array of z-axis values
    Sdata : ndarray
        array of 4th axis values
    is_same_size : bool
        in scatter plot, all squares are the same size
    colormap : colormap object
        colormap prescribed by user
    x_min : float
        minimum value for the x-axis (no automated scaling in 3D)
    x_max : float
        maximum value for the x-axis (no automated scaling in 3D)
    y_min : float
        minimum value for the y-axis (no automated scaling in 3D)
    y_max : float
        maximum value for the y-axis (no automated scaling in 3D)
    z_min : float
        minimum value for the z-axis (no automated scaling in 3D)
    z_max : float
        maximum value for the z-axis (no automated scaling in 3D)
    title : str
        title of the graph
    xlabel : str
        label for the x-axis
    ylabel : str
        label for the y-axis
    zlabel : str
        label for the z-axis
    xticks : list
        list of ticks to use for the x-axis
    yticks: list
        list of ticks to use for the y-axis
    xticklabels : list
        list of tick labels to use for the x-axis
    yticklabels : list
        list of tick labels to use for the x-axis
    annotations : list
        list of annotations to apply to data
    fig : Matplotlib.figure.Figure
        existing figure to use if None create a new one
    ax : Matplotlib.axes.Axes object
        ax on which to plot the data
    is_logscale_x : bool
        boolean indicating if the x-axis must be set in logarithmic scale
    is_logscale_y : bool
        boolean indicating if the y-axis must be set in logarithmic scale
    is_logscale_z : bool
        boolean indicating if the z-axis must be set in logarithmic scale
    is_disp_title : bool
        boolean indicating if the title must be displayed
    type : str
        type of 3D graph : "stem", "surf", "pcolor" or "scatter"
    save_path : str
        full path including folder, name and extension of the file to save if save_path is not None
    is_show_fig : bool
        True to show figure after plot
    """

    print(
        "WARNING: plot_3D function is deprecated and will be removed from the next release. Please use SciDataTool.Functions.Plot.plot_3D instead."
    )

    if color_list is None:
        color_list = COLOR_LIST
    if colormap is None:
        colormap = COLORMAP

    # Call SciDataTool plot function
    plot_4D_fct(
        Xdata,
        Ydata,
        Zdata,
        Sdata=Sdata,
        is_same_size=is_same_size,
        colormap=colormap,
        x_min=x_min,
        x_max=x_max,
        y_min=y_min,
        y_max=y_max,
        z_min=z_min,
        z_max=z_max,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        zlabel=zlabel,
        xticks=xticks,
        yticks=yticks,
        xticklabels=xticklabels,
        yticklabels=yticklabels,
        annotations=annotations,
        fig=fig,
        ax=ax,
        is_logscale_x=is_logscale_x,
        is_logscale_y=is_logscale_y,
        is_logscale_z=is_logscale_z,
        is_disp_title=is_disp_title,
        type_plot=type_plot,
        save_path=save_path,
        is_show_fig=is_show_fig,
        is_switch_axes=is_switch_axes,
        win_title=win_title,
        font_name=FONT_NAME,
        font_size_title=FONT_SIZE_TITLE,
        font_size_label=FONT_SIZE_LABEL,
        font_size_legend=FONT_SIZE_LEGEND,
        is_grid=is_grid,
    )
