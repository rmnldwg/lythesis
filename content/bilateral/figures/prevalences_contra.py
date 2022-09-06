"""
Plot the contralateral prevalence of involvement for the three investigated models.
For each model, plot the four combination of early/late T-stage and with/without
midline extension.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import h5py
from cycler import cycler

import lyscripts.plot.histograms as lyhist
from lyscripts.plot.histograms import COLORS


MODELS = [
    Path("../data/bilateral-v2-prevalences.hdf5",),
    Path("../data/midline-with-mixing-v2-prevalences.hdf5",),
    Path("../data/midline-without-mixing-v2-prevalences.hdf5"),
]

CYCLE = (
    cycler(
        stage=["early", "late"],
    ) *
    cycler(
        midline=["noext", "ext"],
    ) +
    cycler(
        color=list(COLORS.values())[:4]
    ) *
    cycler(
        density=[True],
        alpha=[0.5],
        histtype=["stepfilled"],
    )
)
BINS = 80
TITLES = [
    "$\\mathcal{M}_{ag}$",
    "$\\mathcal{M}_\\alpha$",
    "$\\mathcal{M}_{full}$",
]


if __name__ == "__main__":
    plt.style.use(Path("../../../.mplstyle"))
    
    fig, ax = plt.subplots(
        nrows=1, ncols=3,
        sharey=True,
        figsize=lyhist.get_size(width="full", ratio=3),
        constrained_layout=True,
    )

    for i, filepath in enumerate(MODELS):
        with h5py.File(name=filepath, mode="r") as h5_file:
            min = 0.
            max = 55.
            for stage in ["early", "late"]:
                for midline in ["ext", "noext"]:
                    values = 100. * h5_file[f"contra/{stage}/{midline}"][:]
                    min = np.minimum(min, np.min(values))
                    max = np.maximum(max, np.max(values))

            for pos in CYCLE:
                stage = pos.pop("stage")
                midline = pos.pop("midline")
                values = 100. * h5_file[f"contra/{stage}/{midline}"][:]
                num_match = h5_file[f"contra/{stage}/{midline}"].attrs["num_match"]
                num_total = h5_file[f"contra/{stage}/{midline}"].attrs["num_total"]
                bins = np.linspace(min, max, BINS)
                x = np.linspace(min, max, 200)
                post = 0.01 * sp.stats.beta.pdf(
                    x / 100.,
                    a=num_match+1,
                    b=num_total-num_match+1
                )
                
                ax[i].set_title(TITLES[i], fontsize="x-large")
                
                ax[i].hist(values, bins=bins, label=f"{stage}, {midline}", **pos)
                ax[i].plot(x, post, label=f"{int(num_match)} / {int(num_total)}", color=pos["color"])

                ax[i].set_xlim(left=min, right=max)
                ax[i].set_xlabel("Prevalence [%]")

                if i == 2:
                    ax[i].legend()

    plt.savefig("contra-comp.svg")
    plt.savefig("contra-comp.png", dpi=300)
