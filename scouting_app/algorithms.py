import numpy as np
from .models import MatchResult

def generate_matrix(match_list):
    results_matrix = np.empty((0,4))

    # get what we want out of the matches
    for i in match_list:
        new_value = np.array([i.auto_score,
                              i.teleop_score,
                                  i.alliance_final_score,
                               int(i.penalty),])
        print(new_value)
        np.append(
            results_matrix,
            [new_value],
            axis=0)

    return results_matrix
