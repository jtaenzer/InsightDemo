import mysql.connector
import requests
from bs4 import BeautifulSoup

import db_config as dbcfg

sql_db = mysql.connector.connect(
    host=dbcfg.host,
    user=dbcfg.user,
    passwd=dbcfg.passwd,
    database=dbcfg.database
)
sql_cursor = sql_db.cursor()

teams = ['PIT', 'WSH', 'PHI', 'CAR', 'NYI', 'CBJ', 'NYR', 'NJD', 'BOS', 'TBL', 'TOR', 'FLA', 'BUF', 'MTL', 'OTT', 'DET',
         'STL', 'DAL', 'COL', 'WPG', 'NSH', 'MIN', 'CHI', 'EDM', 'VEG', 'VAN', 'CGY', 'ARI', 'SJS', 'ANA', 'LAK']
years = ['2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']

##############################
### CREATE SCHEDULE TABLES ###
##############################
if dbcfg.schedule:
    for year in years:
        table_name = "nhl_schedule_%s" % year
        try:
            sql_cursor.execute("CREATE TABLE %s \
                                (game_id INT PRIMARY KEY, \
                                date_game DATE, \
                                visitor_team_name VARCHAR(255), \
                                home_team_name VARCHAR(255))" % table_name)
        except mysql.connector.errors.ProgrammingError as err:
            print("%s.%s table may already exist:" %(dbcfg.database, table_name), err)

        schedule_page = requests.get("https://www.hockey-reference.com/leagues/NHL_%s_games.html" % year)
        soup = BeautifulSoup(schedule_page.content, "html.parser")
        val_list = []

        for cnt, row in enumerate(soup.findAll('tr')):
            date_game = row.find('th', attrs={'data-stat': 'date_game'}).text
            visitor = ""
            for child in row.findChildren('td', attrs={'data-stat': 'visitor_team_name'}):
                visitor = child.text
                visitor = visitor.replace("Phoenix", "Arizona")
            home = ""
            for child in row.findChildren('td', attrs={'data-stat': 'home_team_name'}):
                home = child.text
                home = home.replace("Phoenix", "Arizona")
            if not visitor or not home:
                continue
            val_list.append((cnt, date_game, visitor, home))
        sql_str = "INSERT IGNORE INTO " + table_name + " (game_id, date_game, visitor_team_name, home_team_name) \
                   VALUES (%s, %s, %s, %s)"
        sql_cursor.executemany(sql_str, val_list)
        sql_db.commit()
        print("Inserted %s rows into %s" % (str(sql_cursor.rowcount), table_name))

##################################
### CREATE TEAM GAMELOG TABLES ###
##################################
if dbcfg.team_gamelog:
    for team in teams:
        table_name = "nhl_gamelog_%s" % team
        try:
            sql_cursor.execute("CREATE TABLE %s \
                                (date_game DATE PRIMARY KEY, \
                                opp_name VARCHAR(255), \
                                goals INT, \
                                opp_goals INT, \
                                game_outcome INT, \
                                overtimes VARCHAR(255), \
                                shots INT, \
                                pen_min INT, \
                                goals_pp INT, \
                                chances_pp INT, \
                                goals_sh INT, \
                                shots_against INT, \
                                pen_min_opp INT, \
                                goals_against_pp INT, \
                                opp_chances_pp INT, \
                                goals_against_sh INT, \
                                corsi_for INT, \
                                corsi_against INT, \
                                corsi_pct FLOAT, \
                                fenwick_for INT, \
                                fenwick_against INT, \
                                fenwick_pct FLOAT, \
                                faceoff_wins INT, \
                                faceoff_losses INT, \
                                faceoff_percentage FLOAT, \
                                zs_offense_pct FLOAT, \
                                pdo FLOAT)" % table_name)
        except mysql.connector.errors.ProgrammingError as err:
            print("%s.%s table may already exist:" % (dbcfg.database, table_name), err)
        val_list = []
        for year in years:
            url = "https://www.hockey-reference.com/teams/%s/%s_gamelog.html" % (team, year)
            if team == "ARI" and int(year) < 2015:
                url = "https://www.hockey-reference.com/teams/PHX/%s_gamelog.html" % year
            if team == "WPG" and int(year) < 2012:
                url = "https://www.hockey-reference.com/teams/ATL/%s_gamelog.html" % year
            gamelog_page = requests.get(url)
            soup = BeautifulSoup(gamelog_page.content, "html.parser")
            for row in soup.findAll('tr', attrs={'id': [lambda x: x.startswith('tm_gamelog_')]}):
                # Find game_outcome out of order so we can skip unplayed games
                game_outcome = row.find('td', attrs={'data-stat': 'game_outcome'}).text
                if not game_outcome:
                    continue
                game_outcome_int = 1 if game_outcome == 'W' else 1
                date_game = row.find('td', attrs={'data-stat': 'date_game'}).text
                game_location = row.find('td', attrs={'data-stat': 'game_location'}).text
                opp_name = row.find('td', attrs={'data-stat': 'opp_name'}).text
                goals = row.find('td', attrs={'data-stat': 'goals'}).text
                if not goals:
                    goals = 0
                opp_goals = row.find('td', attrs={'data-stat': 'opp_goals'}).text
                if not opp_goals:
                    opp_goals = 0
                overtimes = row.find('td', attrs={'data-stat': 'overtimes'}).text
                shots = row.find('td', attrs={'data-stat': 'shots'}).text
                if not shots:
                    shots = 0
                pen_min = row.find('td', attrs={'data-stat': 'pen_min'}).text
                if not pen_min:
                    pen_min = 0
                goals_pp = row.find('td', attrs={'data-stat': 'goals_pp'}).text
                if not goals_pp:
                    goals_pp = 0
                chances_pp = row.find('td', attrs={'data-stat': 'chances_pp'}).text
                if not chances_pp:
                    chances_pp = 0
                goals_sh = row.find('td', attrs={'data-stat': 'goals_sh'}).text
                if not goals_sh:
                    goals_sh = 0
                shots_against = row.find('td', attrs={'data-stat': 'shots_against'}).text
                if not shots_against:
                    shots_against = 0
                pen_min_opp = row.find('td', attrs={'data-stat': 'pen_min_opp'}).text
                if not pen_min_opp:
                    pen_min_opp = 0
                goals_against_pp = row.find('td', attrs={'data-stat': 'goals_against_pp'}).text
                if not goals_against_pp:
                    goals_against_pp = 0
                opp_chances_pp = row.find('td', attrs={'data-stat': 'opp_chances_pp'}).text
                if not opp_chances_pp:
                    opp_chances_pp = 0
                goals_against_sh = row.find('td', attrs={'data-stat': 'goals_against_sh'}).text
                if not goals_against_sh:
                    goals_against_sh = 0
                corsi_for = row.find('td', attrs={'data-stat': 'corsi_for'}).text
                if not corsi_for:
                    corsi_for = 0
                corsi_against = row.find('td', attrs={'data-stat': 'corsi_against'}).text
                if not corsi_against:
                    corsi_against = 0
                corsi_pct = row.find('td', attrs={'data-stat': 'corsi_pct'}).text
                if not corsi_pct:
                    corsi_pct = 0
                fenwick_for = row.find('td', attrs={'data-stat': 'fenwick_for'}).text
                if not fenwick_for:
                    fenwick_for = 0
                fenwick_against = row.find('td', attrs={'data-stat': 'fenwick_against'}).text
                if not fenwick_against:
                    fenwick_against = 0
                fenwick_pct = row.find('td', attrs={'data-stat': 'fenwick_pct'}).text
                if not fenwick_pct:
                    fenwick_pct = 0
                faceoff_wins = row.find('td', attrs={'data-stat': 'faceoff_wins'}).text
                if not faceoff_wins:
                    faceoff_wins = 0
                faceoff_losses = row.find('td', attrs={'data-stat': 'faceoff_losses'}).text
                if not faceoff_losses:
                    faceoff_losses = 0
                faceoff_percentage = row.find('td', attrs={'data-stat': 'faceoff_percentage'}).text
                if not faceoff_percentage:
                    faceoff_percentage = 0
                zs_offense_pct = row.find('td', attrs={'data-stat': 'zs_offense_pct'}).text
                if not zs_offense_pct:
                    zs_offense_pct = 0
                pdo = row.find('td', attrs={'data-stat': 'pdo'}).text
                if not pdo:
                    pdo = 0
                val_str = (date_game, opp_name, int(goals), int(opp_goals), game_outcome_int, overtimes, int(shots),
                           int(pen_min), int(goals_pp), int(chances_pp), int(goals_sh), int(shots_against),
                           int(pen_min_opp), int(goals_against_pp), int(opp_chances_pp), int(goals_against_sh),
                           int(corsi_for), int(corsi_against), float(corsi_pct), int(fenwick_for), int(fenwick_against),
                           float(fenwick_pct), int(faceoff_wins), int(faceoff_losses), float(faceoff_percentage),
                           float(zs_offense_pct), float(pdo))
                val_list.append(val_str)
        sql_str = "INSERT IGNORE INTO " + table_name.lower() + \
                  "(date_game, \
                    opp_name, \
                    goals, \
                    opp_goals, \
                    game_outcome, \
                    overtimes, \
                    shots, \
                    pen_min, \
                    goals_pp, \
                    chances_pp, \
                    goals_sh, \
                    shots_against, \
                    pen_min_opp, \
                    goals_against_pp, \
                    opp_chances_pp, \
                    goals_against_sh, \
                    corsi_for, \
                    corsi_against, \
                    corsi_pct, \
                    fenwick_for, \
                    fenwick_against, \
                    fenwick_pct, \
                    faceoff_wins, \
                    faceoff_losses, \
                    faceoff_percentage, \
                    zs_offense_pct, \
                    pdo) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        sql_cursor.executemany(sql_str, val_list)
        sql_db.commit()
        print("Inserted %s rows into %s" % (str(sql_cursor.rowcount), table_name))