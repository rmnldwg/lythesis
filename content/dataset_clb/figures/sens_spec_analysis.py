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
OUTPUT = Path(__file__).with_suffix(".png")
LNLS = ["Ib", "II", "III", "IV", "V"]


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
        figsize=get_size(width="full", ratio=8. / len(LNLS)),
    )

    x = np.linspace(0., 100., 500)
    for i,lnl in enumerate(LNLS):
        confusion_matrix = confusion_matrices["ipsi"][lnl]
        try:
            posterior_over_specificity = comp_scaled_beta_posterior(
                x=x,
                num_success=confusion_matrix[False][False],
                num_fail=confusion_matrix[True][False],
            )
            ax[i,0].plot(x, posterior_over_specificity)
            ax[i,0].set_xlim(left=0., right=100.)
        except KeyError:
            ax[i,0].remove()

        try:
            posterior_over_sensitivity = comp_scaled_beta_posterior(
                x=x,
                num_success=confusion_matrix[True][True],
                num_fail=confusion_matrix[False][True],
            )
            ax[i,1].plot(x, posterior_over_sensitivity)
            ax[i,1].set_xlim(left=0., right=100.)
            ax[i,1].set_ylim(bottom=0.)
        except KeyError:
            ax[i,1].remove()

    plt.savefig(OUTPUT)
