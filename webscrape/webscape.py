from bs4 import BeautifulSoup
import requests
import json
import os

def append_to_json(data):
    # Initializes variables
    existing_data = []

    # Finds the absolute path for the JSON
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    project_directory = os.path.abspath(os.path.join(current_script_directory, '..', '..'))
    json_file_path = os.path.join(project_directory, 'botzilla/data/monsters.json')
    
    # Checks if json exists
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        print(f"Error loading existing data: {e}")

    # Stores json data
    existing_data.append(data)
    # print(existing_data)
    # Checks if report number is in JSON data and appends if not
    if data:
        with open(json_file_path, 'w', encoding='utf-8') as file:
            print(f"Appended data to report number: {data['Name']} to {json_file_path.split('/')[-1]}")
            json.dump(existing_data, file, indent=2)
    else:
        print("nothing to append")


def scrape_monster(link):
    monster = {}
    logs = {}

    response_monster = requests.get(link)
    soup = BeautifulSoup(response_monster.text, 'html.parser')

    title = soup.find('span', class_='mw-page-title-main')
    monster['Name'] = title.text
    table = soup.find_all('table', class_='infobox')
    for row in table:
        info = row.find_all('tr')
        for line in info:
            title = line.find('th')
            desc = line.find('td')
            try:
                monster[title.text] = desc.text
            except:
                logs = f'{title}/{desc}: no text found'
    append_to_json(monster)
    return monster

def scrape_links():
    base_url = 'https://kaijufanon.fandom.com'
    toho_url = f'{base_url}/wiki/List_of_Toho_Kaiju'
    monster_links = []
    monsters = {}

    # Parses county website
    response_main = requests.get(toho_url)
    soup = BeautifulSoup(response_main.text, 'html.parser')

    table = soup.find_all('td')
    for row in table:
        links = row.find_all('a', href=True)
        for link in links:
            if link['href'].startswith('/wiki/'):
                monster_links.append(base_url+link['href'])

    for link in monster_links:
        if link == 'https://kaijufanon.fandom.com/wiki/Toho':
            monster_links.remove(link)
        elif link == 'https://kaijufanon.fandom.com/wiki/Daiei':
            monster_links.remove(link)
        else:
            monsters = scrape_monster(link)

    return monsters



# Starts the webscraper
if __name__ == "__main__":
    try:
        scrape_links()
    except Exception as e:
        print(f"Error in main script: {e}")