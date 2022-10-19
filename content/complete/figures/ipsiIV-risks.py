"""
Plot historgams over risks for involvement in LNL IV
given different diagnosis scenarios.
"""
from pathlib import Path
import matplotlib.pyplot as plt

import numpy as np
import lyscripts.plot.histograms as lyhist

from _utils import Histogram, Posterior, draw


DATA_DIR = Path("../data")
USZ_COLORS = {
    "blue": '#005ea8',
    "green": '#00afa5',
    "orange": '#f17900',
    "red": '#ae0060',
    "gray": '#c5d5db',
}


if __name__ == "__main__":
    plt.style.use("../../../.mplstyle")

    fig, ax = plt.subplots(figsize=lyhist.get_size(width="full", ratio=2.))

    plots = []
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-ipsiIV-risks.hdf5",
        dataname="ipsi/IV/N0/early",
        kwargs={
            "color": USZ_COLORS["green"],
            "label": "early, N0",
        }
    ))
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-ipsiIV-risks.hdf5",
        dataname="ipsi/IV/involved-II/early",
        kwargs={
            "color": USZ_COLORS["blue"],
            "label": "early, CT finding in LNL II",
            "histtype": "step",
            "alpha": 1.0,
            "linewidth": 2,
        }
    ))
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-ipsiIV-risks.hdf5",
        dataname="ipsi/IV/N0/late",
        kwargs={
            "color": USZ_COLORS["orange"],
            "label": "late, N0",
        }
    ))
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-ipsiIV-risks.hdf5",
        dataname="ipsi/IV/involved-II/late",
        kwargs={
            "color": USZ_COLORS["red"],
            "label": "late, CT finding in LNL II",
        }
    ))
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-ipsiIV-risks.hdf5",
        dataname="ipsi/IV/involved-IIandIII/late",
        kwargs={
            "color": USZ_COLORS["red"],
            "label": "late, CT finding in LNLs II & III",
            "histtype": "step",
            "hatch": "////",
            "linestyle": "-",
            "linewidth": 2,
        }
    ))

    draw(ax, contents=plots, xlim=(0., 6.))

    ax.legend()
    ax.set_xlabel("Risk $R$ [%]")
    ax.set_title(
        "Ipsilateral LNL IV",
        fontweight="bold",
        fontsize="large",
    )

    plt.savefig(Path(__file__).with_suffix(".svg"))
