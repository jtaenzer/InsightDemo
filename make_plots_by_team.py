import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import db_config as dbcfg
import os

try:
    os.mkdir("%s/plots" % os.getcwd())
except OSError:
    pass

sql_db = mysql.connector.connect(
    host=dbcfg.host,
    user=dbcfg.user,
    passwd=dbcfg.passwd,
    database=dbcfg.database
)
sql_cursor = sql_db.cursor()

teams = ['PIT', 'WSH', 'PHI', 'CAR', 'NYI', 'CBJ', 'NYR', 'NJD', 'BOS', 'TBL', 'TOR', 'FLA', 'BUF', 'MTL', 'OTT', 'DET',
         'STL', 'DAL', 'COL', 'WPG', 'NSH', 'MIN', 'CHI', 'EDM', 'VEG', 'VAN', 'CGY', 'ARI', 'SJS', 'ANA', 'LAK']

sql_str = "game_outcome, pen_min, pen_min_opp, corsi_pct, fenwick_pct, faceoff_percentage, zs_offense_pct, pdo"
variables = sql_str.split(', ')

for team in teams:
    sql_cursor.execute("SELECT %s FROM nhl_gamelog_%s" % (sql_str, team))
    data = np.array(sql_cursor.fetchall())
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
        plt.savefig("./plots/%s_%s.png" % (team, variable))
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
    plt.savefig("./plots/%s_correlations.png" % team)
    plt.close()