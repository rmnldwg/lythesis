"""
Utility functions for plotting histograms over prevalences.
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import h5py
from matplotlib.axes._axes import Axes as MPLAxes
import numpy as np
import scipy as sp
import scipy.stats


def floor_at_decimal(value: float, decimal: int) -> float:
    """
    Compute the floor of `value` for the specified `decimal`, which is the distance
    to the right of the decimal point. May be negative.
    """
    power = 10**decimal
    return np.floor(power * value) / power

def ceil_at_decimal(value: float, decimal: int) -> float:
    """
    Compute the ceiling of `value` for the specified `decimal`, which is the distance
    to the right of the decimal point. May be negative.
    """
    return - floor_at_decimal(-value, decimal)

def floor_to_step(value: float, step: float) -> float:
    """
    Compute the next closest value on a ladder of stepsize `step` that is below `value`.
    """
    return (value // step) * step

def ceil_to_step(value: float, step: float) -> float:
    """
    Compute the next closest value on a ladder of stepsize `step` that is above `value`.
    """
    return floor_to_step(value, step) + step


def _clean_and_check(filename: Union[str, Path]) -> Path:
    """
    Check if file with `filename` exists. If not, raise error, otherwise return
    cleaned `PosixPath`.
    """
    filepath = Path(filename)
    if not filepath.exists():
        raise FileNotFoundError(
            f"File with the name {filename} does not exist at {filepath.resolve()}"
        )
    return filepath


@dataclass
class Histogram:
    """Class containing data for plotting a histogram."""
    filename: Union[str, Path]
    dataname: str
    scale: float = field(default=100.)
    kwargs: Dict[str, Any] = field(default_factory=lambda: {})

    def __post_init__(self) -> None:
        self.filename = _clean_and_check(self.filename)
        with h5py.File(self.filename, mode="r") as h5file:
            dataset = h5file[self.dataname]
            self.values = self.scale * dataset[:]

    @property
    def min_val(self):
        return np.min(self.values)

    @property
    def max_val(self):
        return np.max(self.values)

@dataclass
class Posterior:
    """Class for storing plot configs for a Beta posterior."""
    filename: Union[str, Path]
    dataname: str
    scale: float = field(default=100.)
    quantile: float = field(default=0.3)
    kwargs: Dict[str, Any] = field(default_factory=lambda: {})

    def __post_init__(self) -> None:
        self.filename = _clean_and_check(self.filename)
        with h5py.File(self.filename, mode="r") as h5file:
            dataset = h5file[self.dataname]
            self.num_success = int(dataset.attrs["num_match"])
            self.num_total = int(dataset.attrs["num_total"])
            self.num_fail = self.num_total - self.num_success

    def pdf(self, x):
        """Compute the probability density function."""
        return sp.stats.beta.pdf(
            x,
            a=self.num_success+1,
            b=self.num_fail+1,
            scale=self.scale
        )

    @property
    def min_val(self):
        return sp.stats.beta.ppf(
            self.quantile,
            a=self.num_success+1,
            b=self.num_fail+1,
            scale=self.scale,
        )

    @property
    def max_val(self):
        return sp.stats.beta.ppf(
            1. - self.quantile,
            a=self.num_success+1,
            b=self.num_fail+1,
            scale=self.scale,
        )

def draw(
    axes: MPLAxes,
    contents: List[Union[Histogram, Posterior]],
    xlim: Optional[list] = None,
    hist_kwargs: Optional[Dict[str, Any]] = None,
    plot_kwargs: Optional[Dict[str, Any]] = None,
) -> MPLAxes:
    """
    Draw histograms and Beta posterior from `contents` into `axes`.
    
    The `hist_kwargs` define general settings that will be applied to all histograms.
    Similarly, `plot_kwargs` adjusts the default settings for the Beta posteriors.

    Both these keyword arguments can be overwritten by what the individual `contents`
    have defined.
    """
    if not all(isinstance(c, Histogram) or isinstance(c, Posterior) for c in contents):
        raise TypeError("Contents must be `Histogram` or `Posterior` instances")

    if xlim is None:
        left_lim = floor_to_step(np.min([c.min_val for c in contents]), 2.)
        right_lim = ceil_to_step(np.max([c.max_val for c in contents]), 2.)
    else:
        left_lim = xlim[0]
        right_lim = xlim[-1]
    x = np.linspace(left_lim, right_lim, 300)

    default_hist_kwargs = {
        "density": True,
        "bins": np.linspace(left_lim, right_lim, 60),
        "histtype": "stepfilled",
        "alpha": 0.7,
    }
    if hist_kwargs is not None:
        default_hist_kwargs.update(hist_kwargs)

    default_plot_kwargs = {}
    if plot_kwargs is not None:
        default_plot_kwargs.update(plot_kwargs)

    for content in contents:
        if isinstance(content, Histogram):
            tmp_hist_kwargs = default_hist_kwargs.copy()
            tmp_hist_kwargs.update(content.kwargs)
            axes.hist(content.values, **tmp_hist_kwargs)
        elif isinstance(content, Posterior):
            tmp_plot_kwargs = default_plot_kwargs.copy()
            tmp_plot_kwargs["label"] = f"{content.num_success} / {content.num_total}"
            tmp_plot_kwargs.update(content.kwargs)
            axes.plot(x, content.pdf(x), **tmp_plot_kwargs,)

    axes.set_xlim(left=left_lim, right=right_lim)
    return axes
