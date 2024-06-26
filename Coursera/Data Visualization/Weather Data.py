# coding: utf-8

# # Assignment 2
#
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
#
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/3e180a8aae51042ce0ee942fba8c356d33c2789b8e38fa866113178e.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
#
# Each row in the assignment datafile corresponds to a single observation.
#
# The following variables are provided to you:
#
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
#
# For this assignment, you must:
#
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
#
# The data you have been given is near **Hackettstown, New Jersey, United States**, and the stations the data comes from are shown on the map below.


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplleaflet
import datetime as dt
import pandas as pd
import numpy as np


def leaflet_plot_stations():
    df = pd.read_csv('NOAA Dataset.csv')

    recordMin = [9999] * 365;
    recordMax = [-9999] * 365;
    min2015 = [9999] * 365;
    max2015 = [-9999] * 365;
    df["Date"] = pd.to_datetime(df["Date"])
    df = df[~((df["Date"].dt.month == 2) & (df["Date"].dt.day == 29))]
    df["Year"] = pd.DatetimeIndex(df["Date"]).year
    df["DayOfYear"] = df["Date"].dt.dayofyear
    condition = (df["DayOfYear"] > 60) & (df["Date"].dt.is_leap_year)
    df.loc[condition, "DayOfYear"] -= 1
    df["Data_Value"] = df["Data_Value"] / 10
    df_2015 = df[df["Year"] == 2015]
    df_not_2015 = df[df["Year"] != 2015]
    df_not_2015_min = df_not_2015.groupby(by=["DayOfYear"]).min()
    df_not_2015_max = df_not_2015.groupby(by=["DayOfYear"]).max()
    df_2015_min = df_2015.groupby(by=["DayOfYear"]).min()
    df_2015_max = df_2015.groupby(by=["DayOfYear"]).max()

    start = dt.datetime(2015, 1, 1)
    end = dt.datetime(2015, 12, 31)

    x = [];
    while start <= end:
        x.append(start)
        start += dt.timedelta(days=1)

    colorMin = ['#cccccc'] * len(recordMax)
    for i in range(0, len(colorMin) - 1):
        if df_2015_min["Data_Value"].iloc[i] < df_not_2015_min["Data_Value"].iloc[i]:
            colorMin[i] = 'b'

    colorMax = ['#cccccc'] * len(recordMax)
    for i in range(0, len(colorMax) - 1):
        if df_2015_max["Data_Value"].iloc[i] > df_not_2015_max["Data_Value"].iloc[i]:
            colorMax[i] = 'r'

    fig = plt.figure(figsize=(12, 6))
    fig.patch.set_alpha(1)

    plt.plot(x, df_not_2015_min["Data_Value"], color="#888888", label='_nolegend_')
    plt.plot(x, df_not_2015_max["Data_Value"], color="#888888", label='_nolegend_')
    plt.fill_between(x, df_not_2015_min["Data_Value"], df_not_2015_max["Data_Value"],
                     facecolor='#cccccc', label="Temperature range for 2005-2014")
    plt.scatter(x, df_2015_min["Data_Value"], c=colorMin, s=5, label="Min temp 2015")
    plt.scatter(x, df_2015_max["Data_Value"], c=colorMax, s=5, label="Max Temp 2015")

    plt.title("Breaking Record Temperatures in 2015 at Hackettstown, NJ")
    plt.xlabel("Month")
    plt.ylabel("Temperatures in degrees celsius")

    leg = plt.legend(loc="lower center")
    leg.legendHandles[0].set_color('#cccccc')
    leg.legendHandles[1].set_color('b')
    leg.legendHandles[2].set_color('r')

    locator = mdates.MonthLocator()
    fmt = mdates.DateFormatter("%b")
    X = plt.gca().xaxis
    X.set_major_locator(locator)
    X.set_major_formatter(fmt)

    plt.show()
    plt.savefig("assignment2.png", facecolor=fig.get_facecolor())


leaflet_plot_stations()
