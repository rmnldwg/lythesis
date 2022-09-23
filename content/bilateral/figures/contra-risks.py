"""
Script to plot contralateral risk(s) depending on ipsilateral involvement.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from lyscripts.plot.histograms import get_size

from _utils import Histogram, draw


RISK_FILE = "../data/midline-with-mixing-v3-risks.hdf5"
USZ_COLORS = {
    "blue": '#005ea8',
    "green": '#00afa5',
    "orange": '#f17900',
    "red": '#ae0060',
    "gray": '#c5d5db',
}


if __name__ == "__main__":
    plt.style.use("../../../.mplstyle")

    fig, ax = plt.subplots(
        nrows=1, ncols=1,
        figsize=get_size(),
    )

    histograms = [
        Histogram(
            filename=RISK_FILE,
            dataname="contra-II/healthyCT/early/noext",
            kwargs={
                "label": "...cN0, early, no extension",
                "color": USZ_COLORS["green"],
            }
        ),
        Histogram(
            filename=RISK_FILE,
            dataname="contra-II/healthyCT/late/noext",
            kwargs={
                "label": "...cN0, late, no extension",
                "color": USZ_COLORS["blue"],
                "histtype": "step",
                "linewidth": 1.5,
                "alpha": 1.,
                "hatch": "////",
            }
        ),
        Histogram(
            filename=RISK_FILE,
            dataname="contra-II/healthyCT/late/ext",
            kwargs={
                "label": "...cN0, late, mid-plane ext.",
                "color": USZ_COLORS["blue"],
            }
        ),
        Histogram(
            filename=RISK_FILE,
            dataname="contra-II/ipsi-II-pos/late/ext",
            kwargs={
                "label": "...ipsi LNL II positive,\nlate, mid-plane ext.",
                "color": USZ_COLORS["orange"]
            }
        ),
        Histogram(
            filename=RISK_FILE,
            dataname="contra-II/ipsi-IIandIII-pos/late/ext",
            kwargs={
                "label": "...ipsi LNLs II & III positive,\nlate, mid-plane ext.",
                "color": USZ_COLORS["red"],
                "histtype": "step",
                "linewidth": 1.5,
                "linestyle": "-",
                "alpha": 1.,
                "hatch": r"\\\\",
            }
        ),
    ]

    ax = draw(
        ax,
        contents=histograms,
        xlim=[0., 14.],
        hist_kwargs={"bins": np.linspace(0., 14., 100)}
    )
    ax.set_title("Risk of contra LNL II involvement, given...")
    ax.set_xlabel("Risk $R$ [%]")
    ax.set_ylabel("$p(R)$")
    ax.legend(labelspacing=0.3)
    ax.set_ylim(bottom=0., top=1.5)
    plt.savefig(Path(__file__).with_suffix(".svg"))
