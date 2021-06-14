
import random

def setParameter(paramStr,defaultValue):
# Do not change this function

    '''This function takes as input a string paramStr and a float or 
    int defaultValue.  If paramStr is the empty string, the function 
    returns the value of defaultValue.  If paramStr is not the empty
    string, the function returns the float or integer associated with 
    the string, according to the type of defaultValue.

    param paramStr: a string
    param defaultValue: can be either a float or an int
    '''
    if paramStr == "":
        return defaultValue
    else:
        if type(defaultValue) == int:
            return int(paramStr)
        else:            
            return float(paramStr)

def runTrial(beta,kappa,S0,Z0,survivors):
# You will need to fill in the code for this function

    ''' This function simulates a single trial, where a trial is a
    simulation of the zombie model which starts with S0 susceptibles
    and Z_0 zombies, and proceeds until either the humans win (Z=0) or
    the zombies win (S=0).  The input parameters S0, Z0, beta, and kappa 
    are model parameters.  The input parameter survivors is a list 
    containing the number of human survivors for all trials so far for 
    which there is a positive number.  If the zombies win, the function 
    returns the string "zombies".  If the humans win, the function returns 
    the string "humans"

    param beta: a float giving the rate of zombie infection
    param kappa: a float giving the rate at which zombies are killed
    param S0: an integer giving the initial number of humans
    param Z0: an integer giving the initial number of zombies
    param survivors: a list of integers containing the number of human
     survivors for all trials so far for which there is a positive
     number; note that this is mutable
    '''
    dt = 0.001
    while (S0 != 0) and (Z0 != 0):
        r = random.random()
        prob_hum = beta*S0*Z0*dt
        prob_zom = kappa*S0*Z0*dt
        if r < prob_hum:
            S0 = S0 - 1
            Z0 = Z0 + 1
        elif r > 1 - prob_zom:
            Z0 = Z0 - 1
        else:
            continue
    
    if Z0 == 0:
        survivors.append(S0)
        return("humans")
    else:
        return("zombies")
    
    
# Dictionary which contains default values for the model parameters
# Do not change this dictionary
default = {
    "beta":0.01,
    "kappa":0.008,
    "S0":190,
    "Z0":10,
    "numtrials":100
}
# Main Program

ans = input("Would you like to use the default values for model parameters? (y or n): ")

if ans == 'y':   # use default values for model parameters;
# the values should be accessed from the dictionary called default
    beta = default["beta"]
    kappa = default["kappa"]
    S0 = default["S0"]
    Z0 = default["Z0"]
    numtrials = default["numtrials"]
else:
    beta_str = input("Enter value for beta (Press return for beta = {}): "\
                     .format(default["beta"]))
    beta = setParameter(beta_str, default["beta"])   # this needs to be filled in

# do similar commands to set the values for kappa, S0, Z0, and numtrials
    
    # kappa variable user input
    kappa_str = input("Enter value for kappa (Press return for kappa = {}): "\
                     .format(default["kappa"]))
    kappa = setParameter(kappa_str, default["kappa"])
    
    # S0 variable user input
    S0_str = input("Enter value for S0 (Press return for S0 = {}): "\
                     .format(default["S0"]))
    S0 = setParameter(S0_str, default["S0"])
    
    # Z0 variable user input
    Z0_str = input("Enter value for Z0 (Press return for Z0 = {}): "\
                     .format(default["Z0"]))
    Z0 = setParameter(Z0_str, default["Z0"])
    
    # numtrials variable user input
    numtrials_str = input("Enter value for numtrials (Press return for numtrials = {}): "\
                     .format(default["numtrials"]))
    numtrials = setParameter(numtrials_str, default["numtrials"])
    
    
# Here you'll do numtrials simulations of the zombie apocalypse, keeping
# track of how many times the humans win.  Think of this as a Monte Carlo
# simulation, as discussed in lecture.

winners = []
survivors = []
for i in range(numtrials):
    trial_result = runTrial(beta,kappa,S0,Z0,survivors)
    winners.append(trial_result)

# calculate and print the percent chance that the humans win, in the
# format given in the problem statement
# If appropriate according to the problem statement, print
# "Yikes!"
# "Sorry, doesn't look good for the humans!"
# "It's a toss-up!"
# or "Looks good for the humans!"
human_wins = winners.count("humans")

if numtrials > 0:
    human_pert_win = human_wins*100/numtrials
    print("Chance that humans survive is {:.2f}%".format(human_pert_win))
    if human_pert_win == 0.0:
        print("Yikes!")
    elif (human_pert_win > 0.0) and (human_pert_win < 10.0):
        print("Sorry, doesn’t look good for the humans!")
    elif (human_pert_win >= 40.0) and (human_pert_win <= 60.0):
        print("It’s a toss-up!")
    elif human_pert_win > 90.0:
        print("Looks good for the humans!")
else:
    print("No trials run as per user input")

# If there was at least one trial for which at least one human survived, print
# the average number of suvivors in the format given in the problem statment
if sum(survivors) == 0:
    avg_hum_surv = 0.0
else:
    avg_hum_surv = sum(survivors)/len(survivors)
print("If humans survive, the average number of survivors is {:.2f} out of {}".format(avg_hum_surv, S0))
    
    