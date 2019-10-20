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
fix_list = ['VI','CBB Reference','SBR 1','SBR 2','SBR 3','SBR 4','NC','Massey','Team Link']
fix_log = database_reader('CBB-Team-Fix.csv', fix_list)

game_data = ['Year','Ranking','Team']
database('CBB-Massey-Ratings-Database', game_data)

for year in range(2011,2020):
    BS_link = 'https://www.masseyratings.com/cb/arch/compare' + str(year) + '-0.htm'
    sauce = requests.get(BS_link)
    soup = bs4.BeautifulSoup(sauce.text, 'html.parser')
    start = 0
    rank = 1
    for player in soup.find_all('a'):
        data = (player.text)
        if data == 'Correlation to Consensus':
            start = 0

        if data == '   Mean Median St.Dev':
            if start == 0:
                start = 1
    
        elif start == 1:
            game_data = [year,rank,data]
            for tfix in fix_log:
                if game_data[2] == tfix[7]:
                    game_data[2] = tfix[0]
            database('CBB-Massey-Ratings-Database', game_data)
            rank += 1
