"""
Utility functions for plotting hostograms over prevalences.
"""
from pathlib import Path
from typing import Any, Callable, Dict, List, Union
import h5py

import numpy as np
import scipy as sp
import scipy.stats


def read_prevalences(
    models: List[str],
    format_filename: Callable,
    scenarios: List[str],
    t_stages: List[str],
) -> Dict[str, Any]:
    """
    Read in HDF5 files, whose filenames are computed by calling `format_filename` with
    the respective entry in `models`. Inside the HDF5 files the function expects a
    group for each of the `scenarios` and under that a dataset for each of the
    `t_stages`. The data found in these datasets will be put into a nested dictionary
    of the structure model > scenario > T-stage.
    """
    output = {}
    min_value = 100.
    max_value = 0.
    for model in models:
        output[model] = {}
        filename = Path(format_filename(model))
        with h5py.File(name=filename, mode="r") as h5_file:
            for scenario in scenarios:
                output[model][scenario] = {}
                for stage in t_stages:
                    tmp = {}
                    dataset = h5_file[f"{scenario}/{stage}"]
                    values = 100. * dataset[:]
                    min_value = np.minimum(min_value, np.min(values))
                    max_value = np.maximum(max_value, np.max(values))
                    tmp["values"] = values
                    tmp["num_success"] = int(dataset.attrs["num_match"])
                    tmp["num_fail"] = int(dataset.attrs["num_total"] - tmp["num_success"])
                    output[model][scenario][stage] = tmp

    return output, min_value, max_value


def comp_scaled_beta_posterior(
    x: np.ndarray,
    num_success: int,
    num_fail: int,
) -> np.ndarray:
    """
    Compute the Beta posterior over the success probability (in percent) for
    `num_success` observed successes and `num_total` tries.
    """
    return sp.stats.beta.pdf(x / 100., num_success+1, num_fail+1) / 100.


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


HIST_KWARGS = {
    "density": True,
    "histtype": "stepfilled",
    "alpha": 0.7,
}
