import csv
import os
from datetime import date, timedelta

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

#Headings
game_head = ['Date','Type','Home Team','Home Score','Away Team','Away Score','Venue',
             'H ADJ O','H ADJ D','H OFF PPP','H OFF EFG%','H OFF TO%','H OFF REB%','H OFF FTR','H DEF PPP','H DEF EFG%','H DEF TO%','H DEF REB%','H DEF FTR',
             'A ADJ O','A ADJ D','A OFF PPP','A OFF EFG%','A OFF TO%','A OFF REB%','A OFF FTR','A DEF PPP','A DEF EFG%','A DEF TO%','A DEF REB%','A DEF FTR',
             'Tempo','ID','Home Coach','Away Coach']

#Create lists of database
game_list = database_reader('CBB-Game-Database.csv', game_head)

fix_list = ['VI','CBB Reference','SBR 1','SBR 2','SBR 3','SBR 4','NC','Massey','Team Link','Ret Min','Schedule']
fix_log = database_reader('CBB-Team-Fix.csv', fix_list)


for game in game_list:
    Ohome4 = (float(game[10]) * .4) + (float(game[11]) * .25) + (float(game[12]) * .2) + (float(game[13]) * .15)
    Dhome4 = (float(game[15]) * .4) + (float(game[16]) * .25) + (float(game[17]) * .2) + (float(game[18]) * .15)
    print(game[4],(Ohome4-Dhome4))
    print(game[2],(Dhome4-Ohome4))
    












