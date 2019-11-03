import requests
import bs4
import re
import csv
import os
import wget

first_dir = os.getcwd()
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


change_directory('\\Database\\')

game_data = ['Date','Type','Home Team','Home Score','Away Team','Away Score','Venue',
             'H ADJ O','H ADJ D','H OFF PPP','H OFF EFG%','H OFF TO%','H OFF REB%','H OFF FTR','H DEF PPP','H DEF EFG%','H DEF TO%','H DEF REB%','H DEF FTR',
             'A ADJ O','A ADJ D','A OFF PPP','A OFF EFG%','A OFF TO%','A OFF REB%','A OFF FTR','A DEF PPP','A DEF EFG%','A DEF TO%','A DEF REB%','A DEF FTR',
             'Tempo','ID','Home Coach','Away Coach']
database('CBB-Game-Database', game_data)

fix_list = ['VI','CBB Reference','SBR 1','SBR 2','SBR 3','SBR 4','NC','Massey','Team Link','Ret Min','Schedule']
fix_log = database_reader('CBB-Team-Fix.csv', fix_list)

### File Link: http://www.barttorvik.com/getgamestats.php?year=2018&csv=1

head_list = ['Date','Type','Team','Conf','Opponent','Venue','Result',
             'ADJ O','ADJ D','OFF PPP','OFF EFG%','OFF TO%','OFF REB%','OFF FTR',
             'DEF PPP','DEF EFG%','DEF TO%','DEF REB%','DEF FTR',
             'G-SC','OPP Conf','OPP #','Season','Tempo','ID','Team Coach','OPP Coach','"+/-"','Rank','List']

for year in range(2010,2021):
    change_directory('\\Barttorvik\\')
    if year == 2020:
        if os.path.exists(str(year) + ' game stats.csv'):
            os.remove(str(year) + ' game stats.csv')
        database(str(year) + ' game stats', head_list)
        url = "http://www.barttorvik.com/getgamestats.php?year=2020&csv=1"
        wget.download(url, 'temp game stats.csv')
        for line in open('temp game stats.csv'):
            open(str(year) + ' game stats.csv',"a").write(line)
        os.remove('temp game stats.csv')
    game_log = database_reader(str(year) + ' game stats.csv', head_list)
    os.chdir(first_dir)
    change_directory('\\Database\\')
    no_fly = []
    for game in game_log:
        if game[24] not in no_fly:
            game_data = [game[0],game[1],'','','','',game[5],'','','','','','','','','','','','','','','','','','','','','','','','',game[23],game[24],'','']
            score = game[6][3:]
            score = score.split('-')
            if 'W' in game[6]:
                team_score = score[0]
                opp_score = score[1]
            elif 'L' in game[6]:
                team_score = score[1]
                opp_score = score[0]
            if game[5] == 'A':
                game_data[4] = game[2]
                game_data[2] = game[4]
                game_data[5] = team_score
                game_data[3] = opp_score
                game_data[34] = game[25]
                game_data[33] = game[26]
                mult = 7
            elif game[5] == 'H' or game[5] == 'N':
                game_data[2] = game[2]
                game_data[4] = game[4]
                game_data[3] = team_score
                game_data[5] = opp_score
                game_data[33] = game[25]
                game_data[34] = game[26]
                mult = 19
            for num in range(0,12):
                data_mult = num + mult
                game_mult = 7 + num
                game_data[data_mult] = game[game_mult]
            for game2 in game_log:
                if game2[24] == game[24] and game2[2] == game[4]:
                    if mult == 7:
                        mult = 19
                    elif mult == 19:
                        mult = 7
                    for num in range(0,12):
                        data_mult = num + mult
                        game_mult = 7 + num
                        game_data[data_mult] = game2[game_mult]
            no_fly.append(game[24])
            for tfix in fix_log:
                if game_data[2] == tfix[9]:
                    game_data[2] = tfix[0]
                elif game_data[4] == tfix[9]:
                    game_data[4] = tfix[0]
            database('CBB-Game-Database', game_data)
