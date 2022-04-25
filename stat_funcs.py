# Set of functions for statistics. Main function to perform permutation tests for various statistical comparisons
from statistics import mean, stdev
from numpy import std, mean, sqrt
from statsmodels.stats.anova import AnovaRM
import numpy as np
from scipy import stats
from copy import deepcopy as dc
import matplotlib.pyplot as plt

# function to run permutation test for differences (subtraction between two means for instance)
def delta_paired(X, Y, reps):

    # convert input to numpy
    X = np.array(X)
    Y = np.array(Y)

    # initialize vector to hold statistic on each iteration
    rand_vals = list()

    # get observed statistic based on the test of interest
    print(X - Y)
    obs_stat = np.mean(X - Y)
    # concatenate data from both vars
    data_concat = np.array([X, Y])

    for ii in range(reps):

        print('\r{} of {}'.format(ii, reps), end='')
        # H: shuffle data along the rows (within-subject)
        [np.random.shuffle(x) for x in data_concat.T]
        rand = np.mean(data_concat[0, :] - data_concat[1, :])

        # push back R value
        rand_vals.append(rand)

    rand_vals = np.array(rand_vals)

    # look at probability on either side of the distribution based on the observed statistic - this function is
    # therefore order invariant with respect to its inputs
    prob = np.mean(np.abs(rand_vals) > np.abs(obs_stat))
    _ = plt.hist(rand_vals, bins='auto')  # arguments are passed to np.histogram
    plt.show()
    plt.axvline(obs_stat)

    print(f'p = {prob}')
    print(f'obs_stat = {obs_stat}')

    return obs_stat, prob

def shuffle_along_axis(a, axis):
    idx = np.random.rand(*a.shape).argsort(axis=axis)
    return np.take_along_axis(a,idx,axis=axis)

# function to run permutation test for differences in repeated ANOVA: (A-B) - (C-D)
def delta_paired_ANOVA(A_B, C_D, reps):

    # convert input to numpy
    A_B = np.array(A_B)
    C_D = np.array(C_D)

    # initialize vector to hold statistic on each iteration
    rand_vals = list()

    # get observed statistic based on the test of interest
    print(A_B[0])
    print(A_B[1])
    cond_1_diffs = A_B[0] - A_B[1]
    cond_2_diffs = C_D[0] - C_D[1]
    obs_stat = np.mean(cond_1_diffs - cond_2_diffs)

    # concatenate data from both vars
    data_concat = np.concatenate((A_B, C_D), axis=0)

    for ii in range(reps):

        data_concat_cp = np.copy(data_concat)
        print('\r{} of {}'.format(ii, reps), end='')
        # shuffle data and split into two random groups
        data_concat_cp = shuffle_along_axis(data_concat_cp, axis=0)
        data_concat_cp = shuffle_along_axis(data_concat_cp, axis=1) # THIS NEEDS TO BE MODIFIED, BREAKS UP THE SUBJECT STRUCTURE
        #random_split = np.split(data_concat_cp, 4)
        rand_1_diffs = data_concat_cp[0] - data_concat_cp[1]
        rand_2_diffs = data_concat_cp[2] - data_concat_cp[3]

        rand = np.mean(rand_1_diffs - rand_2_diffs)

        # push back R value
        rand_vals.append(rand)

    rand_vals = np.array(rand_vals)

    # look at probability on either side of the distribution based on the observed statistic - this function is
    # therefore order invariant with respect to its inputs
    prob = np.mean(np.abs(rand_vals) > np.abs(obs_stat))
    _ = plt.hist(rand_vals, bins='auto')  # arguments are passed to np.histogram
    plt.axvline(obs_stat)
    plt.show()

    print(f'p = {prob}')
    print(f'obs_stat = {obs_stat}')

    return obs_stat, prob



# Function to shuffle contents of a Panda structure
def shuffle_panda(df, n, axis=0):
    shuffled_df = df.copy()
    for k in range(n):
        shuffled_df.apply(np.random.shuffle(shuffled_df.values), axis=axis)
    return shuffled_df


# function to run permutation test for a variety of statistical comparisons. BehavMeasure ('RT' or 'PC'). stick with
# F-value here. Conds argument needs to be an array of size 1x2 (string labels)
def permtest_ANOVA_paired(data_panda, behavMeasure, Conds, reps):

    # initialize vector to hold statistic on each iteration
    rand_vals = list()

    # get observed statistics (interaction) for two-way ANOVA
    aovrm2way = AnovaRM(data_panda, behavMeasure, 'Subject_ID', within=Conds)
    results_table = aovrm2way.fit()
    F_vals = results_table.anova_table['F Value']

    # get observed interaction F-value: condition-task
    obs_stat = F_vals[2]

    # deep copy of panda structure
    shuffled_panda = data_panda.copy()

    # loop through repetitions
    for ii in range(reps):

        print('\r{} of {}'.format(ii, reps), end='')

        # H: shuffle column with behavioral measure of interest (PC or RT) WITHIN subject.
        # H: In essence, I am shuffling PC across conditions, but within subject
        shuffled_panda["behavMeasure_shuffled"] = shuffled_panda.groupby("Subject_ID")[behavMeasure].transform(np.random.permutation)

        # H: get randomized statistic (interaction) for two-way ANOVA
        aovrm2way_rand = AnovaRM(shuffled_panda, "behavMeasure_shuffled", 'Subject_ID', within=Conds)
        results_table_rand = aovrm2way_rand.fit()
        F_vals_rand = results_table_rand.anova_table['F Value']

        # get interaction F-value for shuffled structure: condition-task
        rand = F_vals_rand[2]

        # push back rand F value
        rand_vals.append(rand)

    rand_vals = np.array(rand_vals)

    # look at probability on either side of the distribution based on the observed statistic - this function is
    # therefore order invariant with respect to its inputs
    prob = np.mean(rand_vals > obs_stat)

    _ = plt.hist(rand_vals, bins='auto')  # arguments are passed to np.histogram
    plt.show()

    print(f'p = {prob}')
    print(f'obs_stat = {obs_stat}')

    return obs_stat, prob

# function to run permutation test for a pearson correlation
def perm_t_test_paired(X, Y, reps, one_sided=False):

    # convert input to numpy
    X = np.array(X)
    Y = np.array(Y)

    # initialize vector to hold statistic on each iteration
    rand_vals = list()

    # get observed statistic based on the test of interest
    observation = stats.ttest_rel(X, Y)
    obs_stat = observation[0]

    # concatenate data from both vars
    # before: data_concat = np.concatenate((X, Y), axis=0)
    data_concat = np.array([X, Y])

    for ii in range(reps):

        print('\r{} of {}'.format(ii, reps), end='')
        # H: shuffle data along the rows (within-subject), i.e. randomize (in-place) condition labels for each subject
        [np.random.shuffle(x) for x in data_concat.T]
        # before: random_split = np.split(data_concat, 2) # H: I got rid of this
        rand = stats.ttest_rel(data_concat[0,:], data_concat[1,:])
        rand = rand[0]
        # push back R value
        rand_vals.append(rand)

    rand_vals = np.array(rand_vals)

    # look at probability on either side of the distribution based on the observed statistic - this function is
    # therefore order invariant with respect to its inputs
    if not one_sided:
        prob = np.mean(np.abs(rand_vals) > np.abs(obs_stat))
    elif one_sided:
        if obs_stat > 0:
            prob = np.mean(rand_vals > obs_stat)
        else:
            prob = np.mean(rand_vals < obs_stat)

    _ = plt.hist(rand_vals, bins='auto')  # arguments are passed to np.histogram
    plt.axvline(obs_stat)
    plt.show()

    print(f'p = {prob}')
    print(f'obs_stat = {obs_stat}')

    return obs_stat, prob


# function to run permutation test for a pearson correlation
def permtest_spearman(X, Y, reps):

    # convert input to numpy
    X = np.array(X)
    Y = np.array(Y)

    # initialize vector to hold statistic on each iteration
    rand_vals = list()

    # get observed statistic based on the test of interest
    obs_stat = stats.spearmanr(X, Y)
    obs_stat = obs_stat[0]

    y_shuffled = dc(Y)

    for ii in range(reps):
        print('\r{} of {}'.format(ii, reps), end='')

        np.random.shuffle(y_shuffled)

        rand = stats.spearmanr(X, y_shuffled) # THIS WAS PEARSONR -> changing to spearman

        # push back R value
        rand_vals.append(rand[0])

    rand_vals = np.array(rand_vals)

    # look at probability on either side of the distribution based on the observed statistic (positive/negative
    # correlation)
    prob = np.mean(np.abs(rand_vals) > np.abs(obs_stat))

    _ = plt.hist(rand_vals, bins='auto')
    plt.show()

    print(f'p = {prob}')
    print(f'obs_stat = {obs_stat}')

    return obs_stat, prob

# function to run permutation test for a pearson correlation
def permtest_pearson(X, Y, reps):

    # convert input to numpy
    X = np.array(X)
    Y = np.array(Y)

    # initialize vector to hold statistic on each iteration
    rand_vals = list()

    # get observed statistic based on the test of interest
    obs_stat = stats.pearsonr(X, Y)
    obs_stat = obs_stat[0]

    y_shuffled = dc(Y)

    for ii in range(reps):
        print('\r{} of {}'.format(ii, reps), end='')

        np.random.shuffle(y_shuffled)

        rand = stats.pearsonr(X, y_shuffled)

        # push back R value
        rand_vals.append(rand[0])

    rand_vals = np.array(rand_vals)

    # look at probability on either side of the distribution based on the observed statistic (positive/negative
    # correlation)
    prob = np.mean(np.abs(rand_vals) > np.abs(obs_stat))

    _ = plt.hist(rand_vals, bins='auto')
    plt.show()

    print(f'p = {prob}')
    print(f'obs_stat = {obs_stat}')

    return obs_stat, prob

# function to run permutation test for differences (subtraction between two means for instance)
def perm_bias_paired(X, Y, reps):

    # convert input to numpy
    X = np.array(X)
    Y = np.array(Y)

    # initialize vector to hold statistic on each iteration
    rand_vals = list()

    # get observed statistic based on the test of interest
    observation = X - Y
    obs_stat = np.mean(observation)

    # concatenate data from both vars
    data_concat = np.concatenate((X, Y), axis=0)

    for ii in range(reps):

        print('\r{} of {}'.format(ii, reps), end='')

        # shuffle data and split into two random groups
        np.random.shuffle(data_concat)
        random_split = np.split(data_concat, 2)

        rand = np.mean(random_split[0] - random_split[1])

        # push back R value
        rand_vals.append(rand)

    rand_vals = np.array(rand_vals)

    # look at probability on either side of the distribution based on the observed statistic - this function is
    # therefore order invariant with respect to its inputs
    prob = np.mean(np.abs(rand_vals) > np.abs(obs_stat))

    _ = plt.hist(rand_vals, bins='auto')  # arguments are passed to np.histogram
    plt.show()

    print(f'p = {prob}')
    print(f'obs_stat = {obs_stat}')

    return obs_stat, prob


# Compute cohen's d for unpaired t-test
def cohen_d(x, y):

    nx = len(x)
    ny = len(y)
    dof = nx + ny - 2
    return (mean(x) - mean(y)) / sqrt(((nx - 1) * std(x) ** 2 + (ny - 1) * std(y) ** 2) / dof)


# Compute cohen's d for paired t-test
def cohen_d_av(x, y):

    return (mean(x) - mean(y)) / ((stdev(x) + stdev(y)) / 2)
