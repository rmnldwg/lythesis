"""
Plot the ipsilateral prevalences for the three investigated models in one panel each.
"""
from itertools import cycle
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import scipy.stats
import h5py

import lyscripts.plot.histograms as lyhist


# Define model names and location of computed values
MODELS = {
    "$\\mathcal{M}_{ag}$": Path("../data/bilateral-v3-prevalences.hdf5"),
    "$\\mathcal{M}_\\alpha$": Path("../data/midline-with-mixing-v3-prevalences.hdf5"),
    "$\\mathcal{M}_{full}$": Path("../data/midline-without-mixing-v3-prevalences.hdf5"),
}

# define USZ colors
COLORS = {
    "blue": '#005ea8',
    "orange": '#f17900',
    "green": '#00afa5',
    # "red": '#ae0060',
    # "gray": '#c5d5db',
}
COLOR_CYCLE = cycle(COLORS.values())
BINS = 200


if __name__ == "__main__":
    plt.style.use(Path("../../../.mplstyle"))

    fig, ax = plt.subplot_mosaic([
        [
            "$\\mathcal{M}_{ag}$/early",
            "$\\mathcal{M}_\\alpha$/early",
            "$\\mathcal{M}_{full}$/early"
        ],
        [
            "$\\mathcal{M}_{ag}$/late",
            "$\\mathcal{M}_\\alpha$/late",
            "$\\mathcal{M}_{full}$/late"
        ]
    ],
        sharey=True, sharex=True,
        figsize=lyhist.get_size(width="full", ratio=2.)
    )

    for modelname, filepath in MODELS.items():
        with h5py.File(name=filepath, mode="r") as h5_file:
            names, values, lnls, num_matches, num_totals, lines = [], [], [], [], [], [], 
            min_value = 1.
            max_value = 0.

            for stage in ["early", "late"]:
                for lvl in ["II", "III", "IV"]:
                    tmp_values = np.array([])
                    tmp_num_matches = 0
                    tmp_num_totals = 0
                    for midext in ["ext", "noext"]:
                        dataset = h5_file[f"ipsi{lvl}/{stage}/{midext}"]
                        tmp_values = np.concatenate([tmp_values, dataset[:]])
                        tmp_num_matches += dataset.attrs["num_match"]
                        tmp_num_totals += dataset.attrs["num_total"]

                    names.append(f"{modelname}/{stage}")
                    values.append(100. * tmp_values)
                    lnls.append(lvl)
                    num_matches.append(tmp_num_matches)
                    num_totals.append(tmp_num_totals)
                    lines.append(100. * num_matches[-1] / num_totals[-1])
                    min_value = np.minimum(min_value, np.min(values))
                    max_value = np.maximum(max_value, np.max(values))

            min_value = np.min(lines, where=~np.isnan(lines), initial=min_value)
            max_value = np.max(lines, where=~np.isnan(lines), initial=max_value)

        hist_kwargs = {
            "bins": np.linspace(min_value, max_value, BINS),
            "density": True,
            "alpha": 0.5,
            "histtype": "stepfilled"
        }
        x = np.linspace(min_value, max_value, 200)
        ax[f"{modelname}/early"].set_xlim(min_value, max_value)
        ax[f"{modelname}/late"].set_xlim(min_value, max_value)
        
        zipper = zip(names, values, lnls, num_matches, num_totals)

        for i, (name, vals, lnl, a, n) in enumerate(zipper):
            color = next(COLOR_CYCLE)
            posterior = sp.stats.beta.pdf(x / 100., a+1, n-a+1) / 100.
            max_idx = np.argmax(posterior)
            max_x = x[max_idx]
            max_y = posterior[max_idx]

            if "early" in name:
                stage = "early"
                ax[name].set_title(modelname, fontsize="x-large")
            else:
                stage = "late"
                ax[name].set_xlabel("Prevalence [%]")

            ax[name].hist(vals, color=color, **hist_kwargs)
            ax[name].plot(
                x, posterior,
                label=f"{int(a)} / {int(n)}",
                color=color,
            )
            ax[name].annotate(
                text=lnl,
                xy=(max_x - 2.5, max_y + 0.075),
                color=color,
                fontweight="bold",
            )

            if modelname == "$\\mathcal{M}_{full}$":
                ax[name].legend()
            elif modelname == "$\\mathcal{M}_{ag}$":
                ax[name].set_ylabel(stage)
    
    plt.savefig("ipsi-overall.svg")
