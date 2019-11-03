from sportsreference.ncaab.boxscore import Boxscores, Boxscore
from datetime import date, timedelta
import os
import csv


def change_directory(folder):
    #Change Databse Directory
    dirpath = os.getcwd()
    dirpath = dirpath + folder
    os.chdir(dirpath)

def database(path, item_list):
    #Writes Players to CSV file
    with open(path + '.csv', 'a', newline='') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerow(item_list)

def database_reader(current_file, head_list):
    #Read Database Files
    database_players = []
    with open(current_file) as csvfile:
        reader = csv.DictReader(csvfile)
        #Reads rows of CSV file
        for row in reader:
            index = 0
            player_list = []
            #Sets row to proper information
            while index < len(row):
                player_list.append(row[head_list[index]])
                index += 1
            database_players.append(player_list)
    return(database_players)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

#Stores old directory and changes current
first_directory = os.getcwd()
change_directory('/Database/')
"""
game_list = ['Date','Home','Away','H Score','A Score',
             'H FG A','A FG A','H FG M','A FG M',
             'H FT A','A FT A','H FT M','A FT M',
             'H 3P A','A 3P A','H 3P M','A 3P M',
             'H TURN','A TURN',
             'H OREB','A OREB','H DREB','A DREB']
"""
game_list = ['Date','Home','Away','H Score','A Score','ID']

fix_list = ['VI','CBB Reference','SBR 1','SBR 2','SBR 3','SBR 4','NC','Massey','Team Link','Ret Min','Schedule']
fix_log = database_reader('CBB-Team-Fix.csv', fix_list)

database('CBB-Boxscore-Database', game_list)

start_date = date(2010, 11, 1)
end_date = date(2019, 4, 30)
for date in daterange(start_date, end_date):
    if date.month >= 11 or date.month <= 4:
        games = Boxscores(date)
        game_list[0] = date.strftime("%m-%d-%Y")
        for f_key, f_value in games.games.items():
            for current_dict in f_value:
                #game_list = ['','','','','','','','','','','','','','','','','','','','','','','']
                for s_key, s_value in current_dict.items():
                    #print(s_key,s_value)
                    if s_key == 'home_name':
                        game_list[1] = s_value
                    elif s_key == 'away_name':
                        game_list[2] = s_value
                    elif s_key == 'home_score':
                        game_list[3] = s_value
                    elif s_key == 'away_score':
                        game_list[4] = s_value
                    elif s_key == 'boxscore':
                        game_list[5] = s_value
                    """
                    elif s_key == 'boxscore':
                        game_data = Boxscore(s_value)

                        game_list[0] = game_data.date
                        game_list[5] = game_data.home_field_goal_attempts
                        game_list[6] = game_data.away_field_goal_attempts
                        game_list[7] = game_data.home_field_goals
                        game_list[8] = game_data.away_field_goals
                        game_list[9] = game_data.home_free_throw_attempts
                        game_list[10] = game_data.away_free_throw_attempts
                        game_list[11] = game_data.home_free_throws
                        game_list[12] = game_data.away_free_throws
                        game_list[13] = game_data.home_three_point_field_goal_attempts
                        game_list[14] = game_data.away_three_point_field_goal_attempts
                        game_list[15] = game_data.home_three_point_field_goals
                        game_list[16] = game_data.away_three_point_field_goals
                        game_list[17] = game_data.home_turnovers
                        game_list[18] = game_data.away_turnovers
                        game_list[19] = game_data.home_offensive_rebounds
                        game_list[20] = game_data.away_offensive_rebounds
                        game_list[21] = game_data.home_defensive_rebounds
                        game_list[22] = game_data.away_defensive_rebounds
                        print(game_list)
                    """

                if game_list[1] == '':
                    game_data = Boxscore(game_list[5])
                    if game_list[3] < game_list[4]:
                        game_list[1] = game_data.losing_name
                    elif game_list[3] > game_list[4]:
                        game_list[1] = game_data.winning_name

                for tfix in fix_log:
                    if game_list[1] == tfix[1]:
                        game_list[1] = tfix[0]
                    elif game_list[2] == tfix[1]:
                        game_list[2] = tfix[0]
                        
                database('CBB-Boxscore-Database', game_list)
