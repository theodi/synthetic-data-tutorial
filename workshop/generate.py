'''
Script that generates data for you to run the exercise.

Columns of data based on NHS+ODI Leeds blog post:
https://odileeds.org/blog/2019-01-24-exploring-methods-for-creating-synthetic-a-e-data

'''
import os
import random
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import scipy.stats as stats

import filepaths

# TODO: add in probabilities for each of these 
# TODO: give hospitals different average waiting times

num_of_rows = 50

def main():
    postcodes = generate_postcodes()
    hospitals = generate_hospitals()
    arrival_dates, arrival_times = generate_arrival_dates_times()
    times_in_ae = generate_times_in_ae()
    genders = generate_gender_codes()
    ages = generates_ages()
    treatment_codes = generate_treatment_codes()
    breakpoint()

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
    # hardcoding times to first week of April 2019
    arrival_dates, arrival_times = [], []
    start = datetime(2019, 4, 1, 00, 00, 00)
    end = datetime(2019, 4, 6, 23, 59, 59)

    for _ in range(num_of_rows):
        random_datetime = start + (end - start) * random.random()
        arrival_dates.append(random_datetime.strftime('%Y-%m-%d'))
        arrival_times.append(random_datetime.strftime('%H:%M:%S'))

    return arrival_dates, arrival_times


def generate_times_in_ae() -> list:
    lower, upper = 1, 720
    mu, sigma = 30, 100
    # https://stackoverflow.com/questions/18441779/how-to-specify-upper-and-lower-limits-when-using-numpy-random-normal/44603019
    X = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
    times_in_ae = X.rvs(num_of_rows).astype(int)
    return times_in_ae


def generate_gender_codes() -> list:
    # national codes for gender in NHS data
    # https://www.datadictionary.nhs.uk/data_dictionary/attributes/p/person/person_gender_code_de.asp?shownav=1
    gender_codes = random.choices(
        [0, 1, 2, 9], k=num_of_rows, weights=[0.01, 0.49, 0.49, 0.01]
    )
    return gender_codes


def generates_ages() -> list:
    # UK population age groups percentages
    # https://www.ethnicity-facts-figures.service.gov.uk/british-population/demographics/age-groups/latest
    age_brackets = random.choices(
        [0, 5, 10, 15, 18, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85],
        k=num_of_rows, 
        weights=[0.062, 0.056, 0.058, 0.037, 0.094, 0.068, 0.066, 0.067, 0.073, 0.073,
            0.064, 0.057, 0.06, 0.048, 0.039, 0.032, 0.024, 0.022]
    )
    ages = [generate_age(age_bracket) for age_bracket in age_brackets]
    return ages


def generate_age(age_bracket: int) -> int:
    if age_bracket == 0: return random.randint(0, 4)
    elif age_bracket == 5: return random.randint(5, 9) 
    elif age_bracket == 10: return random.randint(10, 14) 
    elif age_bracket == 15: return random.randint(15, 17) 
    elif age_bracket == 18: return random.randint(18, 24) 
    elif age_bracket == 25: return random.randint(25, 29) 
    elif age_bracket == 30: return random.randint(30, 34) 
    elif age_bracket == 35: return random.randint(35, 39) 
    elif age_bracket == 40: return random.randint(40, 44) 
    elif age_bracket == 45: return random.randint(45, 49) 
    elif age_bracket == 50: return random.randint(50, 54) 
    elif age_bracket == 55: return random.randint(55, 59) 
    elif age_bracket == 60: return random.randint(60, 64) 
    elif age_bracket == 65: return random.randint(65, 69) 
    elif age_bracket == 70: return random.randint(70, 74) 
    elif age_bracket == 75: return random.randint(75, 79) 
    elif age_bracket == 80: return random.randint(80, 84) 
    elif age_bracket == 85: return random.randint(85, 100) 


if __name__ == "__main__":
    main()
