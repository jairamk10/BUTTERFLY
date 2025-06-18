#!/usr/bin/env python
# coding: utf-8

# In[12]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from astropy.coordinates import SkyCoord
from sunpy.coordinates import frames
import sunpy.coordinates
import astropy.units as u
import math


# In[13]:


data_strong = pd.read_csv('strong (Copy).csv')

ds = data_strong.dropna(subset=['  X (")','  Y (")', 'Date       Peak           (UT)', 'Brightness(K)', 'Position'])
X_strong = ds['  X (")'] #arcsec
Y_strong = ds['  Y (")'] #arcsec
BS =ds['Brightness(K)']
DATE_strong = ds['Date       Peak           (UT)'] #DATE-TIME


# In[14]:


data_weak = pd.read_csv('weak.csv')

dw = data_weak.dropna(subset=['  X (")','  Y (")', 'Date       Peak           (UT)', 'Brightness(K)', 'Position'])
X_weak = dw['  X (")'] #arcsec
Y_weak = dw['  Y (")'] #arcsec
BW =dw['Brightness(K)']
DATE_weak = dw['Date       Peak           (UT)'] #DATE-TIME


# In[15]:


832 +1790


# In[16]:


fig, ax = plt.subplots()

ax2 =ax.twinx()
ax.scatter(DATE_strong, X_strong, c='blue', marker='.')
ax2.scatter(DATE_strong, Y_strong,c='orange', marker='.')

specific_ticks = DATE_strong[::100]

for axis in ax, ax2:
    axis.set_xticks(specific_ticks)
    axis.xaxis.set_minor_locator(AutoMinorLocator())
    axis.yaxis.set_minor_locator(AutoMinorLocator())
    axis.tick_params(direction='in', length = 12, which ='major', top=True, right=True)
    axis.tick_params(direction='in', length = 5, which ='minor', top=True, right=True)
    axis.tick_params(axis='y')
    axis.tick_params(axis='x', rotation=20)
    axis.set_ylabel("(x,y) in arcseconds", fontsize = 14)
    axis.set_title("Strong Correlation", fontsize = 14)
    axis.legend(loc = 'best')
    axis.grid(True)


# In[17]:


fig, ax = plt.subplots()

ax2 =ax.twinx()
ax.scatter(DATE_weak, X_weak, color = 'blue', label='x')
ax2.scatter(DATE_weak, Y_weak, color = 'orange', label='y')

specific_ticks = DATE_weak[::100]

for axis in ax, ax2:
    axis.set_xticks(specific_ticks)
    axis.xaxis.set_minor_locator(AutoMinorLocator())
    axis.yaxis.set_minor_locator(AutoMinorLocator())
    axis.tick_params(direction='in', length = 12, which ='major', top=True, right=True)
    axis.tick_params(direction='in', length = 5, which ='minor', top=True, right=True)
    axis.tick_params(axis='y')
    axis.tick_params(axis='x', rotation=20)
    axis.set_ylabel("(x,y) in arcseconds", fontsize = 14)
    axis.set_title("Weak Correlation", fontsize = 14)
    axis.legend(loc = 'best')
    axis.grid(True)


# In[18]:


DATE_strong = pd.to_datetime(DATE_strong)# Convert DATE_strong to a datetime series
datas = pd.DataFrame({'Date': DATE_strong})# Create a DataFrame
datas['Year'] = datas['Date'].dt.year# Extract the year from the date

DATE_weak = pd.to_datetime(DATE_weak)# Convert DATE_weak to a datetime series
dataw = pd.DataFrame({'Date': DATE_weak})# Create a DataFrame
dataw['Year'] = dataw['Date'].dt.year# Extract the year from the date


# In[19]:


fig, ax =plt.subplots()
#ax2 = ax.twinx()
ax.scatter(dataw['Year'], Y_weak, marker='.', label = 'Y(weak corr)')
ax.scatter(datas['Year'], Y_strong, marker='.', label = 'Y(strong corr)')
#ax.scatter(dataw['Year'], X_weak, marker='.', label = 'X(weak corr)', alpha =0.1)
#ax.scatter(datas['Year'], X_strong, marker='.', label = 'X(strong corr)', alpha =0.1)

ax.set_ylabel('(X,Y) arcseconds')

ax.axhline(0, c='black')
ax.legend()


# In[20]:


plt.figure()
plt.hist(datas['Year'])
plt.title('Histogram of events (yearwise)')


# In[21]:


dfs = pd.DataFrame(ds['Position'])
dfw = pd.DataFrame(dw['Position'])

def convert_coordinates(coord):
    lat = int(coord[1:3]) * (-1 if coord[0] == 'S' else 1) 
    '''coord[1:3] extracts the degree part of the latitude. The latitude is multiplied by -1 
    if the first character is 'S' (indicating South), making it negative. If it's 'N' (North), it remains positive.'''
    lon = int(coord[4:6]) * (-1 if coord[3] == 'W' else 1)  
    '''coord[4:6] extracts the degree part of the longitude. 
    Similar logic is applied for longitude, making it negative if the fourth character is 'W' (West) and positive if it's 'E' (East).'''
    return lat, lon

dfs[['Latitude', 'Longitude']] = dfs['Position'].apply(convert_coordinates).apply(pd.Series)
dfw[['Latitude', 'Longitude']] = dfw['Position'].apply(convert_coordinates).apply(pd.Series)

plt.figure(figsize=(10, 6))
plt.scatter(datas['Year'], dfs['Latitude'], c='Orange', marker='o')
plt.scatter(dataw['Year'], dfw['Latitude'], c='blue', marker='o', alpha = 0.2)
plt.xlabel('Year')
plt.ylabel('Latitude (degrees)')
plt.axhline(0, color='black', linestyle='--')
plt.grid()
plt.legend()
plt.show()


# In[ ]:




