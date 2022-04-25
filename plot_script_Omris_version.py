import pandas as pd
import numpy as np
import seaborn as sns
from stat_funcs import *
import matplotlib as plt

data_dir = './analyzed/'

data_completion = pd.read_csv(data_dir + 'seq_results.csv')
reps = 10000

# H: analyze only nonexcluded participants
data_completion_AC = data_completion[data_completion.excluded == False]
data_completion_AC = data_completion_AC[data_completion_AC['d-prime'] > 0]

data_completion_AC["musical_training"].replace({"9+": "9"}, inplace=True)
data_completion_AC['musical_training'] = data_completion_AC['musical_training'].astype(int)

# H: Remove subjects with more than 0 yrs of musical training and less than 5 yrs
data_completion_AC_Music = data_completion_AC.loc[(data_completion_AC['musical_training']==0) | (data_completion_AC['musical_training']>4)]

data_completion_AC_Music['musician'] = False
data_completion_AC_Music['musician'] = data_completion_AC_Music['musical_training'] >= 5

data_completion_AC_NonMusicians = data_completion_AC.loc[data_completion_AC['musical_training']==0]
data_completion_AC_Musicians = data_completion_AC.loc[data_completion_AC['musical_training']>4]

# H: plot diatonic versus chromatic d-prime (entire cohort)
sns.set_context("talk")
d_prime_AC_reform = pd.melt(data_completion_AC, value_vars=['diatonic_d-prime', 'chromatic_d-prime'])
ax = sns.boxplot(x="variable", y="value", data=d_prime_AC_reform, saturation=.5)
sns.despine()
sns.set_context("talk")
plt.show()
delta_paired(X, Y, reps)

# H: plot diatonic versus chromatic d-prime (musicians vs. non-musicians)
fig, ax = plt.subplots()
sns.set_style("ticks")
sns.set_context("talk")
data_confab_AC_reform_FA_rate = pd.melt(data_completion_AC_Music, id_vars=['musician'], value_vars=['diatonic_d-prime', 'chromatic_d-prime'])
sns.barplot(x="musician", y="value", hue="variable", data=data_confab_AC_reform_FA_rate, ax=ax, color=".9")
sns.stripplot(x="musician", y="value", hue="variable", data=data_confab_AC_reform_FA_rate, ax=ax, dodge=True, palette="Set2", size=13,
              marker=".", edgecolor="gray", alpha=.15)
#ax.set_ylim(0, .9)
sns.despine()
plt.legend([],[], frameon=False)
plt.show()

delta_paired(data_completion_AC['diatonic_d-prime'], data_completion_AC['chromatic_d-prime'], 10000)
delta_paired(data_completion_AC_Musicians['diatonic_d-prime'], data_completion_AC_Musicians['chromatic_d-prime'], 10000)
delta_paired(data_completion_AC_NonMusicians['diatonic_d-prime'], data_completion_AC_NonMusicians['chromatic_d-prime'], 10000)

# H: plot diatonic versus chromatic HITS (musicians vs. non-musicians)
fig, ax = plt.subplots()
sns.set_style("ticks")
sns.set_context("talk")
data_confab_AC_reform_FA_rate = pd.melt(data_completion_AC_Music, id_vars=['musician'], value_vars=['diatonic_d-prime', 'chromatic_d-prime'])
sns.barplot(x="musician", y="value", hue="variable", data=data_confab_AC_reform_FA_rate, ax=ax, color=".9")
sns.stripplot(x="musician", y="value", hue="variable", data=data_confab_AC_reform_FA_rate, ax=ax, dodge=True, palette="Set2", size=13,
              marker=".", edgecolor="gray", alpha=.15)
#ax.set_ylim(0, .9)
sns.despine()
plt.legend([],[], frameon=False)
plt.show()

delta_paired(data_completion_AC['diatonic_d-prime'], data_completion_AC['chromatic_d-prime'], 10000)
delta_paired(data_completion_AC_Musicians['diatonic_d-prime'], data_completion_AC_Musicians['chromatic_d-prime'], 10000)
delta_paired(data_completion_AC_NonMusicians['diatonic_d-prime'], data_completion_AC_NonMusicians['chromatic_d-prime'], 10000)


