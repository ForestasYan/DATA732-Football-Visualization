# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 22:10:24 2020

@author: forestas yan
"""


from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="forestasyan@gmail.com")

location = geolocator.geocode("Bogot\u00e1 D.C.")
print((location.latitude, location.longitude))