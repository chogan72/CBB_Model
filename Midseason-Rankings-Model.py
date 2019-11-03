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


#Stores old directory and changes current
first_directory = os.getcwd()
change_directory('/Database/')

#Headings
game_head = ['Date','Type','Home Team','Home Score','Away Team','Away Score','Venue',
             'H ADJ O','H ADJ D','H OFF PPP','H OFF EFG%','H OFF TO%','H OFF REB%','H OFF FTR','H DEF PPP','H DEF EFG%','H DEF TO%','H DEF REB%','H DEF FTR',
             'A ADJ O','A ADJ D','A OFF PPP','A OFF EFG%','A OFF TO%','A OFF REB%','A OFF FTR','A DEF PPP','A DEF EFG%','A DEF TO%','A DEF REB%','A DEF FTR',
             'Tempo','ID','Home Coach','Away Coach']
spread_head = ['Date','Home','Away','Spread','Total']
week_head = ['Year','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']

#Create lists of database
game_list = database_reader('CBB-Game-Database.csv', game_head)
spread_list = database_reader('CBB-spread-Database.csv', spread_head)
week_list = database_reader('Week-Dates.csv', week_head)

head = ['Date','Team','Ranking']

os.chdir(first_directory)
change_directory('/Rankings/')

for week in week_list:
    if int(week[0]) >= 2012:
        week_num = 1
        for day in week:
            if day != week[-1]:
                pre_list = database_reader('CBB-' + str(week[0]) + '-Rankings.csv', head)
                if day == pre_list[-1][0]:
                    avg = 0
                    count = 0
                    for row in pre_list:
                        if row[0] == week[week_num - 1]:
                            avg += float(row[2])
                            count += 1
                    avg = avg/count
                    for row in pre_list:
                        start_date = week[week_num - 1].split('/')
                        start_date = date(int(start_date[2]), int(start_date[0]), int(start_date[1]))
                        end_date = week[week_num].split('/')
                        end_date = date(int(end_date[2]), int(end_date[0]), int(end_date[1]))
                        if row[0] == week[week_num - 1]:
                            dif = 0
                            for game in game_list:
                                if game[6] == 'N':
                                    home_court = 0
                                else:
                                    home_court = 4
                                game_date = game[0].split('/')
                                game_date = date(int(game_date[2]), int(game_date[0]), int(game_date[1]))
                                if start_date <= game_date < end_date:
                                    if game[2] == row[1]:
                                        for row2 in pre_list:
                                            if row2[0] == row[0] and row2[1] == game[4]:
                                                home = (float(row[2])-float(avg))*45
                                                away = (float(row2[2])-float(avg))*45
                                                spread = float(away) - float(home) - home_court
                                                dif += ((float(game[3])-float(game[5])) + spread)
                                    if game[4] == row[1]:
                                        for row2 in pre_list:
                                            if row2[0] == row[0] and row2[1] == game[2]:
                                                home = (float(row[2])-float(avg))*45
                                                away = (float(row2[2])-float(avg))*45
                                                spread = float(away) - float(home) - home_court
                                                dif += ((float(game[5])-float(game[3])) - spread)
                            dif = (float(dif)*.0005) + float(row[2])
                            row = [week[week_num],row[1],dif]
                            database('CBB-' + str(week[0]) + '-Rankings', row) 
            week_num += 1

