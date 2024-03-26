"""plot_helpers provides functions that take care of plotting the
contours for the xti model"""
import numpy as np
import matplotlib.pyplot as plt


def format_func(value, tick_number):
    # find number of multiples of 180 degrees
    N = int(np.round(2 * value / 180))
    if N == 0:
        return "0"
    elif N == 1:
        return "Equator 90"
    elif N == 2:
        return "180"
    elif N == 3:
        return "Equator 270"
    else:
        return value


def contour_figure(formation, formation_index, data, fig_param, plot_param=None):
    """
    A helper function to make a the 4 by 4 contour figures

    Parameters
    ----------
    formation : namedtuple
        tuple with information from the formation needed for the
        plots. dae, a, and domega.

    formation_index : tuple
        the formation index to use

    data : list
        first item is x data, second is y data, third is z data

    fig_param : dict
       Dictionary of kwargs to pass to plt.subplots

    plot_param: dict
       contour key contains a dictionary of parameters passed to contour_plotter as cotour_param and key axes as axes_param

    Returns
    -------
    matplotlib.figure.Figure
        the figure
    """
    if plot_param is None:
        plot_param = {}
        plot_param["contour"] = {
            "cmap": "seismic",
        }
        plot_param["axes"] = {
            "add_title": True,
            "title": None,
            "add_xlabel": None,
            "xlabel": "Incident angle /°",
            "add_ylabel": None,
            "ylabel": "Mean argument of latitude /°",
            "y_major_locator": plt.MultipleLocator(180 / 2),
            "y_minor_locator": plt.MultipleLocator(180 / 2),
        }

    contour_params = plot_param["contour"]
    axes_params = plot_param["axes"]
    colorbar_params = plot_param["colorbar"]
    yaxis_formatter = plot_param["yaxis_formatter"]

    fig, axs = plt.subplots(2, 2, **fig_param)
    xlabel_sequence = (False, False, True, True)
    ylabel_sequence = (True, False, True, False)

    for i, (ax, (add_xlabel, add_ylabel)) in enumerate(
        zip(axs.flatten(), zip(xlabel_sequence, ylabel_sequence))
    ):
        title = create_plot_title(formation, formation_index[i])
        z = data[2][:, :, formation_index[i]]
        axes_params["title"] = title
        axes_params["add_xlabel"] = add_xlabel
        axes_params["add_ylabel"] = add_ylabel
        cf = contour_plotter(
            ax, (data[0], data[1], z), contour_params, axes_params, yaxis_formatter
        )
        fig.colorbar(cf, ax=ax, **colorbar_params)
    return fig


def contour_plotter(ax, data, contour_param, axes_param, formatter=None):
    """
    A helper function to make a the contour plots of the uncertainty

    Parameters
    ----------
    ax : Axes
        The axes to draw to

    data : list
       first item is x data, second is y data, third is z data

    conrour_param : dict
       Dictionary of kwargs to pass to ax.contourf

    axes_param : dict
       Dictionary of axes and title parameters

    formatter: plt.FuncFormatter
        y-axis major formatter function (Default value = None)

    Returns
    -------
    out : tuple
        list of artists added
    """
    out = ax.contourf(data[0], data[1], data[2], **contour_param)
    if axes_param["add_title"]:
        ax.set_title(axes_param["title"])
    if axes_param["add_xlabel"]:
        ax.set_xlabel(axes_param["xlabel"])
    if axes_param["add_ylabel"]:
        ax.set_ylabel(axes_param["ylabel"])
        if "y_major_locator" in axes_param:
            ax.yaxis.set_major_locator(axes_param["y_major_locator"])
            if formatter:
                ax.yaxis.set_major_formatter(plt.FuncFormatter(formatter))
        if "y_minor_locator" in axes_param:
            ax.yaxis.set_minor_locator(axes_param["y_minor_locator"])

    return out


def create_plot_title(formation, index, format_dae=".0f", format_domega="03,.0f"):
    """
    A function to create the title for the uncertainty plots based on the index of the formation parameters.
    
     Parameters
    ----------
    formation : namedtuple
        namedtuple with information from the formation needed for the
        plots. dae, a, and domega.

    index : int
        The time index (days) of the formation parameters to include in the title

    fromat_dae : str
        The dae string format specifier (Default value = ".0f")

    fromat_domega : str
        The domega * a string format specifier (Default value = "03,.0f")
        
    Returns
    -------
    title : str
        the rendered title
    """
    title = (
        r"$a\Delta e =$ "
        + f"{formation.dae[index] :{format_dae}}"
        + r"$\si{\m}$, "
        + r"$a\Delta\Omega  =$ "
        + f"{np.radians(formation.domega)[index] * formation.a :{format_domega}}"
        + r"$\si{\m}$"
    )
    return title
