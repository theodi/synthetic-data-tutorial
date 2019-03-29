'''
Takes the Hospitals A&E data generated from generate.py and runs it through a
set of de-identification steps. It then saves this as a new dataset.
'''
import random 
import time
import string

import pandas as pd
import numpy as np

import filepaths


def main():
    print('running de-identification steps...')
    start = time.time()

    # "_df" is the usual way people refer to a Pandas DataFrame object
    hospital_ae_df = pd.read_csv(filepaths.hospital_ae_data)

    print('removing Health Service ID numbers...')
    hospital_ae_df = remove_health_service_numbers(hospital_ae_df)

    print('converting postcodes to LSOA...')
    hospital_ae_df = convert_postcodes_to_lsoa(hospital_ae_df)

    print('converting LSOA to IMD decile...')
    hospital_ae_df = convert_lsoa_to_imd_decile(hospital_ae_df)

    print('replacing Hospital with random number...')
    hospital_ae_df = replace_hospital_with_random_number(hospital_ae_df)

    print('putting Arrival Hour in 4-hour bins...')
    hospital_ae_df = put_time_in_4_hour_bins(hospital_ae_df)

    print('removing non-male-or-female from gender ...')
    hospital_ae_df = remove_non_male_or_female(hospital_ae_df)

    print('putting ages in age brackets...')
    hospital_ae_df = add_age_brackets(hospital_ae_df)

    hospital_ae_df.to_csv(filepaths.hospital_ae_data_deidentify, index=False)

    elapsed = round(time.time() - start, 2)
    print('done in ' + str(elapsed) + ' seconds.')


def remove_health_service_numbers(hospital_ae_df: pd.DataFrame) -> pd.DataFrame:
    """Drops the Health Service ID numbers column from the dataset

    Keyword arguments:
    hospital_ae_df -- Hopsitals A&E records dataframe
    """
    hospital_ae_df = hospital_ae_df.drop('Health Service ID', 1)
    return hospital_ae_df


def convert_postcodes_to_lsoa(hospital_ae_df: pd.DataFrame) -> pd.DataFrame:
    """Adds corresponding Lower layer super output area for each row
    depending on their postcode. Uses London postcodes dataset from
    https://www.doogal.co.uk/PostcodeDownloads.php 

    Keyword arguments:
    hospital_ae_df -- Hopsitals A&E records dataframe
    """
    postcodes_df = pd.read_csv(filepaths.postcodes_london)
    hospital_ae_df = pd.merge(
        hospital_ae_df, 
        postcodes_df[['Postcode', 'Lower layer super output area']], 
        on='Postcode'
    )
    hospital_ae_df = hospital_ae_df.drop('Postcode', 1)
    return hospital_ae_df


def convert_lsoa_to_imd_decile(hospital_ae_df: pd.DataFrame) -> pd.DataFrame:
    """Maps each row's Lower layer super output area to which 
    Index of Multiple Deprivation decile it's in. It calculates the decile 
    rates based on the IMD's over all of London. 
    Uses "London postcodes.csv" dataset from
    https://www.doogal.co.uk/PostcodeDownloads.php 

    Keyword arguments:
    hospital_ae_df -- Hospitals A&E records dataframe
    """

    postcodes_df = pd.read_csv(filepaths.postcodes_london)

    hospital_ae_df = pd.merge(
        hospital_ae_df, 
        postcodes_df[
            ['Lower layer super output area', 
             'Index of Multiple Deprivation']
        ].drop_duplicates(), 
        on='Lower layer super output area'
    )
    _, bins = pd.qcut(
        postcodes_df['Index of Multiple Deprivation'], 10, 
        retbins=True, labels=False
    )
    hospital_ae_df['Index of Multiple Deprivation Decile'] = pd.cut(
        hospital_ae_df['Index of Multiple Deprivation'], bins=bins, 
        labels=False, include_lowest=True) + 1

    hospital_ae_df = hospital_ae_df.drop('Index of Multiple Deprivation', 1)
    hospital_ae_df = hospital_ae_df.drop('Lower layer super output area', 1)

    return hospital_ae_df


def replace_hospital_with_random_number(
        hospital_ae_df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Gives each hospital a random integer number and adds a new column
    with these numbers. Drops the hospital name column. 

    Keyword arguments:
    hospital_ae_df -- Hopsitals A&E records dataframe
    """

    hospitals = hospital_ae_df['Hospital'].unique().tolist()
    random.shuffle(hospitals)
    hospitals_map = {
        hospital : ''.join(random.choices(string.digits, k=6))
        for hospital in hospitals
    }
    hospital_ae_df['Hospital ID'] = hospital_ae_df['Hospital'].map(hospitals_map)
    hospital_ae_df = hospital_ae_df.drop('Hospital', 1)

    return hospital_ae_df


def put_time_in_4_hour_bins(hospital_ae_df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Gives each hospital a random integer number and adds a new column
    with these numbers. Drops the hospital name column. 

    Keyword arguments:
    hospital_ae_df -- Hopsitals A&E records dataframe
    """

    arrival_times = pd.to_datetime(hospital_ae_df['Arrival Time'])
    hospital_ae_df['Arrival Date'] = arrival_times.dt.strftime('%Y-%m-%d')
    hospital_ae_df['Arrival Hour'] = arrival_times.dt.hour

    hospital_ae_df['Arrival hour range'] = pd.cut(
        hospital_ae_df['Arrival Hour'], 
        bins=[0, 4, 8, 12, 16, 20, 24], 
        labels=['00-03', '04-07', '08-11', '12-15', '16-19', '20-23'], 
        include_lowest=True
    )
    hospital_ae_df = hospital_ae_df.drop('Arrival Time', 1)
    hospital_ae_df = hospital_ae_df.drop('Arrival Hour', 1)

    return hospital_ae_df


def remove_non_male_or_female(hospital_ae_df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Removes any record which has a non-male-or-female entry for gender. 

    Keyword arguments:
    hospital_ae_df -- Hopsitals A&E records dataframe
    """

    hospital_ae_df = hospital_ae_df[hospital_ae_df['Gender'].isin(['Male', 'Female'])]
    return hospital_ae_df


def add_age_brackets(hospital_ae_df: pd.DataFrame) -> pd.DataFrame:
    """
    Put the integer ages in to age brackets 

    Keyword arguments:
    hospital_ae_df -- Hopsitals A&E records dataframe
    """

    hospital_ae_df['Age bracket'] = pd.cut(
        hospital_ae_df['Age'], 
        bins=[0, 18, 25, 45, 65, 85, 150], 
        labels=['0-17', '18-24', '25-44', '45-64', '65-84', '85-'], 
        include_lowest=True
    )
    hospital_ae_df = hospital_ae_df.drop('Age', 1)
    return hospital_ae_df


if __name__ == "__main__":
    main()
