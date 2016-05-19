# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 08:48:26 2016

@author: skrzym
"""

import pandas as pd
import numpy as np
from pprint import pprint
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Function built to 'apply' to all date rows in the 'Start' and 'Finish' columns
def str2dt(string):
    return datetime.strptime(string,'%d-%b-%Y %H:%M')

def int2dow(integer):
    dow_dictionary = {
    0:'Mon',
    1:'Tue',
    2:'Wed',
    3:'Thu',
    4:'Fri',
    5:'Sat',
    6:'Sun'
    }
    return dow_dictionary[integer]

#Read the data into a pandas data frame
hd = pd.read_csv('HealthData.csv')

#Rename the columns to simpler names for ... simplicity
columns = ['Start', 'Finish', 'Active_Kcal', 'Distance', 'Heart_Rate', 'Steps']
hd.columns = columns

#Convert the 'Start' and 'Finish' columns to datetime types for easy analysis
for index in ['Start', 'Finish']:
    hd[index] = hd[index].apply(str2dt)

#Create 3 new columns for the 'year', 'month' and 'hour' values of a data point
hd['year'] = hd['Start'].apply(lambda x: x.year)
hd['month'] = hd['Start'].apply(lambda x: x.month)
hd['hour'] = hd['Start'].apply(lambda x: x.hour)

#Create a new column for the 'day of the week' or 'dow'
#Use helper function to convert integer values to real word values for 'dow'
hd['dow'] = hd['Start'].apply(lambda x: x.weekday())
#hd['dow'] = hd['dow'].apply(int2dow)

#For a given year, build a set of data for each month's steps-by-hour averages
def get_monthly_steps_per_hour(df, year=2015):
    for month in range(1,13):
        query = df.query('year=='+str(year))
        pivot = pd.pivot_table(query, index=['month','hour'], values=['Steps'], aggfunc=np.mean)
        pivot = pivot.reset_index()
    return pivot
    
    
def get_monthly_steps_per_dow(df, year=2015):
    for month in range(1,13):
        query = df.query('year=='+str(year))
        pivot = pd.pivot_table(query, index=['month','dow'], values=['Steps'], aggfunc=np.mean)
        pivot = pivot.reset_index()
        pivot['dow'] = pivot['dow'].apply(int2dow)
    return pivot

mdata = get_monthly_steps_per_hour(hd, 2015)
#plt.figure(figsize=(200,100))
sns.set(font_scale=2)
fg = sns.FacetGrid(mdata, col='month', col_wrap=4, size=6, aspect=1.5)
fg.map(sns.barplot,'hour','Steps')
plt.show()

mdata = get_monthly_steps_per_dow(hd, 2015)
#plt.figure(figsize=(200,100))
sns.set(font_scale=2)
fg = sns.FacetGrid(mdata, col='month', col_wrap=4, size=6, aspect=1)
fg.map(sns.barplot,'dow','Steps')

plt.show()













