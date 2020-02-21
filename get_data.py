import mysql.connector
import numpy as np
import db_config as dbcfg


sql_db = mysql.connector.connect(
    host=dbcfg.host,
    user=dbcfg.user,
    passwd=dbcfg.passwd,
    database=dbcfg.database
)
sql_cursor = sql_db.cursor()

teams = {'Tampa Bay Lightning': 'TBL',
         'Boston Bruins': 'BOS',
         'Toronto Maple Leafs': 'TOR',
         'Montreal Canadiens': 'MTL',
         'Florida Panthers': 'FLA',
         'Buffalo Sabres': 'BUF',
         'Detroit Red Wings': 'DET',
         'Ottawa Senators': 'OTT',
         'Washington Capitals': 'WSH',
         'New York Islanders': 'NYI',
         'Pittsburgh Penguins': 'PIT',
         'Carolina Hurricanes': 'CAR',
         'Columbus Blue Jackets': 'CBJ',
         'Philadelphia Flyers': 'PHI',
         'New York Rangers': 'NYR',
         'New Jersey Devils': 'NJD',
         'Winnipeg Jets': 'WPG',
         'Atlanta Thrashers': 'WPG',  # The Thrashers moved to Winnipeg at the start of the 2012 season
         'Nashville Predators': 'NSH',
         'St. Louis Blues': 'STL',
         'Dallas Stars': 'DAL',
         'Minnesota Wild': 'MIN',
         'Chicago Blackhawks': 'CHI',
         'Colorado Avalanche': 'COL',
         'Calgary Flames': 'CGY',
         'San Jose Sharks': 'SJS',
         'Las Vegas Golden Knights': 'VEG',
         'Vegas Golden Knights': 'VEG',  # Data is inconsistent about Las Vegas vs. Vegas
         'Arizona Coyotes': 'ARI',
         'Edmonton Oilers': 'EDM',
         'Vancouver Canucks': 'VAN',
         'Anaheim Ducks': 'ANA',
         'Los Angeles Kings': 'LAK'}


def get_data(years, home_str, visitor_str=""):
    data = list()
    for year in years:
        sql_cursor.execute("SELECT * FROM nhl_schedule_%s" % year)
        schedule = list(sql_cursor.fetchall())
        for game in schedule:
            date = game[1]
            visitor = teams[game[2]].lower()
            home = teams[game[3]].lower()
            sql_cursor.execute(
                "SELECT %s FROM nhl_gamelog_%s WHERE date_game = '%s' LIMIT 1" % (home_str, home, date))
            sql_data = sql_cursor.fetchall()
            if len(sql_data) < 1:
                continue
            data_point = list(sql_data[0])
            if visitor_str:
                sql_cursor.execute(
                    "SELECT %s FROM nhl_gamelog_%s WHERE date_game = '%s' LIMIT 1" % (visitor_str, visitor, date))
                sql_data = sql_cursor.fetchall()
                if len(sql_data) < 1:
                    continue
                data_point.extend(list(sql_data[0]))
            data.append(data_point)
    return np.array(data)
