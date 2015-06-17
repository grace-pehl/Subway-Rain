# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 21:44:07 2015

@author: Grace Pehl
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas
import scipy
import scipy.stats
import statsmodels.api as sm


def entries_histogram(turnstile_weather):
    '''
    plot a histograph of entries with or without rain
    '''
    plt.figure()
    tw = turnstile_weather
    raining = tw[tw["rain"] == 1]
    not_raining = tw[tw["rain"] == 0]
    not_raining['ENTRIESn_hourly'].hist(bins=50, range=[0, 4000],
                                        label="Days Without Rain")
    raining['ENTRIESn_hourly'].hist(bins=50, range=[0, 4000],
                                    label="Days With Rain")
    plt.xlabel('Number of Hourly Subway Entries')
    plt.ylabel('Number of Occurrences')
    plt.title('NYC Subway Entries on Days With or Without Rain')
    plt.legend()
    return plt


def mann_whitney_plus_means(turnstile_weather):
    '''
    This function will take in the turnstile_weather dataframe containing
    our final turnstile weather data. You will want to take the means and run
    the Mann Whitney U-test on the ENTRIESn_hourly column in the
    turnstile_weather dataframe.
    '''
    tw = turnstile_weather
    raining = tw[tw["rain"] == 1]
    not_raining = tw[tw["rain"] == 0]
    with_rain_mean = np.mean(raining['ENTRIESn_hourly'])
    without_rain_mean = np.mean(not_raining['ENTRIESn_hourly'])
    (U, p) = scipy.stats.mannwhitneyu(raining['ENTRIESn_hourly'],
                                      not_raining['ENTRIESn_hourly'])
    return with_rain_mean, without_rain_mean, U, p


def linear_regression(features, values):
    """
    Perform linear regression given a data set with an arbitrary number of
    features.
    """
    x_values = sm.add_constant(features)
    model = sm.OLS(values, x_values, hasconst=True)
    results = model.fit()
    all_params = results.params
    intercept = all_params[0]
    params = all_params[1:]
    return intercept, params


def predictions(dataframe):
    '''
    The NYC turnstile data is stored in a pandas dataframe called
    weather_turnstile. Using the information stored in the dataframe, let's
    predict the ridership of the NYC subway using linear regression with
    gradient descent.
    '''
    # Select Features (try different features!)
    features = dataframe[['rain', 'precipi', 'Hour', 'mintempi',
                          'meanwindspdi']]
    # Add UNIT to features using dummy variables
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    features = features.join(dummy_units)
    # Values
    values = dataframe['ENTRIESn_hourly']
    # Get the numpy arrays
    features_array = features.values
    values_array = values.values
    # Perform linear regression
    intercept, params = linear_regression(features_array, values_array)
    predictions = intercept + np.dot(features_array, params)
    return predictions


def plot_residuals(turnstile_weather, predictions):
    '''
    Using the same methods that we used to plot a histogram of entries
    per hour for our data, why don't you make a histogram of the residuals
    (that is, the difference between the original hourly entry data and the
    predicted values). Try different binwidths for your histogram.
    '''
    plt.figure()
    residuals = turnstile_weather["ENTRIESn_hourly"] - predictions
    residuals.hist(bins=50, range=[-5000, 5000])
    plt.title("Residuals After Linear Regression")
    return plt


def compute_r_squared(data, predictions):
    '''
    In exercise 5, we calculated the R^2 value for you. But why don't you try
    and calculate the R^2 value yourself.
    Given a list of original data points, and also a list of predicted data
    points, write a function that will compute and return the coefficient of
    determination (R^2) for this data.
    '''
    y_bar = np.mean(data)
    numerator = np.sum((data - predictions)**2)
    denominator = np.sum((data - y_bar)**2)
    r_squared = 1 - numerator/denominator
    return r_squared
