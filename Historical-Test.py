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
prediction_head = ['Date','Home','Spread','Home Rank','Away','Away Rank','ADV','ADV Team','ADV Bet']

#Create lists of database
game_list = database_reader('CBB-Game-Database.csv', game_head)
os.chdir(first_directory)
change_directory('/Prediction/')
prediction_list = database_reader('CBB-Prediction.csv', prediction_head)

os.chdir(first_directory)
change_directory('/Historical-Test/')
head = ['Date','Home','Spread','H Score','Away','A Score','ADV','ADV Team','Score']


for mult in range(9,21):
    w = 0
    l = 0
    p = 0
    database(str(mult) + 'ADV-Test',head)
    for spread in prediction_list:
        if float(spread[6]) > float(mult) or float(spread[6]) < -float(mult):
            for game in game_list:
                if game[0] == spread[0] and game[2] == spread[1] and game[4] == spread[4]:
                    if spread[7] == spread[1]:
                        score = float(game[3]) - float(game[5]) + float(spread[2])
                    elif spread[7] == spread[4]:
                        score = float(game[5]) - float(game[3]) - float(spread[2])
                    game_data = [spread[0],spread[1],spread[2],game[3],spread[4],game[5],spread[6],spread[7],score]
                    database(str(mult) + 'ADV-Test',game_data)
                    if score > 0:
                        w += 1
                    elif score < 0:
                        l += 1
                    elif score == 0:
                        p += 1
    print(mult,w,'-',l,'-',p)
        
