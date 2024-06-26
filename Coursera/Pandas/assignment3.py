#!/usr/bin/env python
# coding: utf-8

# # Assignment 3
# All questions are weighted the same in this assignment.
# This assignment requires more individual learning then the last one did
# You are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/)
# to find functions or methods you might not have used yet,
# or ask questions on [Stack Overflow](http://stackoverflow.com/)
# and tag them as pandas and python related.
# All questions are worth the same number of points except question 1 which is worth 17% of the assignment grade.
# 
# **Note**: Questions 3-13 rely on your question 1 answer.


import pandas as pd
import numpy as np

# Filter all warnings. If you would like to see the warnings, please comment the two lines below.
import warnings
warnings.filterwarnings('ignore')


# ### Question 1
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and
# renewable electricity production](Energy%20Indicators.xls) from the [United Nations]
# (http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013,
# and should be put into a DataFrame with the variable name of **Energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file.
# Also, make sure to exclude the footer and header information from the datafile.
# The first two columns are unneccessary, so you should get rid of them,
# and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable]`
# 
# Convert `Energy Supply` to gigajoules (**Note: there are 1,000,000 gigajoules in a petajoule**).
# For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name.
# Be sure to remove these,
# e.g. `'Bolivia (Plurinational State of)'` should be `'Bolivia'`.  `'Switzerland17'` should be `'Switzerland'`.
# 
# Next, load the GDP data from the file `world_bank.csv`,
# which is a csv containing countries' GDP from 1960 to 2015 from
# [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD).
# Call this DataFrame **GDP**.
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology]
# (http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`,
# which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names).
# Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank'
# (Rank 1 through 15).
# 
# The index of this DataFrame should be the name of the country,
# and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries,
# and the rows of the DataFrame should be sorted by "Rank".*
pd.set_option('display.max_rows', None, 
              'display.max_columns', None,
              'display.precision', 3)


def answer_one():
    # YOUR CODE HERE
    Energy = pd.read_excel(io='Energy Indicators.xls', skiprows=17, skipfooter=38)
    Energy.drop(['Unnamed: 0', 'Unnamed: 1'], axis=1, inplace=True)
    Energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    Energy.replace('...', np.NaN, inplace=True)
    Energy['Energy Supply'] *= 1000000

    pattern = r"([^0-9\(\)]+)"
    Energy['Country'] = Energy['Country'].str.extract(pattern)
    Energy['Country'] = Energy['Country'].str.strip()

    Energy.set_index(['Country'], inplace=True)
    Energy.rename(index={"Republic of Korea": "South Korea",
                        "United States of America": "United States",
                        "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                        "China, Hong Kong Special Administrative Region": "Hong Kong"}, inplace=True)

    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    GDP.rename(columns={'Country Name': 'Country'}, inplace=True)
    GDP.set_index(['Country'], inplace=True)
    GDP.rename(index={"Korea, Rep.": "South Korea", 
                         "Iran, Islamic Rep.": "Iran",
                         "Hong Kong SAR, China": "Hong Kong"}, inplace=True)

    ScimEn = pd.read_excel(io='scimagojr-3.xlsx')
    ScimEn.set_index(['Country'], inplace=True)
    
    ScimEn_Energy = pd.merge(ScimEn, Energy, how='inner', 
                             left_index=True, right_index=True)
    ScimEn_Energy_GDP = pd.merge(ScimEn_Energy, GDP, how='inner',
                                left_index=True, right_index=True)

    ScimEn_Energy_GDP = ScimEn_Energy_GDP[ScimEn_Energy_GDP['Rank'] <= 15]
    ScimEn_Energy_GDP = ScimEn_Energy_GDP[['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]

    return ScimEn_Energy_GDP

print(f"Answer 1: \n{answer_one()}")

answer_one()

# ### Question 2
# The previous question joined three datasets then reduced this to just the top 15 entries.
# When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*
def answer_two():
    # YOUR CODE HERE
    Energy = pd.read_excel(io='Energy Indicators.xls', skiprows=17, skipfooter=38)
    Energy.drop(['Unnamed: 0', 'Unnamed: 1'], axis=1, inplace=True)
    Energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    Energy.replace('...', np.NaN, inplace=True)
    Energy['Energy Supply'] *= 1000000

    pattern = r"([^0-9\(\)]+)"
    Energy['Country'] = Energy['Country'].str.extract(pattern)
    Energy['Country'] = Energy['Country'].str.strip()

    Energy.set_index(['Country'], inplace=True)
    Energy.rename(index={"Republic of Korea": "South Korea",
                        "United States of America": "United States",
                        "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                        "China, Hong Kong Special Administrative Region": "Hong Kong"}, inplace=True)

    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    GDP.rename(columns={'Country Name': 'Country'}, inplace=True)
    GDP.set_index(['Country'], inplace=True)
    GDP.rename(index={"Korea, Rep.": "South Korea", 
                         "Iran, Islamic Rep.": "Iran",
                         "Hong Kong SAR, China": "Hong Kong"}, inplace=True)

    ScimEn = pd.read_excel(io='scimagojr-3.xlsx')
    ScimEn.set_index(['Country'], inplace=True)
    
    intersection = pd.merge(ScimEn, Energy, how='inner', 
                             left_index=True, right_index=True)
    intersection = pd.merge(intersection, GDP, how='inner',
                                left_index=True, right_index=True)
    union = pd.merge(ScimEn, Energy, how='outer', 
                             left_index=True, right_index=True)
    union = pd.merge(union, GDP, how='outer',
                                left_index=True, right_index=True)
    
    diff = union.shape[0] - intersection.shape[0]
    return diff

print(f"Answer 2: \n{answer_two()}")

# ### Question 3
# What are the top 15 countries for average GDP over the last 10 years?
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending
# order.*
def answer_three():
    # YOUR CODE HERE
    GDP = answer_one()
    GDP['avgGDP'] = np.nanmean(GDP.loc[:,'2006':'2015'], axis=1)
    GDP.sort_values(by=['avgGDP'], ascending=False, inplace=True)
    return GDP['avgGDP']

print(f"Answer 3:\n {answer_three()}")


# ### Question 4
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*
def answer_four():
    # YOUR CODE HERE
    GDP = answer_one()
    GDP.sort_values(by=['2015'], ascending=False, inplace=True)
    sixthGDP = GDP.iloc[5]
    sixthGDPDiff = sixthGDP.loc['2015'] - sixthGDP.loc['2006']
    
    return sixthGDPDiff

print(f"Answer Four: {answer_four}")


# ### Question 5
# What is the mean energy supply per capita?
# 
# *This function should return a single number.*
def answer_five():
    # YOUR CODE HERE
    Energy = answer_one()
    mean_energy_per_capita = np.mean(Energy['Energy Supply per Capita'])
    return mean_energy_per_capita

print(f"Answer 5: {answer_five}")


# ### Question 6
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*
def answer_six():
    # YOUR CODE HERE
    Energy = answer_one()
    Renewable = Energy['% Renewable']
    Renewable = Renewable.sort_values(ascending=False)
    RenewableTuple = (Renewable.index[0], Renewable.values[0])
    return RenewableTuple

print(f"Answer 6: {answer_six()}")


# ### Question 7
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*
def answer_seven():
    # YOUR CODE HERE
    df = answer_one()
    df["citation ratio"] = df["Self-citations"]/df["Citations"]
    df = df.sort_values(by=["citation ratio"], ascending=False)
    first_country = df.iloc[0]
    citation_ratio_tuple =  (first_country.name, first_country.loc["citation ratio"])
    return citation_ratio_tuple

print(f"Answer 7: {answer_seven()}")


# ### Question 8
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return the name of the country*
def answer_eight():
    # YOUR CODE HERE
    df = answer_one()
    df["Population"] = df["Energy Supply"]/df["Energy Supply per Capita"]
    df.sort_values(by=["Population"], ascending=False)
    third_country = df.iloc[3]
    country_name = third_country.name
    return country_name

print(f"Answer 8: {answer_eight()}")


# ### Question 9
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita?
# Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs.
# Citable docs per Capita)*
def plot9():
    import matplotlib as plt

    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])

def answer_nine():
    # YOUR CODE HERE
    df = answer_one()
    df["Population"] = df["Energy Supply"]/df["Energy Supply per Capita"]
    df["Citable docs per Capita"] = df["Citable documents"]/df["Population"]
    df2 = df[["Citable docs per Capita", "Energy Supply per Capita"]]
    correlation = df2.corr()
    return correlation.iloc[0].iloc[1]

print(f"Answer 9: {answer_nine()}")
plot9()


# ### Question 10
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the
# top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of
# rank.*
def answer_ten():
    # YOUR CODE HERE
    df = answer_one()
    median_renew = np.median(df.loc[:, "% Renewable"])
    HighRenew = (df.loc[:, "% Renewable"] >= median_renew).astype("int32")
    return HighRenew

print(f"Answer 10:\n {answer_ten()}")


# ### Question 11
# Use the following dictionary to group the Countries by Continent, then create a DataFrame that displays the sample
# size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated
# population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with
# index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and
# columns `['size', 'sum', 'mean', 'std']`*
def answer_eleven():
    # YOUR CODE HERE
    df = answer_one()
    df["Population"] = df["Energy Supply"]/df["Energy Supply per Capita"]
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    
    df["Continent"] = df.index.map(ContinentDict)
    aggdf = df.groupby(by=["Continent"]).agg(['size', 'sum', 'mean', 'std'])
    aggdf = aggdf["Population"]
    return aggdf

print(f"Answer 11:\n {answer_eleven()}")


# ### Question 12
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins.
# How many countries are in each of these groups?
# 
# *This function should return a Series with a MultiIndex of `Continent`, then the bins for `% Renewable`.
# Do not include groups with no countries.*
def answer_twelve():
    # YOUR CODE HERE
    df = answer_one()
    df["% Renewable"] = pd.cut(df["% Renewable"], 5)
    ContinentDict  = {'China':'Asia', 
              'United States':'North America', 
              'Japan':'Asia', 
              'United Kingdom':'Europe', 
              'Russian Federation':'Europe', 
              'Canada':'North America', 
              'Germany':'Europe', 
              'India':'Asia',
              'France':'Europe', 
              'South Korea':'Asia', 
              'Italy':'Europe', 
              'Spain':'Europe', 
              'Iran':'Asia',
              'Australia':'Australia', 
              'Brazil':'South America'}
    
    df["Continent"] = df.index.map(ContinentDict)
    df = df.groupby(by=["Continent", "% Renewable"]).agg(["size"])
    df = df["Rank", "size"]
    
    return df

print(f"Answer 12:\n {answer_twelve()}")


# ### Question 13
# Convert the Population Estimate series to a string with thousands separator (using commas). \
# Use all significant digits (do not round the results).
# 
# e.g. 12345678.90 -> 12,345,678.90
# 
# *This function should return a series `PopEst` whose index is the country name and whose values are the population
# estimate string*
def answer_thirteen():
    # YOUR CODE HERE
    df = answer_one()
    df["Population"] = df["Energy Supply"]/df["Energy Supply per Capita"]
    PopEst = df["Population"].map("{:,}".format)
    PopEst = PopEst.astype(str)
    return PopEst

print(f"Answer 13:\n {answer_thirteen()}")


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.
def plot_optional():
    import matplotlib as plt

    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6])

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    # print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")

plot_optional()
