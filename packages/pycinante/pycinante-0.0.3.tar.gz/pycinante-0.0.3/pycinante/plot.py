"""This module provides functions to plotting convincingly.
"""
from __future__ import annotations
from matplotlib import pyplot as plt
from matplotlib_inline import backend_inline
from typing import Union, Tuple
from pycinante.list import listify
from pycinante.system import is_on_ipython
from pycinante.validator import check_condition

try:
    # noinspection PyUnresolvedReferences
    from IPython import display
except ImportError:
    pass

__all__ = [
    'use_svg_display',
    'use_chinese_display',
    'plot',
    'plt',
    'Animator'
]

def use_svg_display() -> None:
    """Use the svg format to display a plot in Python."""
    backend_inline.set_matplotlib_formats('svg')

def use_chinese_display() -> None:
    """Set matplotlib to support Chinese font display."""
    plt.rcParams['font.sans-serif'] = ['SimSun', 'Songti SC']
    plt.rcParams['axes.unicode_minus'] = False

def set_figsize(figsize: tuple[float, float] = (3.5, 2.5)) -> None:
    """Set the figure size for matplotlib."""
    plt.rcParams['figure.figsize'] = figsize

def set_axes(
    axes: plt.Axes,
    xlabel: str,
    ylabel: str,
    xlim: float | tuple[float, float],
    ylim: float | tuple[float, float],
    xscale: str,
    yscale: str,
    legend: tuple[str]
) -> None:
    """Set the axes for matplotlib."""
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)
    axes.set_xscale(xscale)
    axes.set_yscale(yscale)
    axes.set_xlim(*listify(xlim))
    axes.set_ylim(*listify(ylim))
    if legend:
        axes.legend(legend)
    axes.grid()

# noinspection PyUnresolvedReferences
def plot(
    X: Union[list, 'np.ndarray', 'torch.Tensor'],
    Y: Union[list, 'np.ndarray', 'torch.Tensor', None] = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    legend: Tuple[str] | None = None,
    xlim: float | tuple[float, float] | None = None,
    ylim: float | tuple[float, float] | None = None,
    xscale: str = 'linear',
    yscale: str = 'linear',
    fmts: tuple[str] = ('-', 'm--', 'g-.', 'r:'),
    figsize: tuple[float, float] = (3.5, 2.5),
    axes: plt.Axes | None = None
) -> None:
    """Plot data points."""
    legend = legend or []
    set_figsize(figsize)
    axes = axes if axes else plt.gca()

    def has_one_axis(X):
        """Return True if `X` (tensor or list) has 1 axis"""
        return (hasattr(X, "ndim") and X.ndim == 1 or isinstance(X, list)
                and not hasattr(X[0], "__len__"))

    if has_one_axis(X):
        X = [X]
    if Y is None:
        X, Y = [[]] * len(X), X
    elif has_one_axis(Y):
        Y = [Y]
    if len(X) != len(Y):
        X = X * len(Y)
    axes.cla()
    for x, y, fmt in zip(X, Y, fmts):
        if len(x):
            axes.plot(x, y, fmt)
        else:
            axes.plot(y, fmt)
    set_axes(axes, xlabel, ylabel, xlim, ylim, xscale, yscale, legend)

class Animator:
    """For plotting data in animation. Ref: https://pypi.org/project/d2l/.
    """

    @check_condition(is_on_ipython, 'a animator must be run in a notebook')
    def __init__(
        self,
        xlabel: str = None,
        ylabel: str = None,
        legend: tuple[str] = None,
        xlim: float | tuple[float, float] | None = None,
        ylim: float | tuple[float, float] | None = None,
        xscale: str = 'linear',
        yscale: str = 'linear',
        fmts: tuple[str] = ('-', 'm--', 'g-.', 'r:'),
        nrows: int = 1,
        ncols: int = 1,
        figsize: tuple[float, float] = (3.5, 2.5)
    ) -> None:
        legend = legend or []
        backend_inline.set_matplotlib_formats('svg')
        self.fig, self.axes = plt.subplots(nrows, ncols, figsize=figsize)
        self.axes = (nrows * ncols == 1 and [self.axes, ]) or self.axes
        # Use a lambda function to capture arguments
        self.config_axes = lambda: set_axes(
            self.axes[0], xlabel, ylabel, xlim, ylim, xscale, yscale, legend)
        self.X, self.Y, self.fmts = None, None, fmts

    # noinspection PyUnresolvedReferences
    def add(
        self,
        x: Union[float, list[float], 'np.ndarray', 'torch.Tensor'],
        y: Union[float, list[float], 'np.ndarray', 'torch.Tensor']
    ) -> None:
        """Add multiple data points into the figure."""
        y = (not hasattr(y, '__len__') and [y]) or y
        n = len(y)
        x = (not hasattr(x, '__len__') and [x] * n) or x
        self.X = self.X or [[] for _ in range(n)]
        self.Y = self.Y or [[] for _ in range(n)]
        for i, (a, b) in enumerate(zip(x, y)):
            if a is not None and b is not None:
                self.X[i].append(a)
                self.Y[i].append(b)
        self.axes[0].cla()
        for x, y, fmt in zip(self.X, self.Y, self.fmts):
            self.axes[0].plot(x, y, fmt)
        self.config_axes()
        display.display(self.fig)
        display.clear_output(wait=True)
