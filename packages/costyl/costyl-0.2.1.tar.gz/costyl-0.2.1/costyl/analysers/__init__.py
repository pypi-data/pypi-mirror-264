
from .layout import layout_analysis
from .lexical import lexical_analysis

import numpy as np


def analyse_vectorized_files(vectorized_files_whole: list[str], vectorized_files_lines: list[list[str]]) -> np.ndarray:
    """
    Analyse the files and return a matrix with the results of the analysis
    """
    layout = layout_analysis(vectorized_files_lines)
    lexical = lexical_analysis(vectorized_files_whole)

    return np.concatenate((layout, lexical), axis=1)
