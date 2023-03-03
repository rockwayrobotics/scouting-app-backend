import numpy as np
import seaborn as sns
import seaborn.objects as so
import matplotlib as mpl
import matplotlib.pyplot as plt
import mplcatppuccin
import pandas as pd
import threading
from random import seed, randint

from .models import MatchResult


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


# just generate some fake match data for now, based around gaussian distribution
def fake_data(match_list):
    for i in match_list:
        i.auto_score = np.random.normal(loc=12.0, scale=6.0)
        i.auto_move = True
        i.teleop_score = np.clip(np.random.normal(loc=25.0, scale=10.0), 0, 75)
        i.endgame_score = np.clip(np.random.normal(loc=40, scale=25.0), 0, 150)
        i.penalty = randint(0, 2)
        i.tippy = False
        i.disabled = False
        i.save()
    return match_list


# generate a `results_matrix` from the `MatchResult`
def generate_matrix(match_list):
    seed()

    results_matrix = np.empty((0, 3))

    # get what we want out of the matches
    for i in match_list:
        new_value = np.array(
            [
                i.auto_score,
                i.teleop_score,
                i.alliance_final_score,
            ]
        )
        results_matrix = np.append(results_matrix, [new_value], axis=0)

    return results_matrix


# Generate a ranking value from a `results_matrix`
def generate_rank(team_data):
    np.set_printoptions(precision=3, suppress=True)
    results_matrix = team_data
    crop_results = results_matrix[2:-2]

    weights = np.array([1, 1, 1])
    expected_avg = np.array([12, 25, 40])

    deviation = np.empty(3)

    for i in range(0, 3):
        field = np.array([])
        field = crop_results[:, i]

        deviation[i] = np.std(field)

    averages = np.average(crop_results, axis=0)  # get the averages
    difference = np.multiply(np.subtract(averages, expected_avg), 2)
    weighted_avg = difference * weights  # weight the averages

    total = np.clip(
        np.add(np.average(weighted_avg), 40).round(), 0, 100
    )  # clip value to 0-100

    return {
        "avg_autoscore": averages[0],
        "avg_telescore": averages[1],
        "avg_endscore": averages[2],
        "ranking": total,
    }


def generate_rankedteam(team):
    match_list = MatchResult.objects.filter(linked_team=team).order_by("recorded_time")
    matrix = generate_matrix(match_list)
    return {
        "id": team.number,
        "rank": generate_rank(matrix),
    }


def analyze_data(match_list):
    match_list = MatchResult.objects.order_by("recorded_time")
    matches = []

    for i in match_list:
        matches.append(
            {
                "match": i.match_number,
                "team": i.linked_team.number,
                "event": i.linked_event.event_key,
                "alliance": i.alliance,
                "recorded_time": i.recorded_time,
                "auto_score": i.auto_score,
                "teleop_score": i.teleop_score,
                "endgame_score": i.endgame_score,
                "final_score": i.alliance_final_score,
                "penalties": i.penalty,
            }
        )

    data = pd.DataFrame(matches)
    data["rank"] = data["final_score"].rank(method="max")

    print(data.sort_values(by="rank"))

    # visualize(data)


def visualize(rankings):
    mpl.style.use("mocha")

    # Score vs. Event
    g = sns.lmplot(
        data=rankings["final_score"].rank(method="max").head(5),
        x="match",
        y="final_score",
        hue="team",
    )
    g.set_axis_labels("Match", "Final Score")
    g.legend.set_title("Team")
    g.figure.set_size_inches(12, 5)
    plt.savefig("rank_vs_auto.png")
