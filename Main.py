# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:12:48 2020

@author: forestas yan
"""

#conda install -c conda-forge basemap-data-hires=1.0.8.dev0
#conda install -c conda-forge proj4


from TP2 import *
import time as time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mplsoccer.pitch import Pitch

a = time.time()

df_coaches = pd.read_json("coaches.json")

df_teams = pd.read_json("teams.json")

df_matches_en = pd.read_json("matches_England.json")

df_events_en = pd.read_json("events_England.json")





#This function will produce a diagramm with the proportion of retired/active coaches
types_coaches(df_coaches)

#This function will produce a diagramm with the proportion of Coaches per country
#The countries with only one coaches will be in the "Others" category
coaches_per_country(df_coaches)

#This function creates a map with a dot on every city in the dataset where there is a national team
map_teams(df_teams)

#This function creates a graph for the big 6 teams
#The amount of goals is on the y axis and the game week is on the y axis
curves_big6(df_teams, df_matches_en)

#This program shows a football field with a dot at every spot where a member of the selected team scores a goal
#This is an example for Liverpool
#This programm takes A LOT of time (4min) due to the sheer size of the data
goals_team_field("Liverpool", df_teams, df_events_en)

print(time.time()-a)

