from sportsreference.ncaab.roster import Roster, Player
import os
import csv
import requests


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

fix_list = ['VI','CBB Reference','SBR 1','SBR 2','SBR 3','SBR 4','NC','Massey','Team Link','Ret Min']
fix_log = database_reader('CBB-Team-Fix.csv', fix_list)

game_list = ['Year','Team','Player','Stats','Played','ID']
#database('CBB-Player-Database', game_list)

for year in range(2019,2020):
    last_year = year -1
    new_year = str(last_year) + '-' + str(year)[2:]
    for team in fix_log:
        test_link = 'https://www.sports-reference.com/cbb/schools/' + team[8] + '/' + str(year) + '.html'
        request = requests.get(test_link)
        if request.status_code == 200:
            team_player = 0
            roster_plays = Roster(team[8],str(year))
            for player in roster_plays.players:
                if team_player < 15:
                    try:
                        game_list = [year,team[0],player.name, player(new_year).games_started, player(new_year).games_played, player.player_id]
                        database('CBB-Player-Database', game_list)
                        team_player += 1
                    except TypeError:
                        pass

