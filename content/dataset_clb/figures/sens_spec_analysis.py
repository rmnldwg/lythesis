"""
Analyze the senstivity and specificity of the CLB data.
"""
from pathlib import Path

import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

from lyscripts.plot.histograms import get_size


def extract_confusion_matrix(
    data: pd.DataFrame,
    observed_modality: str,
    truth_modality: str,
    side: str,
    lnl: str,
) -> pd.DataFrame:
    """
    Extract the confusion matrix of the `observed_modality` from the `data`, based on
    the true values as reported by the `truth_modality`. Do this for the specified
    `side` of the neck and the requested `lnl`. The returned `confusion_matrix` is a
    2x2 `DataFrame` and can be indexed like this:

    >>> observed = False
    >>> truth = True
    >>> num_false_positive = confusion_matrix[observed][truth]
    """
    observed_column = (observed_modality, side, lnl)
    truth_column = (truth_modality, side, lnl)
    counted_cases = data.groupby([observed_column, truth_column], as_index=False).size()
    confusion_matrix = counted_cases.pivot_table(
        values="size",
        aggfunc=sum,
        index=[truth_column],
        columns=[observed_column],
    )
    confusion_matrix.index.name = "truth"
    confusion_matrix.columns.name = "observed"
    return confusion_matrix


def comp_scaled_beta_posterior(
    x: np.ndarray,
    num_success: int,
    num_fail: int,
) -> np.ndarray:
    """
    Compute the Beta posterior over the success probability (in percent) for
    `num_success` observed successes and `num_total` tries.
    """
    return sp.stats.beta.pdf(x / 100., num_success+1, num_fail+1) / 100.


INPUT = Path("../data/2021-clb-oropharynx.csv")
OUTPUT = Path(__file__).with_suffix(".svg")
LNLS = ["Ib", "II", "III", "IV", "V"]
COLORS = {
    "blue": '#005ea8',
    "green": '#00afa5',
    "orange": '#f17900',
    "red": '#ae0060',
    "gray": '#c5d5db',
}
CT = {
    "specificity": 76,
    "sensitivity": 81,
}
MRI = {
    "specificity": 63,
    "sensitivity": 81,
}
PET = {
    "specificity": 86,
    "sensitivity": 79,
}


if __name__ == "__main__":
    data = pd.read_csv(INPUT, header=[0,1,2])

    confusion_matrices = {}
    for side in ["ipsi", "contra"]:
        confusion_matrices[side] = {}
        for lnl in LNLS:
            confusion_matrices[side][lnl] = extract_confusion_matrix(
                data=data,
                observed_modality="diagnostic_consensus",
                truth_modality="pathology",
                side=side,
                lnl=lnl,
            )

    plt.style.use("../../../.mplstyle")
    fig, ax = plt.subplots(
        nrows=len(LNLS), ncols=2,
        sharex=True, sharey="row",
        figsize=get_size(width="full", ratio=1.3),
    )

    ax[-1,0].set_xlabel("specificity $s_P$ [%]")
    ax[-1,1].set_xlabel("sensitivity $s_N$ [%]")

    x = np.linspace(0., 100., 500)
    for side in ["ipsi", "contra"]:
        color = COLORS["green"] if side == "ipsi" else COLORS["blue"]
        for i,lnl in enumerate(LNLS):
            try:
                confusion_matrix = confusion_matrices[side][lnl]
                true_negative = confusion_matrix[False][False]
                false_positive = confusion_matrix[True][False]
                specificity = true_negative / (true_negative + false_positive)
                posterior_over_specificity = comp_scaled_beta_posterior(
                    x=x,
                    num_success=true_negative,
                    num_fail=false_positive,
                )
                ax[i,0].plot(
                    x, posterior_over_specificity,
                    color=color,
                    linewidth=1.5,
                    label=f"{side}: {specificity:.1%}"
                )
                ax[i,0].axvline(
                    CT["specificity"],
                    color=COLORS["orange"],
                    linestyle="--",
                    label="CT" if i == 0 else None,
                )
                ax[i,0].axvline(
                    MRI["specificity"],
                    color=COLORS["red"],
                    linestyle="-.",
                    label="MRI" if i == 0 else None,
                )
                ax[i,0].axvline(
                    PET["specificity"],
                    color="black",
                    linestyle=":",
                    label="PET" if i == 0 else None,
                )
                ax[i,0].set_xlim(left=0., right=100.)
                ax[i,0].set_ylabel(lnl)
                ax[i,0].legend()
            except KeyError:
                pass

            try:
                true_positive = confusion_matrix[True][True]
                false_negative = confusion_matrix[False][True]
                sensitivity = true_positive / (true_positive + false_negative)
                posterior_over_sensitivity = comp_scaled_beta_posterior(
                    x=x,
                    num_success=true_positive,
                    num_fail=false_negative,
                )
                ax[i,1].plot(
                    x, posterior_over_sensitivity,
                    color=color,
                    linewidth=1.5,
                    label=f"{side}: {sensitivity:.1%}"
                )
                ax[i,1].axvline(
                    CT["specificity"],
                    color=COLORS["orange"],
                    linestyle="--",
                    label="CT" if i == 0 else None,
                )
                ax[i,1].axvline(
                    MRI["specificity"],
                    color=COLORS["red"],
                    linestyle="-.",
                    label="MRI" if i == 0 else None,
                )
                ax[i,1].axvline(
                    PET["specificity"],
                    color="black",
                    linestyle=":",
                    label="PET" if i == 0 else None,
                )
                ax[i,1].set_xlim(left=0., right=100.)
                ax[i,1].set_ylim(bottom=0.)
                ax[i,1].legend()
            except KeyError:
                pass

    plt.savefig(OUTPUT)
