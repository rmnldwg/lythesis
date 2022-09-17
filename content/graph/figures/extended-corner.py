"""
Corner plot of the extended network using the base graph.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

from emcee.backends import HDFBackend
from corner import corner
from lyscripts.plot.histograms import get_size


MODEL = Path("../data/extended-base-v1-samples.hdf5")
LABELS = [
    r"$\tilde{b}_1$",
    r"$\tilde{b}_2$",
    r"$\tilde{b}_3$",
    r"$\tilde{b}_4$",
    r"$\tilde{b}_5$",
    r"$\tilde{b}_7$",
    r"$\tilde{t}_{2 \rightarrow 3}$",
    r"$\tilde{t}_{2 \rightarrow 5}$",
    r"$\tilde{t}_{3 \rightarrow 4}$",
    r"$p_{late}$",
]
CORNER_KWARGS = {
    "smooth": True,
    "color": "#005ea8",
    "plot_datapoints": False,
    "plot_density": True,
    "no_fill_contours": True,
    "show_titles": True,
    "levels": [0.2, 0.5, 0.8],
    "hist_kwargs": {"histtype": "stepfilled", "color": "#005ea8"},
    "contour_kwargs": {"colors": "black"},
    "title_kwargs": {"fontsize": "medium"},
}


if __name__ == "__main__":
    plt.style.use(Path("../../../.mplstyle"))

    backend = HDFBackend(MODEL, read_only=True)
    samples = backend.get_chain(flat=True)

    fig = plt.figure(figsize=get_size(width="full", ratio=1.))
    fig = corner(
        samples,
        labels=LABELS,
        fig=fig,
        **CORNER_KWARGS,
    )

    axes = fig.get_axes()
    for ax in axes:
        ax.grid(False)
        xleft, xright = ax.get_xlim()
        ylower, _ = ax.get_ylim()
        xleft = np.maximum(0., xleft)
        xright = np.minimum(1., xright)
        ylower = np.maximum(0., ylower)
        ax.set_xlim(xleft, xright)
        ax.set_ylim(ylower)
        ax.tick_params(labelsize=5.0)

    plt.savefig("extended-base-corner.svg")
