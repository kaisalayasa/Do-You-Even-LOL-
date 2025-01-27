import json
import random
with open("champions.json","r") as f:
    champ_data = json.load(f)
    
champ_list=[]
ability_list_choices=['Passive','Q','W','R','R']


def chose_random_ability():
    for key in champ_data:
        champ_list.append(key)
    random_champ= random.choice(champ_list)
    random_ability= random.choice(ability_list_choices)
    ability_name= champ_data[random_champ][random_ability]['name']
    ability_icon= champ_data[random_champ][random_ability]['icon']
    
    return(ability_name,ability_icon,random_ability,random_champ)
ability_name, ability_icon, random_ability, random_champ = chose_random_ability()


print(ability_name)
print(ability_icon)
print(random_ability)