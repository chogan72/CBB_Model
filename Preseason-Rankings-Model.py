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
nc_head = ['Year','Team','Odds']
pythag_head = ['Year','Team','Real Win Total', 'Real Loss Total', 'Pythag']
mass_head = ['Year','Ranking','Team']
rm_head = ['Year','Team','Ret Mins']

#Create lists of database
nc_list = database_reader('CBB-NC-Database.csv', nc_head)
pythag_list = database_reader('CBB-Pythag-Database.csv', pythag_head)
mass_list = database_reader('CBB-Massey-Ratings-Database.csv', mass_head)
rm_list = database_reader('CBB-Ret-Mins-Database.csv', rm_head)

os.chdir(first_directory)
change_directory('/Rankings/')

head = ['Year','Team','Ranking']
database('CBB-Preseason-Rankings', head) 

for year in range(2012,2020):
    for mass in mass_list:
        if mass[0] == str(year):
            mass_rank = (355 - int(mass[1])) * .003
            for team in pythag_list:
                py_year = year - 1
                if team[0] == str(py_year) and team[1] == mass[2] and team[2] != 0 and team[3] != 0:
                    team_check = 0
                    for champ in nc_list:
                        if champ[0] == str(year) and champ[1] == team[1]:
                            if int(champ[2]) > 100000:
                                champ[2] = 100000
                            odds = 1/(((int(champ[2])/100)+1)+1)
                            team_check = 1
                    if team_check == 0:
                        odds = 1/(((100000/100)+1)+1)
                    first_year = 0
                    for rm in rm_list:
                        if rm[0] == str(year) and rm[1] == mass[2]:
                            current_rm = rm
                            first_year = 1
                    if (int(team[2]) + int(team[3])) > 15 and first_year  == 1:
                        rank = (float(team[4]) + (float(odds)*10) + float(mass_rank) + (float(current_rm[2])/100)) / 4
                    elif first_year  == 0:
                        rank = ((float(odds)*10) + float(mass_rank)) / 2
                    head = [year,team[1],rank]
                    database('CBB-Preseason-Rankings', head) 
            
            
