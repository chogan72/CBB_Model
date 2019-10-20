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
boxscore_head = ['Date','Home','Away','H Score','A Score','ID']
nf_head = ['VI','CBB Reference','SBR 1','SBR 2','SBR 3','SBR 4','NC','Massey','Team Link']

#Create lists of database
boxscore_list = database_reader('CBB-Boxscore-Database.csv', boxscore_head)
nf_list = database_reader('CBB-Team-Fix.csv', nf_head)

head = ['Year','Team','Real Win Total', 'Real Loss Total', 'Pythag']
database('CBB-Pythag-Database', head) 

for year in range(2011,2020):
    year_fix = year - 1
    for team in nf_list:
        team_list = [year,team[0],0,0,0]
        fp = 0
        ap = 0
        for score in boxscore_list:
            month = score[0][:2]
            if month.endswith('/'):
                month = month[:1]
            new_year = score[0][-4:]
            if int(month) >= 11 and int(new_year) == year_fix or int(month) <= 4 and int(new_year) == year:
                if team[0] == score[1]:
                    if int(score[3]) > int(score[4]):
                        team_list[2] += 1
                    else:
                        team_list[3] += 1
                    fp += float(score[3])
                    ap += float(score[4])
                elif team[0] == score[2]:
                    if int(score[3]) < int(score[4]):
                        team_list[2] += 1
                    else:
                        team_list[3] += 1
                    fp += float(score[4])
                    ap += float(score[3])

        #Pythagorean Expectation Formula
        if fp != 0 or ap != 0:
            pyth = (fp**10.25/(fp**10.25+ap**10.25))
            team_list[4] = pyth
        database('CBB-Pythag-Database', team_list)

