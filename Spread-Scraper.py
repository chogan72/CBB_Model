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

game_data = ['Date', 'Home', 'Away', 'Spread', 'Total']

vi_list = []
database('CBB-Spread-Database', game_data)

fix_list = ['VI','CBB Reference','SBR 1','SBR 2','SBR 3','SBR 4','NC','Massey','Team Link']
fix_log = database_reader('CBB-Team-Fix.csv', fix_list)

head_list = ['Date','Rot','VH','Team','1st','2nd','Final','Open','Close','ML','2H']
for year in range(2011,2020):
    change_directory('\\SBR\\')
    game_log = database_reader('ncaa basketball ' + str(year) + '.csv', head_list)
    year -= 1
    os.chdir(first_dir)
    change_directory('\\Database\\')
    index = 0
    new_year = 0
    for game in game_log:
        if len(game[0]) > 3:
            date = str(game[0])[:2] + '-' + str(game[0])[2:]  + '-' + str(year)
        else:
            if new_year == 0:
                year += 1
                new_year = 1
            date = str(game[0])[:1] + '-' + str(game[0])[1:]  + '-' + str(year)
        game_data[0] = date
        if index == 1:
            game_data[1] = game[3]
            if game_data[4] == 'NL' and game[8] == 'NL' or game_data[3] == 'NL' and game[8] == 'NL':
                game_data[3] = ''
                game_data[4] = ''

            else:
                if game_data[3] == 'NL' and game[8] != 'NL':
                    game_data[3] = game[8]
                    game_data[4] = ''
                elif game_data[3] != 'NL' and game[8] == 'NL':
                    game[8] = game_data[3]
                    game_data[4] = ''
                    
                if game_data[3] == 'pk':
                    game_data[3] = 0
                if game[8] == 'pk':
                    game[8] = 0
                    
                if '-' in str(game_data[3]):
                    split = re.split('-', str(game_data[3]))
                    game_data[3] = split[0]
                if '-' in str(game[10]):
                    split = re.split('-', str(game[8]))
                    game[8] = split[0]
                    
                if float(game_data[3]) < float(game[8]):
                    game_data[4] = game[8]
                elif float(game_data[3]) > float(game[8]):
                    game_data[4] =  game_data[3]
                    game_data[3] = '-' + str(game[8])

                for tfix in fix_log:
                    if game_data[1] == tfix[2] or game_data[1] == tfix[3] or game_data[1] == tfix[4] or game_data[1] == tfix[5]:
                        game_data[1] = tfix[0]
                    elif game_data[2] == tfix[2] or game_data[2] == tfix[3] or game_data[2] == tfix[4] or game_data[2] == tfix[5]:
                        game_data[2] = tfix[0]
            
            index = 0
            database('CBB-Spread-Database', game_data)
            game_data = ['', '', '', '', '']
                    
        elif index == 0:
            game_data[2] = game[3]
            game_data[3] = game[8]
            index = 1
            

#beautifulsoup4 link
os.chdir(first_dir)
change_directory('\\Database\\')
start_date = date(2019, 11, 1)
end_date = date(2020, 4, 30)
delta = timedelta(days=1)
while start_date <= end_date:
    date = (start_date.strftime("%Y-%m-%d"))
    year = date[2:4]
    month = date[5:7]
    day = date[8:10]
    start_date += delta
    date = (start_date.strftime("%m-%d-%Y"))
    BS_link = 'http://www.vegasinsider.com/college-basketball/matchups/matchups.cfm/date/' + str(month) + '-' + str(day) + '-' + str(year)
    sauce = requests.get(BS_link)
    soup = bs4.BeautifulSoup(sauce.text, 'html.parser')
    for player in soup.find_all('td', {"class":["viCellBg2 cellBorderL1 cellTextNorm padCenter", "viHeaderNorm"]}):

        #Splits needed information
        gdata = (player.text)
        gdata = re.split('>|<', gdata)
        gdata = gdata[0].strip()

        #Checks For Home and Away Teams
        if len(gdata) > 5:
            gdata = re.split(' @ ', gdata)
            game_data[1] = gdata[1]
            game_data[2] = gdata[0]
            vi_list = []
            index = 0
            max_len = 14

        #Adds stats to temp list
        else:
            vi_list.append(gdata)
            index += 1

        #Writes Spread and Total to Game list
        if len(vi_list) == max_len:
            if '-' in vi_list[1]:
                game_data[3] = vi_list[1][1:]
            elif vi_list[1] == 'PK':
                game_data[3] = '0'
            elif '-' not in gdata:
                game_data[4] = vi_list[1]

            if '-' in vi_list[9]:
                game_data[3] = vi_list[9]
            elif vi_list[6] == 'PK':
                game_data[3] = '0'
            elif '-' not in gdata:
                game_data[4] = vi_list[9]

            #Write Year and Week
            game_data[0] = date

            #Writes list to CSV file
            database('CBB-Spread-Database', game_data)
            game_data = ['','','','','']

