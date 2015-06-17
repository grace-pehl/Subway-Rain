# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 17:57:47 2015

@author: Grace Pehl
"""

from pandas import *
from ggplot import *
import numpy as np


def plot_weather_data(turnstile_weather):
    '''
    You are passed in a dataframe called turnstile_weather.
    Use turnstile_weather along with ggplot to make a data visualization
    focused on the MTA and weather data we used in assignment #3.
    You should feel free to implement something that we discussed in class
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.
    '''
    hourly = []
    for i in range(24):
        single_hour_data = turnstile_weather[turnstile_weather.Hour == i]
        hourly.append(np.mean(single_hour_data['ENTRIESn_hourly']))
    temp = {"Hour": range(24), "Riders": hourly}
    hourly_riders = pandas.DataFrame(temp)
    plot = ggplot(hourly_riders, aes("Hour", "Riders")) \
        + xlab("Hour of the Day") + ylab('Average Number of MTA Riders') \
        + ylim(0, 3000) + xlim(0, 23) \
        + scale_x_continuous(breaks=range(2, 22, 2)) + geom_point() \
        + geom_line() + ggtitle("MTA Ridership Throughout the Day")
    return plot


def plot_weather_data2(turnstile_weather):
    '''
    plot_weather_data is passed a dataframe called turnstile_weather.
    Use turnstile_weather along with ggplot to make another data visualization
    focused on the MTA and weather data we used in Project 3.  Make a type of
    visualization different than what you did in the previous exercise.
    Try to use the data in a different way (e.g., if you made a lineplot
    concerning ridership and time of day in exercise #1, maybe look at weather
    and try to make a histogram in this exercise). Or try to use multiple
    encodings in your graph if you didn't in the previous exercise.
    '''

    plot = ggplot(turnstile_weather, aes('meanwindspdi')) \
        + geom_histogram(binwidth=1) + xlab("Mean Wind Speed") \
        + ggtitle("Average Daily Wind Speed in Manhattan, NY") \
        + ylab("MTA Station Measurements")
    return plot
