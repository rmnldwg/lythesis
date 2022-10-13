"""
Analyze the senstivity and specificity of the CLB data.
"""
from pathlib import Path
from typing import Optional
import re

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
    table_dir: Optional[str] = None,
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

    for obs in [False, True]:
        if obs not in confusion_matrix:
            confusion_matrix[obs] = 0

    if table_dir is not None:
        write_latex(
            confusion_matrix,
            observation=observed_modality,
            truth=truth_modality,
            side=side,
            lnl=lnl,
            table_dir=table_dir,
        )
    return confusion_matrix


def write_latex(
    confusion_matrix: pd.DataFrame,
    observation: str,
    truth: str,
    side: str,
    lnl: str,
    table_dir: str,
    width: float = 0.45,
):
    """Write a confusion matrix nicely into a LaTeX file."""
    Path(table_dir).mkdir(exist_ok=True)
    table_path = Path(table_dir) / f"{observation}-vs-{truth}-{side}-{lnl}"
    table_path = table_path.with_suffix(".tex")
    caption = f"{side}lateral LNL {lnl}"

    with open(table_path, mode="w") as table_file:
        latex = confusion_matrix.to_latex(
            column_format=r"|l|rr|",
            caption=caption,
        )
        latex = latex.replace("_", " ")
        latex = latex.replace(
            r"\begin{table}",
            r"\begin{subtable}{" + f"{width:.2f}" + r"\textwidth}"
        )
        latex = latex.replace(r"\end{table}", r"\end{subtable}")
        latex = re.sub("\w*rule", "hline", latex)

        latex_lines = latex.splitlines()
        for i,line in enumerate(latex_lines):
            if i == 5:
                latex_lines[i] = line.replace("observed", r"\diagbox{truth}{observed}")
            elif i == 6:
                latex_lines[i] = ""
        latex = "\n".join(latex_lines)

        table_file.write(latex)


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
                table_dir="../tables",
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
                    CT["sensitivity"],
                    color=COLORS["orange"],
                    linestyle="--",
                    label="CT" if i == 0 else None,
                )
                ax[i,1].axvline(
                    MRI["sensitivity"],
                    color=COLORS["red"],
                    linestyle="-.",
                    label="MRI" if i == 0 else None,
                )
                ax[i,1].axvline(
                    PET["sensitivity"],
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
