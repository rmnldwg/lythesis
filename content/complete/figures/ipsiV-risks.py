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
        filename=DATA_DIR / "complete-v1-ipsiV-risks.hdf5",
        dataname="ipsi-V/N0/late",
        kwargs={
            "color": USZ_COLORS["green"],
            "label": "N0",
        }
    ))
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-ipsiV-risks.hdf5",
        dataname="ipsi-V/ipsi-II/late",
        kwargs={
            "color": USZ_COLORS["orange"],
            "label": "LNL II involved",
        }
    ))
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-ipsiV-risks.hdf5",
        dataname="ipsi-V/ipsi-IIandIII/late",
        kwargs={
            "color": USZ_COLORS["red"],
            "label": "LNL II & III involved",
        }
    ))
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-ipsiV-risks.hdf5",
        dataname="ipsi-V/ipsi-IIandIIIandIV/late",
        kwargs={
            "color": "black",
            "label": "LNL II, III & IV involved",
        }
    ))

    draw(ax, contents=plots, xlim=(0., 5.))

    ax.legend(
        title=(
            "All for late T-category,\n"
            "given the following diagnosis (CT scan):"
        ),
        alignment="left",
    )
    ax.set_xlabel("Risk $R$ [%]")
    ax.set_title(
        "Ipsilateral LNL V",
        fontweight="bold",
        fontsize="large",
    )

    plt.savefig(Path(__file__).with_suffix(".svg"))
