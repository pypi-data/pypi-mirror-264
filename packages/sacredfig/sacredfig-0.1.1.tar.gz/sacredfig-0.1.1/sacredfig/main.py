import string

import matplotlib.pyplot as plt
import matplotlib.transforms as mtrans


# Convert centimeters to inches
cm2in = 1 / 2.54


def add_labels_to_axes(fig: plt.Figure, axes: list[plt.Axes], fontsize: int = 9, Δx: float = -0.25, Δy: float = 0.1) -> None:
    """Add bold numbers (A, B, C, etc.) on the top left of every matplotlib axis."""

    for n, ax in enumerate(axes):
        trans_offset = mtrans.offset_copy(ax.transAxes, fig=fig, x=Δx, y=Δy, units="inches")
        ax.text(
            0,
            1,
            string.ascii_lowercase[n] + ".",
            fontweight=500,
            transform=trans_offset,
            size=fontsize,
        )


def restyle_axis(ax: plt.Axes, *, lineprops: dict = {}, artistprops: dict = {}) -> None:
    if lineprops:
        plt.setp(ax.lines, **lineprops)

    if artistprops:
        plt.setp(ax.artists, **artistprops)


# See <https://matplotlib.org/stable/tutorials/introductory/customizing.html> for all
# possible rcParams.
style = {
    # Lines
    "lines.linewidth": 1.0,  # line width in points
    "lines.linestyle": "-",  # solid line
    "lines.color": "b",  # has no affect on plot(); see axes.prop_cycle
    "lines.marker": "",  # the default marker
    "lines.markerfacecolor": "auto",  # the default markerfacecolor
    "lines.markeredgecolor": "auto",  # the default markeredgecolor
    "lines.markeredgewidth": 0.5,  # the line width around the marker symbol
    "lines.markersize": 6,  # markersize, in points
    "lines.dash_joinstyle": "round",  # miter|round|bevel
    "lines.dash_capstyle": "butt",  # butt|round|projecting
    "lines.solid_joinstyle": "round",  # miter|round|bevel
    "lines.solid_capstyle": "projecting",  # butt|round|projecting
    "lines.antialiased": True,  # render lines in antialiased (no jaggies)
    "lines.dashed_pattern": (6, 6),
    "lines.dashdot_pattern": (3, 5, 1, 5),
    "lines.dotted_pattern": (1, 3),
    "lines.scale_dashes": False,
    # Axes
    "axes.linewidth": 0.5,
    "axes.grid": True,
    "axes.titlesize": 7,
    "axes.labelpad": 2,
    "axes.labelsize": 7,
    ## Main tick parameters
    "xtick.labelsize": 5,
    "xtick.direction": "in",
    "ytick.labelsize": "5",
    "ytick.direction": "in",
    ## Major and minor ticks
    "xtick.major.width": 0.2,
    "xtick.major.size": 4,
    "xtick.major.pad": 2.5,
    "ytick.major.width": 0.2,
    "ytick.major.size": 4,
    "ytick.major.pad": 2.5,
    "xtick.minor.width": 0.1,
    "xtick.minor.size": 2,
    "xtick.minor.pad": 2.5,
    "ytick.minor.width": 0.1,
    "ytick.minor.size": 2,
    "ytick.minor.pad": 2.5,
    # Grid
    "grid.color": "#999999",
    "grid.linestyle": "-",
    "grid.linewidth": 0.1,
    # Remove legend frame
    "legend.frameon": False,
    # Typography
    "font.weight": "regular",
    "font.size": 7,
    "font.family": "sans-serif",
    "font.serif": "PT Serif, DejaVu Serif, New Century Schoolbook, Century Schoolbook L, Utopia, ITC Bookman, Bookman, Nimbus Roman No9 L, Times New Roman, Times, Palatino, Charter, serif",
    "font.sans-serif": "Source Sans Pro, DejaVu Sans, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, Avant Garde, sans-serif",
    "font.cursive": "Apple Chancery, Textile, Zapf Chancery, Sand, Script MT, Felipa, cursive",
    "font.fantasy": "Comic Sans MS, Chicago, Charcoal, ImpactWestern, Humor Sans, fantasy",
    "font.monospace": "DejaVu Sans Mono, Andale Mono, Nimbus Mono L, Courier New, Courier, Fixed, Terminal, monospace",
    ## Math fonts
    "mathtext.fontset": "custom",
    "mathtext.cal": "cursive",
    "mathtext.rm": "sans",
    "mathtext.tt": "monospace",
    "mathtext.it": "sans:italic",
    "mathtext.bf": "sans:bold",
    "mathtext.sf": "sans:serif",
    # Boxplots
    "boxplot.notch": False,
    "boxplot.vertical": True,
    "boxplot.whiskers": 1.5,
    "boxplot.bootstrap": None,
    "boxplot.patchartist": False,
    "boxplot.showmeans": False,
    "boxplot.showcaps": True,
    "boxplot.showbox": True,
    "boxplot.showfliers": True,
    "boxplot.meanline": False,
    "boxplot.flierprops.color": "black",
    "boxplot.flierprops.marker": "o",
    "boxplot.flierprops.markerfacecolor": "none",
    "boxplot.flierprops.markeredgecolor": "black",
    "boxplot.flierprops.markeredgewidth": 0.5,
    "boxplot.flierprops.markersize": 2,
    "boxplot.flierprops.linestyle": "none",
    "boxplot.flierprops.linewidth": 1.0,
    "boxplot.boxprops.color": "black",
    "boxplot.boxprops.linewidth": 0.5,
    "boxplot.boxprops.linestyle": "-",
    "boxplot.whiskerprops.color": "black",
    "boxplot.whiskerprops.linewidth": 0.5,
    "boxplot.whiskerprops.linestyle": "-",
    "boxplot.capprops.color": "black",
    "boxplot.capprops.linewidth": 0.5,
    "boxplot.capprops.linestyle": "-",
    "boxplot.medianprops.color": "black",
    "boxplot.medianprops.linewidth": 0.5,
    "boxplot.medianprops.linestyle": "-",
    "boxplot.meanprops.color": "C2",
    "boxplot.meanprops.marker": "^",
    "boxplot.meanprops.markerfacecolor": "C2",
    "boxplot.meanprops.markeredgecolor": "C2",
    "boxplot.meanprops.markersize": 6,
    "boxplot.meanprops.linestyle": "--",
    "boxplot.meanprops.linewidth": 1.0,
}
