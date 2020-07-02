# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 21:41:37 2020

@author: srujan
"""

import pandas as pd
import matplotlib.pyplot as plot
import matplotlib.pyplot as plt


#import pandas as pd
import numpy as np
import os
import seaborn as sns


os.chdir("C:/Users/sruja/Desktop/Courses/AIT 580/Final Project")
mydata= pd.read_csv('Drug-related-deaths2.csv')
mydata.columns
#First 5 rows of data
mydata.head()
mydata.shape
mydata.columns


# To see how many count of non-null values for each column
mydata.info()

# Count of NA values per each row.
mydata.isna().sum()

#Removing records where Age, Sex, Race are Null or NA

mydata.dropna(subset=['Date', 'Age','Sex','Race'], inplace=True)
#mydata=mydata.dropna(subset=['Date', 'Age','Sex','Race'], thresh=1)


# Exploratory Analysis

plt.figure(figsize=(16,6))
fig = sns.countplot(x='Age', data=mydata)
plt.xticks(rotation = 45, horizontalalignment = 'right')
plt.title('Count of deaths by Age ')
plt.show()

mydata['Sex'].describe()
mydata['Sex'].value_counts()
mydata['Sex'].value_counts().plot(kind='bar')
plt.title('Count of deaths by Sex ')
plt.xlabel('Sex')
plt.ylabel('Count')


mydata['Race'].value_counts()
mydata['Race'].value_counts().plot(kind='bar')
plt.title('Count of deaths by Race ')
plt.xlabel('Race')
plt.ylabel('Count')



mydata['DeathCounty'].value_counts()
mydata['DeathCounty'].value_counts().plot(kind='bar')
plt.title('Count of deaths for each DeathCounty ')
plt.xlabel('County')
plt.ylabel('Count')

mydata['Location'].value_counts()
mydata['Location'].value_counts().plot(kind='bar')
plt.title('Count of deaths in each Location ')
plt.xlabel('Location')
plt.ylabel('Count')


#########################################################################




#Cleaning date column, creating new column  for year, month, day_of_week


Date_df = pd.to_datetime(mydata['Date'])
mydata.insert(loc=2, column='new_date', value=Date_df)
# Creating new column for Year by extracting Year from old Date column
mydata.insert(loc=3,column='Year',value=mydata['new_date'].dt.year)
#Creating Month Column and adding it our data frame mydata
mydata.insert(loc=4,column='Month',value=mydata['new_date'].dt.month)
# month Dictionary 
month_dict={1:'January',2:'Febuary',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'}
#replacing the numerical month with words from above dictionary using apply function
mydata['Month'] = mydata['Month'].apply(lambda x: month_dict[x])
#Creating column for day of week 
mydata.insert(loc=5,column='day_of_week',value=mydata['new_date'].dt.dayofweek)
days_dict = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thurday',4:'Friday',5:'Saturday',6:'Sunday'}
mydata['day_of_week'] = mydata['day_of_week'].apply(lambda x: days_dict[x])

mydata.iloc[:,[2,3,4,5]].head()


mydata.columns

#mydata['drugs_used'] = mydata.loc[:, 'Heroin':'AnyOpioid'].apply(lambda value: ', '.join(value[value.notnull()]), axis = 1)


## Creating column for count of drugs used 
#mydata['count_of_drugs']= mydata.drugs_used.str.split(',').apply(lambda x: len(x))

#Convert drug associated death from Y to Drug name in upper case
def Drugname(value, column):
    if(value == 'Y'):
        return str(column).upper()
    else:
        return value

for column in mydata.loc[:, 'Heroin':'AnyOpioid']:
    if(column != 'Other'):
        mydata[column] = mydata[column].map(lambda value: Drugname(value, column))

# The below code gives us the number of deaths associated by each drug
        
Drugs_used=pd.DataFrame()
Drugs_used['Drug_name']=0
Drugs_used['count']=0

for column in mydata.loc[:, 'Heroin':'AnyOpioid']:
        Drugs_used=Drugs_used.append({'Drug_name':column,'count':mydata[column].value_counts()[0]},ignore_index=True)


# plot for number of deaths associated by each drug   
Drugs_used.sort_values('count',ascending=False).plot(kind='bar',x='Drug_name',figsize=(7,5))
plt.ylabel('Count')
plt.title('Count of deaths by each drug')

# Adding to new column to track deaths associated with combination of one or more drugs used
 
mydata['multiple_drugs_used'] = mydata.loc[:, 'Heroin':'AnyOpioid'].apply(lambda value: ', '.join(value[value.notnull()]), axis = 1)


multiple_drugs_count=mydata['multiple_drugs_used'].value_counts()
multiple_drugs_count.loc[mydata['multiple_drugs_used'].value_counts()>100]



multiple_drugs_count.loc[mydata['multiple_drugs_used'].value_counts()>100].plot(kind='bar',figsize=(7,5))
plt.ylabel('Count')
plt.title('Deaths due to overdose of combination of drug(Deaths>100)')



mydata['drugs_count'] = mydata['multiple_drugs_used'].apply(lambda drugs: len(drugs.split(', ')))


# The below plot shows us the number of accidental deaths caused by drugs by Year 

mydata.groupby('Year')['multiple_drugs_used'].count().plot(kind='bar',figsize=(7,5))
plt.ylabel('Count')
plt.title('Number of Deaths per year')


# number of deaths per each month
mydata.groupby('Month')['multiple_drugs_used'].count().sort_values(ascending =False).plot(kind='bar',  figsize=(7,5))
plt.ylabel('Count')
plt.title('Number of Deaths in each month from (2012-2018)')


lookup={11:'Autumn',12:'Winter',1:'Winter',2:'Winter',3:'Spring',4:'Spring',5:'Spring',6:'Summer',7:'Summer',8:'Summer',9:'Autumn',10:'Autumn'}
mydata['Season']=mydata['new_date'].dt.month.apply(lambda x: lookup[x])
mydata.loc[:,'multiple_drugs_used':'Season'].head()

mydata['Season'].value_counts()

mydata['Season'].value_counts().plot(kind='bar',figsize=(7,5))
plt.ylabel('Count')
plt.title('Number of Deaths for each season')
# Number of deaths caused by one drug (top 5)
one_drug=mydata[(mydata['drugs_count']==1)].groupby('multiple_drugs_used')['multiple_drugs_used'].count()
one_drug[one_drug>50].sort_values().plot(kind='bar',figsize=(7,5))
plt.ylabel('Count of Deaths')
plt.title('Count of Fatalities due to use of one drug ')

one_drug[one_drug>50].sort_values()

# Number of deaths caused by two drugs 
two_drug=mydata[(mydata['drugs_count']==2)].groupby('multiple_drugs_used')['multiple_drugs_used'].count()
two_drug[two_drug>50].sort_values().plot(kind='bar', figsize=(7,5))
plt.ylabel('Count of Deaths')
plt.title('Count of Fatalities due combination of two drugs ')

two_drug[two_drug>50].sort_values()

# Number of deaths associated by three drugs

three_drug=mydata[(mydata['drugs_count']==3)].groupby('multiple_drugs_used')['multiple_drugs_used'].count()
three_drug[three_drug>50].sort_values().plot(kind='bar', figsize=(7,5))
plt.ylabel('Count of Deaths')
plt.title('Count of Fatalities due combination of Three drugs ')
 
three_drug[three_drug>50].sort_values()


# Deaths associated with combinations of drugs
mydata.groupby('drugs_count')['drugs_count'].count().plot(kind='bar',figsize=(7,5))
plt.ylabel('Count')
plt.title('Deaths associated with combinations of drugs')


# drugs which is most dangerous over years

dang_drugs=mydata.groupby(['Year','multiple_drugs_used'])['Year'].size().reset_index(name='count')

dang_drugs2=dang_drugs[dang_drugs['multiple_drugs_used'].isin(list(multiple_drugs_count[multiple_drugs_count>100].index))].reset_index(drop=True)


dang_drugs2.pivot(*dang_drugs2.columns).plot(kind='bar', legend=True, figsize=(15,8))
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.ylabel('Count')
plt.title('Most used drugs over years')


# PLot to see which age group is affected most
# Creating a new column for age group as age range

min(mydata['Age'])

bins = [0, 29, 39, 49,59,69, 70]
labels = ['0-29', '30-39', '40-49', '50-59', '60-69', '70+']
mydata['agerange'] = pd.cut(mydata.Age, bins, labels = labels,include_lowest = True)

mydata.groupby('agerange')['agerange'].count()


mydata.groupby('agerange')['agerange'].count().plot(kind='bar',figsize=(7,5))
plt.ylabel('Count')
plt.title('Number of Deaths by Age Group')


# Deaths per Age group and sex plot


mydata[mydata['Sex']!='Unknown'].groupby(['agerange','Sex'])['Sex'].count().unstack().plot(kind='bar',figsize=(7,5))
plt.ylabel('Count')
plt.title('Number of Deaths by Age Group and Gender')

## Plot deaths of male and females for each year

mydata[mydata['Sex']!='Unknown'].groupby(['Year','Sex'])['Sex'].count().unstack().plot(kind='line',figsize=(7,5))
plt.ylabel('Count')
plt.title('Number of Deaths of each gender across 2012-2018')

# plot for deaths by race

mydata['Race'].value_counts().plot(kind='bar',figsize=(7,5))
plt.ylabel('Count')
plt.title('Number of Deaths of each race')


mydata['Race'].value_counts()

# Avg age  for each race grouped by sex

mydata[mydata['Sex']!='Unknown'].groupby(['Race','Sex'])['Age'].mean().unstack().plot(kind='bar',figsize=(7,5))
plt.ylabel('Avg Age')
plt.title('Avg Age for Deaths of each race')
# Count of deaths for each race grouped by gender

mydata[mydata['Sex']!='Unknown'].groupby(['Race','Sex'])['Sex'].count().unstack().sort_values( 'Male').plot(kind='bar',figsize=(7,5))
plt.ylabel('Count')
plt.title('Number of Deaths for each Race grouped by Sex')



# Drugs Related Deaths by City

mydata['DeathCity'].value_counts()


# Top 15 cities

mydata['DeathCity'].value_counts().nlargest(15).plot(kind='bar',figsize=(7,5))
plt.ylabel('Count')
plt.title('Number of Deaths in each city (top 15)')








