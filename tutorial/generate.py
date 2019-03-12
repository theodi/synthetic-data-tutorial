"""
Script that generates data to use in the synthetic data tutorial.

Columns of data inpired by NHS+ODI Leeds blog post:
https://odileeds.org/blog/2019-01-24-exploring-methods-for-creating-synthetic-a-e-data

"""

import os
import random
from datetime import datetime, timedelta
import uuid
import random, string
import time

import pandas as pd
import numpy as np
import scipy.stats as stats

import filepaths

# TODO: add in probabilities for some attributes
# TODO: add correlations between attributes
# TODO: give hospitals different average waiting times

num_of_rows = 10000

def main():
    print('generating data...')
    start = time.time()

    nhs_ae_dataset = {}

    print('generating A&E admission IDs...')
    nhs_ae_dataset['Attendance ID'] = generate_admission_ids()

    print('generating NHS numbers...')
    nhs_ae_dataset['NHS number'] = generate_nhs_numbers()

    print('generating hospital instances...')
    nhs_ae_dataset['Hospital'] = generate_hospitals()

    print('generating arrival times...')
    nhs_ae_dataset['Arrival Time'] = generate_arrival_times()

    print('generating times spent in A&E...')
    nhs_ae_dataset['Time in A&E (mins)'] = generate_times_in_ae()

    print('generating A&E treaments...')
    nhs_ae_dataset['Treatment'] = generate_treatments()

    print('generating patient gender instances...')
    nhs_ae_dataset['Gender'] = generate_genders()

    print('generating patient ages...')
    nhs_ae_dataset['Age'] = generates_ages()

    print('generating patient postcodes...')
    nhs_ae_dataset['Postcode'] = generate_postcodes()

    write_out_dataset(nhs_ae_dataset, filepaths.nhs_ae_data)
    print('dataset written out to: ', filepaths.nhs_ae_data)

    elapsed = round(time.time() - start, 2)
    print('done in ' + str(elapsed) + ' seconds.')


def generate_admission_ids() -> list:
    """ Generate a unique 10-digit ID for every admission record """
    
    uids = []
    for _ in range(num_of_rows):    
        x = ''.join(random.choice(string.digits) for _ in range(10))
        uids.append(x)
    return uids

def generate_nhs_numbers() -> list:
    """ Generate dummy NHS numbers similar to 10 digit format
    See: https://www.nhs.uk/using-the-nhs/about-the-nhs/what-is-an-nhs-number/
    """
    nhs_numbers = []
    for _ in range(num_of_rows): 
        nhs_number = ''.join(random.choice(string.digits) for _ in range(3)) + '-'   
        nhs_number = ''.join(random.choice(string.digits) for _ in range(3)) + '-'   
        nhs_number = ''.join(random.choice(string.digits) for _ in range(4))
        nhs_numbers.append(nhs_number)
    return nhs_numbers


def generate_postcodes() -> list:
    """ Reads a .csv containing info on every London postcode. Reads the 
    postcodes in use and returns a sample of them.

    # List of London postcodes from https://www.doogal.co.uk/PostcodeDownloads.php
    """
    postcodes_df = pd.read_csv(filepaths.postcodes_london)
    postcodes_in_use = list(postcodes_df[postcodes_df['In Use?'] == "No"]['Postcode'])
    postcodes = random.choices(postcodes_in_use, k=num_of_rows)
    return postcodes


def generate_hospitals() -> list:
    """ Reads the data/hospitals_london.txt file, and generates a
    sample of them to add to the dataset.

    List of London NHS hospitals loosely based on 
    https://en.wikipedia.org/wiki/Category:NHS_hospitals_in_London
    """
    with open(filepaths.nhs_hospitals_london, 'r') as file_in:
        hospitals = file_in.readlines()
    hospitals = [name.strip() for name in hospitals]
    hospitals = random.choices(hospitals, k=num_of_rows)
    return hospitals


def generate_arrival_times() -> list:
    """ Generate and return arrival times.
        Hardcoding times to first week of April 2019
    """
    arrival_times = []
    start = datetime(2019, 4, 1, 00, 00, 00)
    end = datetime(2019, 4, 6, 23, 59, 59)

    for _ in range(num_of_rows):
        random_datetime = start + (end - start) * random.random()
        arrival_times.append(random_datetime.strftime('%Y-%m-%d %H:%M:%S'))

    return arrival_times


def generate_times_in_ae() -> list:
    """ Generate and return length of times in A&E.
    Method included tries to get a good spread around the mean without
    going below 1 minute or above 720 minutes (chosen arbitrarily).
    """
    lower, upper = 1, 720
    mu, sigma = 30, 100
    # Normal distribution with upper and lower limits solution from stackoverflow
    # https://stackoverflow.com/questions/18441779/how-to-specify-upper-and-lower-limits-when-using-numpy-random-normal/44603019
    X = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
    times_in_ae = X.rvs(num_of_rows).astype(int)
    return times_in_ae


def generate_genders() -> list:
    """ Generate and return list of genders for every row. 

    # National codes for gender in NHS data
    # https://www.datadictionary.nhs.uk/data_dictionary/attributes/p/person/person_gender_code_de.asp?shownav=1
    """
    gender_codes_df = pd.read_csv(filepaths.nhs_ae_gender_codes)
    genders = gender_codes_df['Gender'].tolist()
    # these weights are just dummy values. please don't take them as accurate.
    weights =[0.005, 0.495, 0.495, 0.005]
    gender_codes = random.choices(genders, k=num_of_rows, weights=weights)
    return gender_codes


def generates_ages() -> list:
    """ Generate and return sample of ages 

    Reads London age distribution file, generates ages based on those (max 100),
    returns the list. 

    # London population age groups populations based on 2011 census:
    # https://data.london.gov.uk/dataset/census-2011-population-age-uk-districts
    """

    age_population_london_df = pd.read_csv(filepaths.age_population_london)
    weights = age_population_london_df['Population'].tolist()
    age_brackets_start = [
        int(age_bracket.split('-')[0]) 
        for age_bracket in
        age_population_london_df['Age bracket'].tolist()
    ]
    age_brackets = random.choices(
        age_brackets_start, k=num_of_rows, weights=weights)
    ages = [generate_age(age_bracket) for age_bracket in age_brackets]
    return ages


def generate_age(age: int) -> int:
    if age == 90: 
        return random.randint(90, 100) 
    else:
        return random.randint(age, age+4)


def generate_treatments() -> list:
    """ Generate and return sample of treatments patients received. 

    Reads data/treatment_codes_nhs_ae.csv file 
    generates ages based on those (max 100)
    returns the list. 

    NHS treatment codes:
    https://www.datadictionary.nhs.uk/web_site_content/supporting_information/clinical_coding/accident_and_emergency_treatment_tables.asp?shownav=1
    """

    treatment_codes_df = pd.read_csv(filepaths.nhs_ae_treatment_codes)
    treatments = treatment_codes_df['Treatment'].tolist()
    treatment_codes = random.choices(treatments, k=num_of_rows)
    return treatment_codes


def write_out_dataset(dataset: dict, filepath: str):
    """Writing dataset to .csv file

    Keyword arguments:
    dataset -- the dataset to be written to disk
    filepath -- path to write the file out to
    """

    df = pd.DataFrame.from_dict(dataset)
    df.to_csv(filepath, index=False)


if __name__ == "__main__":
    main()
