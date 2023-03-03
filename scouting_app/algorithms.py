import numpy as np
import matplotlib.pyplot as plt
import threading
from random import seed, randint
from .models import MatchResult

plt.style.use("dark_background")


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


def plt_save(team):
    plt.title(str(team) + " Match Results")
    plt.legend(title="Field:")
    plt.xlabel("Match")
    plt.ylabel("Points")
    plt.savefig("results.png")
    plt.close()


# Generate a ranking value from a `results_matrix`
def generate_rank(team_data):
    np.set_printoptions(precision=3, suppress=True)
    results_matrix = team_data[1]
    crop_results = results_matrix[2:-2]

    weights = np.array([1, 1, 1])
    expected_avg = np.array([12, 25, 40])

    prop_cycle = plt.rcParams["axes.prop_cycle"]
    colors = prop_cycle.by_key()["color"]
    deviation = np.empty(3)

    for i in range(0, 3):
        field = np.array([])
        field = crop_results[:, i]

        field_name = ""
        color = ""
        match i:
            case 0:
                field_name = "Auto"
                color = colors[0]
            case 1:
                field_name = "Teleop"
                color = colors[1]
            case 2:
                field_name = "Endgame"
                color = colors[2]

        deviation[i] = np.std(field)
        plt.plot(field, label=field_name + " Origin", alpha=0.6, color=color)
        plt.axhline(expected_avg[i], color=color, alpha=0.2)

    threading.Thread(target=plt_save, args=(team_data[0],)).start()

    averages = np.average(crop_results, axis=0)  # get the averages
    print(averages)
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
