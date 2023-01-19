import numpy as np
import matplotlib.pyplot as plt
from random import seed, randint
from .models import MatchResult

plt.style.use('dark_background')

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# just generate some fake match data for now, based around gaussian distribution
def fake_data(match_list):
    for i in match_list:
        i.auto_score = np.random.normal(loc=12.0, scale=6.0)
        i.auto_move = True
        i.teleop_score = np.clip(np.random.normal(loc=25.0, scale=10.0), 0, 75)
        i.endgame_score = np.clip(np.random.normal(loc=40, scale=25.0), 0, 150)
        i.penalty = randint(0,2)
        i.tippy = False
        i.disabled = False
        i.save()
    return match_list

# generate a `results_matrix` from the `MatchResult`
def generate_matrix(match_list):
    seed()
    #fake_data(match_list)
    results_matrix = np.empty((0,4))

    # get what we want out of the matches
    for i in match_list:
        new_value = np.array([i.auto_score,
                              i.teleop_score,
                              i.alliance_final_score,
                              int(i.penalty),])
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
        results_matrix = np.append(
            results_matrix,
            [new_value],
            axis=0)

    return results_matrix


# Generate a ranking value from a `results_matrix`
def generate_rank(team_data):
    results_matrix = team_data[1]
    crop_results = results_matrix[2:-2]

    weights = np.array([0.8, 1, 1.5, -4])
    expected_avg = np.array([18, 35, 65, 4])
    x = np.linspace(0,2,5)
    f = x**2

    # TODO:
    # - [x] rank based on expected average
    # - [ ] adjust expected average on frontend
    # - [ ] add in wanted fields
    # - [ ] test ranking for different teams
    # - [ ] value recent matches more highly


    conv_results = np.empty((4,38))
    for i in range(0,4):
        field = np.array([])
        field = crop_results[:,i]

        convolution = np.convolve(f, field, mode="same")
        field_name = ""
        match i:
            case 0:
                field_name = "Auto"
                plt.plot(field, label=field_name)
                plt.plot(convolution, label=field_name+"convolution")
                plt.plot(f, label="kernel")
            case 1:
                field_name = "Teleop"
            case 2:
                field_name = "Endgame"
            case 3:
                field_name = "Penalties"


        conv_results = np.append(conv_results, [convolution], axis=0)
        # print(field_name+": "+str(field.round()))
        # print(convolution.round())
    plt.title("Match Results")
    plt.legend(title="Field:")
    plt.savefig('results.png')
    plt.close()
    
    print(conv_results.round())

    #conv_results = np.convolve(crop_results, kernel, mode="valid")
    #print("\nConvolution: "+str(conv_results))
    averages = np.average(results_matrix, axis=0) # get the averages
    difference = np.subtract(averages, expected_avg)
    weighted_avg = difference * weights # weight the averages
    
    total = np.clip(round(np.average(weighted_avg)+40), 0, 100) # clip value to 0-100

    return (team_data[0], total)
