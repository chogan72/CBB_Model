import bs4
import requests
import re
import csv
import os
from datetime import date, timedelta

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

game_data = ['Year','Team', 'Odds']

vi_list = []
database('CBB-NC-Database', game_data)

fix_list = ['VI','CBB Reference','SBR 1','SBR 2','SBR 3','SBR 4','NC','Massey','Team Link','Ret Min']
fix_log = database_reader('CBB-Team-Fix.csv', fix_list)

head_list = ['Date','Rot','VH','Team','1st','2nd','Final','Open','Close','ML','2H']
for year in range(2011,2020):
    game_data[0] = year
    BS_link = 'https://www.sports-reference.com/cbb/seasons/' + str(year) + '-preseason_odds.html'
    sauce = requests.get(BS_link)
    soup = bs4.BeautifulSoup(sauce.text, 'html.parser')
    for player in soup.find_all(['th','td']):
        data = (player.text)
        if data != 'School' or data != 'Odds':
            if '+' in data:
                game_data[2] = data
                database('CBB-NC-Database', game_data)
            else:
                game_data[1] = data
                for tfix in fix_log:
                    if game_data[1] == tfix[6]:
                        game_data[1] = tfix[0]
