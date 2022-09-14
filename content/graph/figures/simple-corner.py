"""
Combined corner plot of the simple graph with no connections btw. LNL II and III as
well as a corner plot of the graph with a two-way connection between those LNLs.
"""
from pathlib import Path
import matplotlib.pyplot as plt

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


if __name__ == "__main__":
    nocon_backend = HDFBackend(MODELS["nocon"], read_only=True)
    nocon_samples = nocon_backend.get_chain(flat=True)

    both_backend = HDFBackend(MODELS["both"], read_only=True)
    both_samples = both_backend.get_chain(flat=True)

    fig_nocon, ax_nocon = plt.subplots(
        nrows=3, ncols=3,
        figsize=get_size(width="full", ratio=1.)
    )
    fig_nocon = corner(
        nocon_samples,
        reverse=True,
        fig=fig_nocon,
    )
    
    fig_both, ax_both = plt.subplots(
        nrows=5, ncols=5,
        figsize=get_size(width="full", ratio=1.)
    )
    fig_both = corner(
        both_samples,
        fig=fig_both,
    )
    
    for i in range(1,4):
        for j in range(1,i+1):
            ax_both[-i,-j] = ax_nocon[-i,-j]
    
    plt.savefig("test.png")
