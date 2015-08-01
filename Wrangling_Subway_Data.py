# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 13:40:58 2015

@author: Grace Pehl
"""
import csv
import pandas
import pandasql
from datetime import datetime


def num_rainy_days(filename):
    '''
    This function should run a SQL query on a dataframe of
    weather data.  The SQL query should return one column and
    one row - a count of the number of days in the dataframe where
    the rain column is equal to 1 (i.e., the number of days it
    rained).
    '''
    weather_data = pandas.read_csv(filename)
    # Create SQL command
    q = """
    SELECT COUNT(rain) FROM weather_data WHERE cast(rain as integer) = 1
    """
    # Execute your SQL command against the pandas frame
    rainy_days = pandasql.sqldf(q.lower(), locals())
    return rainy_days


def max_temp_aggregate_by_fog(filename):
    '''
    This function should run a SQL query on a dataframe of
    weather data.  The SQL query should return two columns and
    two rows - whether it was foggy or not (0 or 1) and the max
    maxtempi for that fog value (i.e., the maximum max temperature
    for both foggy and non-foggy days).  The dataframe will be
    titled 'weather_data'. You'll need to provide the SQL query.
    '''
    weather_data = pandas.read_csv(filename)
    # Create SQL command
    q = """
    SELECT cast(fog as integer), MAX(cast(maxtempi as integer)) FROM \
    weather_data GROUP BY fog
    """
    # Execute your SQL command against the pandas frame
    foggy_days = pandasql.sqldf(q.lower(), locals())
    return foggy_days


def avg_weekend_temperature(filename):
    '''
    This function should run a SQL query on a dataframe of
    weather data.  The SQL query should return one column and
    one row - the average meantempi on days that are a Saturday
    or Sunday (i.e., the the average mean temperature on weekends).
    The dataframe will be titled 'weather_data'.
    '''
    weather_data = pandas.read_csv(filename)
    # Create SQL command
    q = """
    SELECT avg(meantempi) FROM weather_data WHERE cast(strftime('%w', date) as\
     integer) = 0 or cast(strftime('%w', date) as integer) = 6
    """
    # Execute your SQL command against the pandas frame
    mean_temp_weekends = pandasql.sqldf(q.lower(), locals())
    return mean_temp_weekends


def avg_min_temperature(filename):
    '''
    This function should run a SQL query on a dataframe of
    weather data. More specifically you want to find the average
    minimum temperature (mintempi column of the weather dataframe) on
    rainy days where the minimum temperature is greater than 55 degrees.
    '''
    weather_data = pandas.read_csv(filename)
    # Create SQL query
    q = """
    SELECT avg(cast(mintempi as integer)) FROM weather_data WHERE cast(rain as\
    integer) = 1 and cast(mintempi as integer) > 55
    """
    # Execute your SQL command against the pandas frame
    avg_min_temp_rainy = pandasql.sqldf(q.lower(), locals())
    return avg_min_temp_rainy


def fix_turnstile_data(filenames):
    '''
    You want to write a function that will update each row in the text
    file so there is only one entry per row.
    '''
    for name in filenames:
        f_in = open(name, "r")
        updated_filename = "updated_" + str(name)
        f_out = open(updated_filename, "w")

        reader_in = csv.reader(f_in, delimiter=',')

        for line in reader_in:
            num_records = (len(line) - 3) / 5
            initial = "%s,%s,%s" % (line[0], line[1], line[2])
            for number in range(num_records):
                record = initial
                for num in range(3, 8):
                    record += "," + line[number*5+num]
                f_out.write(record+'\n')

        f_in.close()
        f_out.close()


def create_master_turnstile_file(filenames, output_file):
    '''
    Write a function that takes the files in the list filenames, which all have
    the columns 'C/A, UNIT, SCP, DATEn, TIMEn, DESCn, ENTRIESn, EXITSn', and
    consolidates them into one file located at output_file.  There should be
    ONE row with the column headers, located at the top of the file. The input
    files do not have column header rows of their own.
    '''
    with open(output_file, 'w') as master_file:
        master_file.write('C/A,UNIT,SCP,DATEn,TIMEn,DESCn,ENTRIESn,EXITSn\n')
        for name in filenames:
            f_in = open(name, "r")
            for line in f_in:
                master_file.write(line)
            f_in.close()


def filter_by_regular(filename):
    '''
    This function should read the csv file located at filename into a pandas
    dataframe, and filter the dataframe to only rows where the 'DESCn' column
    has the value 'REGULAR'.
    '''
    df = pandas.read_csv(filename)
    turnstile_data = df[df['DESCn'] == 'REGULAR']
    return turnstile_data


def get_hourly_entries(df):
    '''
    The data in the MTA Subway Turnstile data reports on the cumulative
    number of entries and exits per row.  Assume that you have a dataframe
    called df that contains only the rows for a particular turnstile machine
    (i.e., unique SCP, C/A, and UNIT).  This function should change
    these cumulative entry numbers to a count of entries since the last reading
    (i.e., entries since the last row in the dataframe).
    '''
    df['ENTRIESn_hourly'] = df['ENTRIESn'] - df['ENTRIESn'].shift(1)
    df = df.fillna(1)
    return df


def get_hourly_exits(df):
    df['EXITSn_hourly'] = df['EXITSn'] - df['EXITSn'].shift(1)
    df = df.fillna(0)
    return df


def time_to_hour(time):
    '''
    Given an input variable time that represents time in the format of:
    "00:00:00" (hour:minutes:seconds) Write a function to extract the hour part
    from the input variable time and return it as an integer.
    '''
    hour = int(time[0:2])
    return hour


def reformat_subway_dates(date):
    '''
    The dates in our subway data are formatted in the format month-day-year.
    The dates in our weather underground data are formatted year-month-day.
    Write a function that takes as its input a date in the MTA Subway
    data format, and returns a date in the weather underground format.
    '''
    date_formatted = str(datetime.strptime(date, "%m-%d-%y"))
    return date_formatted[:10]
