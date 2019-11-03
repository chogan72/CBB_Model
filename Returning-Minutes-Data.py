import csv
import os

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

#Stores old directory and changes current
first_directory = os.getcwd()
change_directory('/Database/')

#Headings
player_head = ['Year','Team','% returning']
fix_head = ['VI','CBB Reference','SBR 1','SBR 2','SBR 3','SBR 4','NC','Massey','Team Link','Ret Min','Schedule']

#Create lists of database
player_list = database_reader('ret-mins.csv', player_head)
fix_log = database_reader('CBB-Team-Fix.csv', fix_head)

head = ['Year','Team','Ret Mins']
database('CBB-Ret-Mins-Database', head) 

for team in player_list:
    for tfix in fix_log:
        if team[1] == tfix[9]:
            team[1] = tfix[0]
            
    database('CBB-Ret-Mins-Database', team)

