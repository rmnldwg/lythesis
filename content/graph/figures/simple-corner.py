"""
Combined corner plot of the simple graph with no connections btw. LNL II and III as
well as a corner plot of the graph with a two-way connection between those LNLs.
"""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

from emcee.backends import HDFBackend
from corner import corner
from lyscripts.plot.histograms import get_size


MODELS = {}
for tag in ["nocon", "both"]:
    MODELS[tag] = Path(f"../data/simple-{tag}-v1-samples.hdf5")

# define USZ colors
COLORS = {
    "green": '#00afa5',
    "orange": '#f17900',
    "blue": '#005ea8',
    "red": '#ae0060',
    # "gray": '#c5d5db',
}
CORNER_KWARGS = {
    "smooth": True,
    "plot_datapoints": False,
    "plot_density": True,
    "no_fill_contours": True,
    "show_titles": True,
    "levels": [0.2, 0.5, 0.8],
    "contour_kwargs": {"colors": "black"},
    "title_kwargs": {"fontsize": "medium"},
}


if __name__ == "__main__":
    plt.style.use(Path("../../../.mplstyle"))

    # Samples of graph with no connection btw LNL II and III
    nocon_backend = HDFBackend(MODELS["nocon"], read_only=True)
    nocon_samples = nocon_backend.get_chain(flat=True)
    labels = [
        r"$\tilde{b}_2$",
        r"$\tilde{b}_3$",
        r"$p_{late}$"
    ]

    fig = plt.figure(
        figsize=get_size(width=8., ratio=1.),
    )
    corner(
        nocon_samples,
        labels=labels,
        reverse=True,
        fig=fig,
        color=COLORS["green"],
        hist_kwargs={
            "histtype": "stepfilled",
            "color": COLORS["green"],
        },
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

    plt.savefig("simple-nocon-corner.svg")
    
    # samples of graph with connection going both directions
    both_backend = HDFBackend(MODELS["both"], read_only=True)
    both_samples = both_backend.get_chain(flat=True)
    labels = [
        r"$\tilde{b}_2$",
        r"$\tilde{b}_3$",
        r"$\tilde{t}_{2 \rightarrow 3}$",
        r"$\tilde{t}_{3 \rightarrow 2}$",
        r"$p_{late}$"
    ]

    fig = plt.figure(
        figsize=get_size(width=5. * 16. / 6., ratio=1.),
    )
    corner(
        both_samples,
        labels=labels,
        fig=fig,
        color=COLORS["blue"],
        hist_kwargs={
            "histtype": "stepfilled",
            "color": COLORS["blue"],
        },
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

    plt.savefig("simple-both-corner.svg")
