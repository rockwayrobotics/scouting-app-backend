import numpy as np
from random import seed, randint
from .models import MatchResult

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

def fake_data(match_list):
    for i in match_list:
        i.auto_score = np.random.normal(loc=30.0, scale=10.0)
        i.auto_move = True
        i.teleop_score = np.clip(np.random.normal(loc=50.0, scale=25.0), 0, 75)
        i.endgame_score = np.clip(np.random.normal(loc=50, scale=45.0), 0, 150)
        i.penalty = randint(0,4)
        i.tippy = False
        i.disabled = False
        i.save()
    return match_list

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
        print(color.CYAN+color.UNDERLINE+
              "\nMatch #"+
              color.END+color.DARKCYAN+color.UNDERLINE+
              str(i.match_number)+
              color.END+
              "\n    auto_score: "+
              color.YELLOW+
              str(round(new_value[0]))+
              color.END+
              "\n    teleop_score: "+
              color.BLUE+
              str(round(new_value[1]))+
              color.END+
              "\n    final_score: "+
              color.PURPLE+
              str(round(new_value[2]))+
              color.END+
              "\n    penalities: "+
              color.RED+
              str(new_value[3])+
              color.END
              )
        results_matrix = np.append(
            results_matrix,
            [new_value],
            axis=0)

    return results_matrix

def generate_rank(team_data):
    results_matrix = team_data[1]

    weights = np.array([0.8, 1.3, 1.5, 4])
    print(results_matrix)

    #clipped = results_matrix[1:-1] # remove the oldest & most recent
    averages = np.average(results_matrix, axis=0) # get the averages
    weighted_avg = averages * weights # weight the averages
    weighted_avg[3] *= -1 # inverse because it counts against you
    
    total = round(weighted_avg.sum())

    return (team_data[0], total)
