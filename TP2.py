# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 13:39:47 2020

@author: forestas yan
"""
import os
#on veux le fichier "epsg" dans l'emplacement ci-dessous
os.environ["PROJ_LIB"] = "C:\\Users\\fores\\Anaconda3\\Library\\share";
from mpl_toolkits.basemap import Basemap

from mplsoccer.pitch import Pitch
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="forestasyan@gmail.com")

def types_coaches(df):    
    number_coaches = df.shape[0]
    
    
    #On regarde le nombre de coachs dont l'Id de leur équipe est 0
    number_retired_coaches = df["currentTeamId"].value_counts()[0]
    
    types_coaches = ["retired", "active"]
    data_coaches = [number_retired_coaches, (number_coaches-number_retired_coaches)]
    
    plt.pie(data_coaches, labels=types_coaches, shadow=True, autopct='%1.1f%%')
    plt.axis('equal')
    plt.show()
    plt.clf()


def coaches_per_country(df):
    per_country = df["passportArea"].value_counts()
    
    label_countries_aux = []
    value_countries_aux = []
    for country, occurence in per_country.items():
        label_countries_aux.append(country["name"])
        value_countries_aux.append(occurence)
       
    #On enleve tous les pays qui n'apparaissent qu'une fois
    label_countries = []
    value_countries = []
    number_countries_once = 0
    
    for k in range(len(value_countries_aux)):
        if value_countries_aux[k] != 1:
            label_countries.append(label_countries_aux[k])
            value_countries.append(value_countries_aux[k])
        else:
            number_countries_once +=1
    label_countries.append("Others")
    value_countries.append(number_countries_once)
        
    plt.pie(value_countries, labels=label_countries, shadow=True)
    plt.axis('equal')
    plt.show()
    
    
def map_teams(df_teams):
    rows_to_remove = []
    original_length = df_teams.shape[0]
    for k in range(original_length):
        if df_teams.type[k] == "club":
            rows_to_remove.append(df_teams.index[k])
    
    df_teams_new = df_teams.drop(rows_to_remove) 
    
    remaining_indexes = [k for k in range(original_length)][len(rows_to_remove):]
    
    
    label_cities = []
    latitude_cities = []
    longitude_cities = []
    for index in remaining_indexes:
        name_city = df_teams_new.city[index]
        label_cities.append(name_city)
        
        #We use an API to find what the coordonates of the cities are
        #If the API can't find the city, it wont show it
        try:
            location = geolocator.geocode(name_city)
            latitude_cities.append(location.latitude)
            longitude_cities.append(location.longitude)
            
        except:
            print(name_city)
            
            
    # A basic map
    plt.figure(figsize=(12,6))
    m=Basemap(llcrnrlon=-160, llcrnrlat=-75,urcrnrlon=160,urcrnrlat=80)
    m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
    m.fillcontinents(color='grey', alpha=0.7, lake_color='grey')
    m.drawcoastlines(linewidth=0.2, color="white")
     
    # Add a marker per city of the data frame!
    m.plot(longitude_cities, latitude_cities, linestyle='none', marker="o", markersize=6, alpha=0.6, c="orange", markeredgecolor="black", markeredgewidth=1)
    plt.show()
    plt.clf()
    
    
    
def curves_big6(df_teams, df_matches_en):
        
    #We first get the team id of the 6 teams we are working with
    name_big6 = ["Liverpool", "Manchester City", "Manchester United", "Chelsea", "Arsenal", "Tottenham Hotspur"]
    dico_id_big6 = {"Liverpool": "", "Manchester City": "", "Manchester United": "", "Chelsea": "", "Arsenal": "", "Tottenham Hotspur": ""}
    
    
    for k in range(df_teams.shape[0]):
        if df_teams.name[k] in name_big6:
            dico_id_big6[df_teams.name[k]] = df_teams.wyId[k]
    
    nb_gameweek = len(df_matches_en["gameweek"].value_counts())
    
    dico_bi6_goals = {"Liverpool": [0 for k in range(nb_gameweek)], "Manchester City": [0 for k in range(nb_gameweek)], "Manchester United": [0 for k in range(nb_gameweek)], "Chelsea": [0 for k in range(nb_gameweek)], "Arsenal": [0 for k in range(nb_gameweek)], "Tottenham Hotspur": [0 for k in range(nb_gameweek)]}
    
    
    for k in range(df_matches_en.shape[0]):
        for key in dico_id_big6:
            try:
                dico_bi6_goals[key][df_matches_en.gameweek[k]-1] = df_matches_en.teamsData[k][str(dico_id_big6[key])]["score"]    
            except:
                pass
            
    
    list_week = [(k+1) for k in range(nb_gameweek)]
    
    plt.figure(figsize=(12,6))
    for key in dico_id_big6:
        plt.plot(list_week, dico_bi6_goals[key], label=key)
    plt.legend()
    plt.show()
    
    
    
    
def goals_team_field(team, df_teams, df_events_en):
    for k in range(df_teams.shape[0]):
        if df_teams.name[k] == team:
            Id_team = df_teams.wyId[k]
            break
    
    rows_to_remove = []
    original_length = df_events_en.shape[0]
    for k in range(original_length):
        if df_events_en.teamId[k] != Id_team:
            rows_to_remove.append(df_events_en.index[k])
        elif (df_events_en.subEventName[k] != "Goal kick"):
            rows_to_remove.append(df_events_en.index[k])
        
    df_events_en_new = df_events_en.drop(rows_to_remove) 
        
    remaining_indexes = [k for k in range(original_length)]
    for nb in rows_to_remove:
        remaining_indexes.remove(nb)
    
    x = []
    y = []
    
    for k in range(df_events_en_new.shape[0]):
        position = df_events_en_new.positions[remaining_indexes[k]][1]
        x.append(position["x"])
        y.append(position["y"])
    
    plt.style.use('ggplot')
    pitch = Pitch(pitch_color='grass', line_color='white', stripe=True)
    fig, ax = pitch.draw()
    sc = pitch.scatter(y, x,  s=50, ax=ax)
