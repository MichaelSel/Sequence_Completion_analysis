import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import formats

from csv_to_pandas import csv_to_pandas


plotting_dir = './analyzed'

def change_width(ax, new_value) :
    for patch in ax.patches :
        current_width = patch.get_width()
        diff = current_width - new_value

        # we change the bar width
        patch.set_width(new_value)

        # we recenter the bar
        patch.set_x(patch.get_x() + diff * .5)

def violins_chromatic_v_diatonic(partition, data,x,y,name=""):
    n_groups = len(data.groupby(partition))
    fig, axes = plt.subplots(ncols=n_groups, sharex=True, sharey=True)
    fig.suptitle(name, fontsize=16)

    for ax, (n,grp) in zip(axes, data.groupby(partition)):
        # sns.violinplot(x=x, y=y, data=grp, ax=ax, palette=['green','purple'], inner="stick")
        # sns.violinplot(x=x, y=y, data=grp, ax=ax, inner="box")

        sns.barplot(x=x, y=y, data=grp, ax=ax, palette=['#A64669', '#9688F2'])
        # sns.stripplot(x=x, y=y, data=grp, palette=['black'], ax=ax)

        # sns.pointplot(x=x, y=y, hue="subject", data=grp,
        #               palette=["black"], ax=ax)
        ax.set_title(n)
    for ax in axes:
        try:
            ax.get_legend().remove()
        except:
            1+1
    # plt.ylim(0.9, 1.1)
    # plt.ylim(800, 2750)
    plt.savefig('plots/' + name + ".svg")
    plt.show()

def bars_contour_v_pitch(partition, data,x,y,name=""):
    n_groups = len(data.groupby(partition))
    fig, axes = plt.subplots(ncols=n_groups, sharex=True, sharey=True,figsize=[3,8])
    fig.suptitle(name, fontsize=16)
    for ax, (n,grp) in zip(axes, data.groupby(partition)):
        # print(grp.head())
        sns.barplot(x=x, y=y, data=grp,ax=ax)
        sns.stripplot(x=x, y=y, data=grp,palette=['black'],ax=ax)
        # change_width(ax, .35)

        ax.set_title(n)
    for i,ax in enumerate(axes):
        try:
            if(i>0): ax.set_ylabel('')
            ax.set_xlabel('')
            ax.set(xticklabels=[''])
            ax.get_legend().remove()
        except:
            1+1
    plt.show()




format_general = formats.general()
format_conf = formats.confidence()

seq_gen = csv_to_pandas(plotting_dir + "/seq_results.csv",format_general)
seq_gen = seq_gen.loc[seq_gen['excluded'] == 'False']
seq_gen['d-prime'] = seq_gen['d-prime'].astype('float')
violins_chromatic_v_diatonic('type',seq_gen,x='type',y='d-prime',name="D'")
# violins_chromatic_v_diatonic('type',seq_gen,x='type',y='confidence_correct',name="confidence")

seq_conf = csv_to_pandas(plotting_dir + "/seq_results.csv",format_conf)
seq_conf['conf_correct_d:c'] = seq_conf['conf_correct_d:c'].astype('float')
sns.barplot(data=seq_conf,y='conf_correct_d:c')
plt.show()



