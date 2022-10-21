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
        filename=DATA_DIR / "complete-v1-contraIIIandIV-risks.hdf5",
        dataname="contra-III/N0/late/ext",
        kwargs={
            "color": USZ_COLORS["green"],
            "label": "III, N0 CT diagnosis",
        }
    ))
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-contraIIIandIV-risks.hdf5",
        dataname="contra-III/ipsi-IIandIII/late/ext",
        kwargs={
            "color": USZ_COLORS["orange"],
            "label": "III, involved ipsi LNLs II & III",
        }
    ))
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-contraIIIandIV-risks.hdf5",
        dataname="contra-III/ipsi-IIandIII-contra-II/late/ext",
        kwargs={
            "color": USZ_COLORS["red"],
            "label": "III, involved ipsi LNLs II & III, and contra LNL II",
        }
    ))

    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-contraIIIandIV-risks.hdf5",
        dataname="contra-IV/ipsi-IIandIII/late/ext",
        kwargs={
            "color": USZ_COLORS["blue"],
            "label": "IV, involved ipsi LNLs II & III",
            "histtype": "step",
            "alpha": 1.0,
            "linewidth": 2.0,
            "linestyle": "-",
            "hatch": "////"
        }
    ))
    plots.append(Histogram(
        filename=DATA_DIR / "complete-v1-contraIIIandIV-risks.hdf5",
        dataname="contra-IV/N+/late/ext",
        kwargs={
            "color": "black",
            "label": "IV, involved ipsi LNLs II & III, contra LNLs II & III",
            "histtype": "step",
            "alpha": 1.0,
            "linewidth": 2.0,
            "linestyle": "-",
            "hatch": "////"
        }
    ))

    draw(ax, contents=plots, xlim=(0., 6.))

    ax.set_title(
        "Risk for Involvement in Contralateral LNLs III and IV",
        fontweight="bold",
        fontsize="large",
    )
    ax.legend(
        title=(
            "All late T-category, with mid-plane extension.\n"
            "Diagnosed involvement based on CT.\n\n"
            "Contra LNL..."
        ),
        alignment="left"
    )
    ax.set_xlabel("Risk $R$ [%]")

    plt.savefig(Path(__file__).with_suffix(".svg"))
