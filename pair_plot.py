import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


data_dir = './analyzed/'
data_completion = pd.read_csv(data_dir + 'seq_results.csv')
data_completion = data_completion[data_completion['excluded'] == False]
data_completion = data_completion[data_completion['d-prime'] > 0]
data_completion = data_completion.reset_index()
columns = ['diatonic_d-prime','chromatic_d-prime']
df = data_completion
df = df[columns]



jitter = 0.05
df_x_jitter = pd.DataFrame(np.random.normal(loc=0, scale=jitter, size=df.values.shape), columns=columns)
df_x_jitter += np.arange(len(columns))

fig, ax = plt.subplots()
for col in df:
    ax.plot(df_x_jitter[col], df[col], 'o', alpha=.40, zorder=1, ms=8, mew=1)
    # ax.set_xticks(range(len(df.columns)))
    # ax.set_xticklabels(df.columns)
    # ax.set_xlim(-0.5,len(df.columns)-0.5)

for idx in df.index:
    ax.plot(df_x_jitter.loc[idx,columns], df.loc[idx,columns], color = 'grey', linewidth = 0.5, linestyle = '--', zorder=-1)

plt.show()