import bs4
import requests
import re
import csv
import os

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

change_directory('\\Database\\')
BS_link = 'https://www.sports-reference.com/cbb/schools/'
sauce = requests.get(BS_link)
soup = bs4.BeautifulSoup(sauce.text, 'html.parser')
for player in soup.find_all('a'):
    link = player.get('href')
    if 'schools' in link:
        database('CBB-SR-Link-Database', [link[13:-1]])
