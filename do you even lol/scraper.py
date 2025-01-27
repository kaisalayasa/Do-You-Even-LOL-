from bs4 import BeautifulSoup
import requests
import json

champions = []
full_champion = {}

base_url = 'https://www.leagueoflegends.com/en-us/champions/'

ability_keys = ["Passive", "Q", "W", "E", "R"]


response = requests.get(base_url).text
mainpage = BeautifulSoup(response, 'html.parser')

champions_table = mainpage.find_all('a', href=lambda href: href and '/en-us/champions/' in href)

for champ in champions_table:

    champ_name = champ.get("aria-label").lower().replace(" ", "").replace(".", "").replace("'", "")
    if "nunu & willump" in champ_name:

        champ_name = "nunu"
    champions.append(champ_name)

    champ_details_url = f"{base_url}{champ_name}/"

   
    try:
        detail_response = requests.get(champ_details_url, timeout=10)
        detail_response.raise_for_status()  
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch details for {champ_name}: {e}")
        continue 

    champ_details = BeautifulSoup(detail_response.text, "html.parser")
    champion_abilities = {}
    abilities = champ_details.find_all("div", class_="icon-tab-label")

    for index, ability in enumerate(abilities):
        if index >= len(ability_keys):
            break  

        key = ability_keys[index]

        ability_icon_info = champ_details.find("img", attrs={'data-testid': f'icon-tab-tab-{index}'})
        ability_icon = ability_icon_info.get('src') if ability_icon_info else "Icon Not Found"
        ability_name = ability.get_text(strip=True) if ability else "Ability Name Not Found"

        champion_abilities[key] = {
            "name": ability_name,
            "icon": ability_icon
        }
        
    final_name = champ.get("aria-label")  
    full_champion[final_name] = champion_abilities

    
    print(full_champion[final_name])
    print("_________")

   
   


with open('champions.json', 'w', encoding='utf-8') as f:
    json.dump(full_champion, f, ensure_ascii=False, indent=4)

print("All champion data has been written to 'champions.json'.")
