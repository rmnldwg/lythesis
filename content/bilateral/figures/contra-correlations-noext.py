"""
Script to plot histograms showing the contralateral correlations between the LNLs II
and III for the three bilateral models but only considering the cases of the tumor
NOT extending over the mid-sagittal plane.
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
EXT = "noext"


if __name__ == "__main__":
    plt.style.use("../../../.mplstyle")

    fig, ax = plt.subplots(
        nrows=3, ncols=2,
        sharex="col", sharey="row",
        figsize=lyhist.get_size(width="full", ratio=2.),
    )

    data_panel = {}
    for row, file in zip(
        ["top"      , "middle"             , "bottom"                ],
        ["bilateral", "midline-with-mixing", "midline-without-mixing"],
    ):
        data_panel[row] = {}
        for col, stage in zip(
            ["left" , "right"],
            ["early", "late" ],
        ):
            data_panel[row][col] = []
            for scenario, color, label in zip(
                ["contraIIInotII"    , "contraIIandIII", "contraIInotIII"    ],
                ["blue"              , "green"         , "orange"            ],
                ["LNL III without II", "LNL III and II", "LNL II without III"],
            ):
                data_panel[row][col].append(
                    Histogram(
                        filename=DATA_DIR / f"{file}-v3-prevalences.hdf5",
                        dataname=f"{scenario}/{stage}/{EXT}",
                        kwargs={"color": USZ_COLORS[color], "label": label},
                    )
                )
                data_panel[row][col].append(
                    Posterior(
                        filename=DATA_DIR / f"{file}-v3-prevalences.hdf5",
                        dataname=f"{scenario}/{stage}/{EXT}",
                        kwargs={"color": USZ_COLORS[color]},
                    )
                )

    left_row = [data_panel[row]["left"] for row in ["top", "middle", "bottom"]]
    right_row = [data_panel[row]["right"] for row in ["top", "middle", "bottom"]]

    top_col = [data_panel["top"][col] for col in ["left", "right"]]
    middle_col = [data_panel["middle"][col] for col in ["left", "right"]]
    bottom_col = [data_panel["bottom"][col] for col in ["left", "right"]]

    left_row_min = 100.
    left_row_max = 0.
    for panel in left_row:
        for c in panel:
            left_row_min = np.minimum(left_row_min, c.min_val)
            left_row_max = np.maximum(left_row_max, c.max_val)

    right_row_min = 100.
    right_row_max = 0.
    for panel in right_row:
        for c in panel:
            right_row_min = np.minimum(right_row_min, c.min_val)
            right_row_max = np.maximum(right_row_max, c.max_val)

    left_row_max = 15.
    right_row_max = 15.

    draw(
        ax[0,0],
        contents=data_panel["top"]["left"],
        xlim=[left_row_min, left_row_max],
    )
    draw(
        ax[0,1],
        contents=data_panel["top"]["right"],
        xlim=[right_row_min, right_row_max],
    )
    ax[0,0].legend(fontsize=6.)
    ax[0,0].set_title("early T-stages")
    ax[0,0].set_ylabel(r"$\mathcal{M}_{ag}$")
    ax[0,1].legend(fontsize=6.)
    ax[0,1].set_title("late T-stages")

    draw(
        ax[1,0],
        contents=data_panel["middle"]["left"],
        xlim=[left_row_min, left_row_max],
    )
    draw(
        ax[1,1],
        contents=data_panel["middle"]["right"],
        xlim=[right_row_min, right_row_max],
    )
    ax[1,0].set_ylabel(r"$\mathcal{M}_\alpha$")

    draw(
        ax[2,0],
        contents=data_panel["bottom"]["left"],
        xlim=[left_row_min, left_row_max],
    )
    draw(
        ax[2,1],
        contents=data_panel["bottom"]["right"],
        xlim=[right_row_min, right_row_max],
    )
    ax[2,0].set_ylabel(r"$\mathcal{M}_{full}$")
    ax[2,0].set_xlabel("prevalence [%]")
    ax[2,1].set_xlabel("prevalence [%]")

    plt.savefig(f"contra-correlations-{EXT}.svg")

