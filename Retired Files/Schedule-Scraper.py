import bs4
import requests
import re
import csv
import os

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
fix_list = ['VI','CBB Reference','SBR 1','SBR 2','SBR 3','SBR 4','NC','Massey','Team Link','Ret Min','Schedule']
fix_log = database_reader('CBB-Team-Fix.csv', fix_list)

game_data = ['Date','Home','Away','Nutral Site']
database('CBB-Schedule-Database', game_data)
game_data = ['','','','','','']
tournament = ['Championship','Semifinals','Quarterfinals','Semifinal','Quarterfinal','Second Round','First Round','First Four','Sweet Sixteen','Elite Eight','Final Four','Game 1','Game 2','Game 3']
date = 0


for year in range(2010,2019):
    last_year = year + 1
    new_year = str(year) + str(last_year)[2:]
    for week in range(1,23):
        BS_link = 'http://mattsarzsports.com/Schedule/WeeklyText/basketball' + str(new_year) + '/' + str(week)
        sauce = requests.get(BS_link)
        soup = bs4.BeautifulSoup(sauce.text, 'html.parser')
        for player in soup.find_all('td',{"class":["tablecell gamecell", "tablecell timecell"]}):
            data = (player.text)
            if ' at ' in data or '(at ' in data or "vs" in data:
                if 'vs' in data and '(' not in data:
                    if 'vs.' in data:
                        data = data.split(' vs. ')
                    elif 'vs,' in data:
                        data = data.split(' vs, ')
                    elif 'vs' in data:
                        data = data.split(' vs ')
                    game_data[2] = data[0]
                    game_data[1] = data[1]
                    game_data[3] = 'Post Season'
                if '(' in data:
                    dtest = 0
                    if 'vs.' in data:
                        dtest = data.split(' vs. ')
                    elif 'vs,' in data:
                        dtest = data.split(' vs, ')
                    elif 'vs' in data:
                        dtest = data.split(' vs ')
                    if dtest == 0:
                        pass
                    elif len(dtest[1]) > 5:
                        data = dtest
                        data[1] = data[1].split('(')
                        game_data[2] = data[0][1:]
                        game_data[1] = data[1][0]
                        if 'at' in data[1][1]:
                            game_data[3] = data[1][1][:-2]
                if " at " in data:
                    data = data.split(" at ")
                    game_data[2] = data[0][1:]
                    game_data[1] = data[1][:-1]

                for tround in tournament:
                    if tround in game_data[2]:
                        tdata = game_data[2].split(tround)
                        if tdata[1].startswith(' #'):
                            game_data[2] = tdata[1][3:]
                        else:
                            game_data[2] = tdata[1]
                """
                if 'SIU Edwardsvilleat UT Martin' in data:
                    data = data.split("at ")
                    game_data[2] = data[0][1:]
                    game_data[1] = data[1][:-1]
                """
                game_data = [game_data[0].strip(),game_data[1].strip(),game_data[2].strip(),game_data[3].strip()]

                for tfix in fix_log:
                    if tfix[10] == game_data[1]:
                        game_data[1] = tfix[0]
                    elif tfix[10] == game_data[2]:
                        game_data[2] = tfix[0]
                        
            if 'PM' in data and ':' in data or 'AM' in data and ':' in data:
                data = data.split(" ")
                game_data[0] = data[0][1:].strip()
                if game_data[0] == '':
                    game_data[0] = date
                date = game_data[0]
                database('CBB-Schedule-Database', game_data)
                game_data = ['','','','','','']

