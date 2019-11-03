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
rank_head = ['Date','Team','Ranking']

#Create lists of database
game_list = database_reader('CBB-Game-Database.csv', game_head)
spread_list = database_reader('CBB-Spread-Database.csv', spread_head)
week_list = database_reader('Week-Dates.csv', week_head)

os.chdir(first_directory)
change_directory('/Prediction/')
    
head = ['Date','Home','Spread','Home Rank','Away','Away Rank','ADV','ADV Team','ADV Bet']
database('CBB-Prediction', head)

for year in range(2012,2020):
    os.chdir(first_directory)
    change_directory('/Rankings/')
    rank_list = database_reader('CBB-' + str(year) + '-Rankings.csv', rank_head)
    os.chdir(first_directory)
    change_directory('/Prediction/' + str(year) + '/')
    yesterday = ('10/31/1999')
    for spread in spread_list:
        game_date = spread[0].split('/')
        game_year = game_date[2]
        game_month = game_date[0]
        game_date = date(int(game_date[2]), int(game_date[0]), int(game_date[1]))
        if str(game_month) == '11' or str(game_month) == '12':
            game_year = int(game_year) + 1
        if str(game_year) == str(year): 
            if spread[0] != yesterday:
                database('CBB-' + str(spread[0].replace('/','-')) + '-Prediction', head)
            yesterday = spread[0]
            for week in week_list:
                week_num = 1
                for day in week:
                    if week_num != 1 and week_num != 25:
                        start_date = week[week_num - 1].split('/')
                        start_date = date(int(start_date[2]), int(start_date[0]), int(start_date[1]))
                        end_date = week[week_num].split('/')
                        end_date = date(int(end_date[2]), int(end_date[0]), int(end_date[1]))
                        if start_date <= game_date < end_date:
                            avg = 0
                            count = 0
                            for row in rank_list:
                                if row[0] == week[week_num - 1]:
                                    avg += float(row[2])
                                    count += 1
                            if count != 0:
                                avg = avg/count
                                for rank in rank_list:
                                    if rank[0] == day:
                                        if spread[1] == rank[1]:
                                            home_rank = rank
                                        elif spread[2] == rank[1]:
                                            away_rank = rank
                                home_court = 4
                                if year < 2020:
                                    for game in game_list:
                                        if game[0] == spread[0] and game[2] == spread[1] and game[4] == spread[2]:
                                            if game[6] == 'N':
                                                home_court = 0
                                            else:
                                                home_court = 4
                                home = (float(home_rank[2])-float(avg))*45
                                away = (float(away_rank[2])-float(avg))*45
                                my_spread = float(away) - float(home) - home_court
                                if spread[3] != '':
                                    advantage = float(spread[3]) - my_spread
                                else:
                                    advantage = 0
                                prediction = []
                                prediction = [spread[0],spread[1],spread[3],home,spread[2],away,advantage,'-','-']
                                if advantage < 0:
                                    prediction[7] = spread[2]
                                elif advantage > 0:
                                    prediction[7] = spread[1]
                                if advantage >= 10 or advantage <= -10:
                                    prediction[8] = 1
                                database('CBB-' + str(spread[0].replace('/','-')) + '-Prediction', prediction)
                                os.chdir(first_directory)
                                change_directory('/Prediction/')
                                database('CBB-Prediction', prediction)
                                os.chdir(first_directory)
                                change_directory('/Prediction/' + str(year) + '/')
                    week_num += 1
