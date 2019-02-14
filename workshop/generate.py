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

num_of_rows = 10000

def main():
    mock_nhs_ae_dataset = {}
    mock_nhs_ae_dataset['Postcode'] = generate_postcodes()
    mock_nhs_ae_dataset['Hospital'] = generate_hospitals()
    (mock_nhs_ae_dataset['Arrival Date'], 
        mock_nhs_ae_dataset['Arrival Time']) = generate_arrival_dates_times()
    mock_nhs_ae_dataset['Time in A&E (mins)'] = generate_times_in_ae()
    mock_nhs_ae_dataset['Gender'] = generate_genders()
    mock_nhs_ae_dataset['Age'] = generates_ages()
    mock_nhs_ae_dataset['Treatment'] = generate_treatments()
    mock_nhs_ae_dataset['Ethnicity'] = generate_ethnicities()

    write_out_dataset(mock_nhs_ae_dataset, filepaths.mock_nhs_ae_dataset)


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


def generate_genders() -> list:
    # national codes for gender in NHS data
    # https://www.datadictionary.nhs.uk/data_dictionary/attributes/p/person/person_gender_code_de.asp?shownav=1
    gender_codes_df = pd.read_csv(filepaths.nhs_ae_gender_codes)
    genders = gender_codes_df['Gender'].tolist()
    weights =[0.005, 0.495, 0.495, 0.005]
    gender_codes = random.choices(genders, k=num_of_rows, weights=weights)
    return gender_codes


def generates_ages() -> list:
    # London population age groups populations. based on 2011 census
    # https://data.london.gov.uk/dataset/census-2011-population-age-uk-districts
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
    # treatment codes found here:
    # https://www.datadictionary.nhs.uk/web_site_content/supporting_information/clinical_coding/accident_and_emergency_treatment_tables.asp?shownav=1
    treatment_codes_df = pd.read_csv(filepaths.nhs_ae_treatment_codes)
    treatments = treatment_codes_df['Treatment'].tolist()
    treatment_codes = random.choices(treatments, k=num_of_rows)
    return treatment_codes


def generate_ethnicities() -> list:
    # based on the 2011 census
    # https://en.wikipedia.org/wiki/Demography_of_London#Ethnicity
    london_ethnicities_df = pd.read_csv(filepaths.london_ethnicities)
    ethnic_groups = london_ethnicities_df['Ethnic Group']
    percentages = london_ethnicities_df['Percentage'].tolist()
    ethnicities = random.choices(
        ethnic_groups, weights=percentages, k=num_of_rows)

    return ethnicities


def write_out_dataset(dataset, filepath):
    df = pd.DataFrame.from_dict(dataset)
    df.to_csv(filepath, index=False)


if __name__ == "__main__":
    main()
