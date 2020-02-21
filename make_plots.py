from get_data import get_data
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

years = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']

home_str = "game_outcome, pen_min, pen_min_opp, corsi_pct, fenwick_pct, faceoff_percentage, zs_offense_pct, pdo"
visitor_str = "pdo"

data = get_data(years, home_str, visitor_str)

variables = home_str.split(', ')
variables.extend(["opponent " + x for x in visitor_str.split(', ')])

# Mask to split wins and losses
game_outcome = data[:, :1]
mask = np.where(game_outcome == 1, True, False)

# Histograms of each variable split into wins and losses
for cnt, variable in enumerate(variables):
    column = data[:, cnt:cnt+1]
    plt.hist(column[mask], bins=20, label='Wins', color='red', density=1, histtype=u'step')
    plt.hist(column[~mask], bins=20, label='Losses', color='blue', density=1, histtype=u'step')
    plt.xlabel(variable)
    plt.ylabel("Count")
    plt.legend()
    plt.savefig("./plots/allteams_%s.png" % variable)
    plt.close()

# Correlation matrix
df = pd.DataFrame(data, columns=variables)
corr = df.corr()
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(corr, cmap='seismic', vmin=-1, vmax=1)
fig.colorbar(cax)
ticks = np.arange(0,len(variables), 1)
ax.set_xticks(ticks)
ax.set_yticks(ticks)
ax.set_xticklabels(variables, rotation='vertical')
ax.set_yticklabels(variables)
plt.savefig("./plots/allteams_correlations.png")