"""
Plot historgams over risks for involvement in LNL II contralaterally
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
        filename=DATA_DIR / "complete-v1-contraII-risks.hdf5",
        dataname="contra-II/N0/early/noext",
        kwargs={
            "color": USZ_COLORS["green"],
            "label": "early, no ext, N0",
        }
    ))
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-contraII-risks.hdf5",
        dataname="contra-II/N0/late/noext",
        kwargs={
            "color": USZ_COLORS["blue"],
            "label": "late, no ext, N0",
            "histtype": "step",
            "linewidth": 2.,
            "alpha": 1.,
        }
    ))
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-contraII-risks.hdf5",
        dataname="contra-II/ipsi-IIandIII/late/noext",
        kwargs={
            "color": USZ_COLORS["blue"],
            "label": "late, no ext, CT shows ipsi LNLs II & III involved",
        }
    ))
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-contraII-risks.hdf5",
        dataname="contra-II/N0/early/ext",
        kwargs={
            "color": USZ_COLORS["orange"],
            "label": "early, ext, N0",
        }
    ))
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-contraII-risks.hdf5",
        dataname="contra-II/ipsi-II/early/ext",
        kwargs={
            "color": USZ_COLORS["orange"],
            "label": "early, ext, CT shows ipsi LNL II involved",
            "histtype": "step",
            "linewidth": 2.,
            "alpha": 1.,
            "linestyle": "-",
        }
    ))
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-contraII-risks.hdf5",
        dataname="contra-II/N0/late/ext",
        kwargs={
            "color": "black",
            "label": "late, ext, N0",
        }
    ))
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-contraII-risks.hdf5",
        dataname="contra-II/ipsi-II/late/ext",
        kwargs={
            "color": USZ_COLORS["red"],
            "label": "late, ext, CT shows ipsi LNL II involved",
            "histtype": "step",
            "linewidth": 2.,
            "alpha": 1.,
            "linestyle": "-",
        }
    ))
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-contraII-risks.hdf5",
        dataname="contra-II/ipsi-IIandIII/late/ext",
        kwargs={
            "color": USZ_COLORS["red"],
            "label": "late, ext, CT shows ipsi LNLs II & III involved",
        }
    ))

    draw(ax, contents=plots, xlim=(0., 11.))

    ax.legend()
    ax.set_xlabel("Risk $R$ [%]")
    ax.set_title(
        "Contralateral LNL II",
        fontweight="bold",
        fontsize="large",
    )

    plt.savefig(Path(__file__).with_suffix(".svg"))
