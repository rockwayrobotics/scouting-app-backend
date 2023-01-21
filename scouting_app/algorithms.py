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
    # fake_data(match_list)
    results_matrix = np.empty((0, 4))

    # get what we want out of the matches
    for i in match_list:
        new_value = np.array(
            [
                i.auto_score,
                i.teleop_score,
                i.alliance_final_score,
                int(i.penalty),
            ]
        )
        # print(color.CYAN+color.UNDERLINE+
        #       "\nMatch #"+
        #       color.END+color.DARKCYAN+color.UNDERLINE+
        #       str(i.match_number)+
        #       color.END+
        #       "\n    auto_score: "+
        #       color.YELLOW+
        #       str(round(new_value[0]))+
        #       color.END+
        #       "\n    teleop_score: "+
        #       color.BLUE+
        #       str(round(new_value[1]))+
        #       color.END+
        #       "\n    final_score: "+
        #       color.PURPLE+
        #       str(round(new_value[2]))+
        #       color.END+
        #       "\n    penalities: "+
        #       color.RED+
        #       str(new_value[3])+
        #       color.END
        #       )
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
    # TODO:
    # - [x] rank based on expected average
    # - [ ] adjust expected average on frontend
    # - [ ] add in wanted fields
    # - [ ] test ranking for different teams
    # - [ ] value recent matches more highly

    np.set_printoptions(precision=3, suppress=True)
    results_matrix = team_data[1]
    crop_results = results_matrix[2:-2]

    weights = np.array([1, 1, 1, 1])
    expected_avg = np.array([12, 25, 40, 1])
    # x = np.linspace(0,1,4)
    # f = x**2
    f = np.full(3, 1 / 3)
    kernel = np.logspace(2, 1, num=5, base=0.2)

    prop_cycle = plt.rcParams["axes.prop_cycle"]
    colors = prop_cycle.by_key()["color"]
    deviation = np.empty(4)

    conv_results = np.empty((4, 38))
    for i in range(0, 4):
        field = np.array([])
        field = crop_results[:, i]

        convolution = np.convolve(f, field, mode="same")
        # convolution = np.convolve(kernel, convolution, mode="same")
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
            case 3:
                field_name = "Penalties"
                color = colors[3]

        deviation[i] = np.std(field)
        conv_results[i] = convolution
        plt.plot(field, label=field_name + " Origin", alpha=0.6, color=color)
        plt.plot(convolution, color=color, label=field_name)
        plt.axhline(expected_avg[i], color=color, alpha=0.2)

    print(deviation)

    threading.Thread(target=plt_save, args=(team_data[0],)).start()

    averages = np.average(conv_results, axis=1)  # get the averages
    difference = np.multiply(np.subtract(averages, expected_avg), 2)
    weighted_avg = difference * weights  # weight the averages

    total = np.clip(
        np.add(np.average(weighted_avg), 40).round(), 0, 100
    )  # clip value to 0-100

    return (team_data[0], total)
