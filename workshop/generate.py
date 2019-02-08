'''
Script that generates data for you to run the exercise.

Columns of data based on NHS+ODI Leeds blog post:
https://odileeds.org/blog/2019-01-24-exploring-methods-for-creating-synthetic-a-e-data

'''
import os
import random
from datetime import datetime, timedelta

import pandas as pd

import filepaths

# TODO: add in probabilities for each of these 

num_of_rows = 10

def main():
    # postcodes = generate_postcodes()
    # hospitals = generate_hospitals()
    arrival_dates, arrival_times = generate_arrival_dates_times()

def generate_postcodes() -> list:
    ''' Reads a .csv containing info on every London postcode. Reads the 
    postcodes in use and returns them. 
    '''
    # Where a patient lives
    # List of London postcodes retrieved from https://www.doogal.co.uk/PostcodeDownloads.php
    postcodes_df = pd.read_csv(filepaths.postcodes_london)
    postcodes_in_use = list(postcodes_df[postcodes_df['In Use?'] == "No"]['Postcode'])
    postcodes = random.choices(postcodes_in_use, k=num_of_rows)
    return postcodes


def generate_hospitals() -> list:
    # Individual Hospitals
    # List of London NHS hospitals retrieved from https://en.wikipedia.org/wiki/Category:NHS_hospitals_in_London
    with open(filepaths.nhs_hospitals_london, 'r') as file_in:
        hospitals = file_in.readlines()
    hospitals = [name.strip() for name in hospitals]
    hospitals = random.choices(hospitals, k=num_of_rows)
    return hospitals


def generate_arrival_dates_times() -> (list, list):
    arrival_dates, arrival_times = [], []

    for _ in range(num_of_rows):
        random_datetime = gen_datetime()
        breakpoint()

    return arrival_dates, arrival_times


def gen_datetime(min_year=2019, max_year=datetime.now().year):
# generate a datetime in format yyyy-mm-dd hh:mm:ss.000000
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    random_datetime = start + (end - start) * random.random()
    return random_datetime

# Arrival date, arrival time


# time in a&e


if __name__ == "__main__":
    main()
