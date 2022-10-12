"""
This scripts generates a figure comparing the distribution of T-stages for the USZ data
and the CLB dataset.
"""
from pathlib import Path
from typing import Union

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from lyscripts.plot.histograms import get_size


def extract_tstages(
    patient_data: pd.DataFrame,
    density: bool = True,
    percent: bool = True,
) -> float:
    """Get `pd.Series` with number of patients per T-stage."""
    counted_tstages = patient_data.groupby(T_STAGE_COL).size()
    norm = 1 if not density else len(patient_data)
    fac = 1 if not percent else 100
    
    for t in [0,1,2,3,4]:
        if t in counted_tstages:
            yield fac * counted_tstages[t] / norm
        else:
            yield 0


USZ_FILE = Path("../../dataset_usz/data/2021-usz-oropharynx-enhanced.csv")
CLB_FILE = Path("../data/2021-clb-oropharynx-enhanced.csv")
OUTPUT = Path(__file__).with_suffix(".svg")

T_STAGE_COL = ("tumor", "1", "t_stage")

COLORS = {
    "green": '#00afa5',
    "red": '#ae0060',
    "blue": '#005ea8',
    "orange": '#f17900',
    "gray": '#c5d5db',
}


if __name__ == "__main__":
    plt.style.use("../../../.mplstyle")

    fig, ax = plt.subplots(figsize=get_size())
    
    usz_data = pd.read_csv(USZ_FILE, header=[0,1,2])
    clb_data = pd.read_csv(CLB_FILE, header=[0,1,2])

    t_stage_df = pd.DataFrame({
        "USZ": [num for num in extract_tstages(usz_data, density=True)],
        "CLB": [num for num in extract_tstages(clb_data, density=True)],
    },
        index=[0,1,2,3,4],
    )
    t_stage_df.plot.bar(ax=ax, rot=0)

    ax.set_xlabel("T-Stage")
    ax.set_ylabel("Portion of patients [%]")
    ax.legend(fontsize="medium", loc="upper left")

    plt.savefig(OUTPUT)
