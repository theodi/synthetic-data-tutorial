'''
Answers for all the sections of the tutorial
'''
import random 

import pandas as pd
import numpy as np

import filepaths


def main():
    nhs_london_ae_df = load_nhs_london_ae_data()
    nhs_london_ae_df = convert_postcodes_to_lsoa(nhs_london_ae_df)
    nhs_london_ae_df = convert_lsoa_to_imd_decile(nhs_london_ae_df)
    nhs_london_ae_df = replace_hospital_with_random_number(nhs_london_ae_df)
    nhs_london_ae_df = sample_data(nhs_london_ae_df, frac=0.8)
    nhs_london_ae_df = put_time_in_4_hour_bins(nhs_london_ae_df)
    nhs_london_ae_df = remove_non_male_or_female(nhs_london_ae_df)
    nhs_london_ae_df = add_age_brackets(nhs_london_ae_df)

    nhs_london_ae_df.to_csv(filepaths.nhs_ae_anonymous, index=False)

    print('done.')


def load_nhs_london_ae_data():
    nhs_london_ae_df = pd.read_csv(filepaths.nhs_ae_mock)
    return nhs_london_ae_df


def convert_postcodes_to_lsoa(nhs_df) -> pd.DataFrame:
    postcodes_df = pd.read_csv(filepaths.postcodes_london)
    nhs_df = pd.merge(
        nhs_df, 
        postcodes_df[['Postcode', 'Lower layer super output area']], 
        on='Postcode'
    )
    # remove postcode
    nhs_df = nhs_df.drop('Postcode', 1)
    return nhs_df


def convert_lsoa_to_imd_decile(nhs_df) -> pd.DataFrame:
    postcodes_df = pd.read_csv(filepaths.postcodes_london)

    nhs_df = pd.merge(
        nhs_df, 
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
    nhs_df['Index of Multiple Deprivation Decile'] = pd.cut(
        nhs_df['Index of Multiple Deprivation'], bins=bins, 
        labels=False, include_lowest=True) + 1

    nhs_df = nhs_df.drop('Index of Multiple Deprivation', 1)
    nhs_df = nhs_df.drop('Lower layer super output area', 1)

    return nhs_df


def replace_hospital_with_random_number(nhs_df):
    hospitals = list(set(nhs_df['Hospital'].tolist()))
    random.shuffle(hospitals)
    hospital_ids = range(1, len(hospitals)+1)
    hospitals_map = {
        hospital : hospital_id
        for hospital, hospital_id in zip(hospitals, hospital_ids)
    }
    nhs_df['Hospital'] = nhs_df['Hospital'].map(hospitals_map)
    return nhs_df


def sample_data(nhs_df, frac=0.5):
    return nhs_df.sample(frac=frac)
    

def put_time_in_4_hour_bins(nhs_df):
    arrival_times = pd.to_datetime(nhs_df['Arrival Time'])        
    nhs_df['Arrival Date'] = arrival_times.dt.strftime('%Y-%m-%d')
    nhs_df['Arrival Hour'] = arrival_times.dt.hour

    nhs_df['Arrival hour range'] = pd.cut(
        nhs_df['Arrival Hour'], 
        bins=[0, 4, 8, 12, 16, 20, 24], 
        labels=['00-03', '04-07', '08-11', '12-15', '16-19', '20-23'], 
        include_lowest=True
    )
    nhs_df = nhs_df.drop('Arrival Time', 1)
    return nhs_df


def remove_non_male_or_female(nhs_df):
    nhs_df = nhs_df[nhs_df['Gender'].isin(['Male', 'Female'])]
    return nhs_df


def add_age_brackets(nhs_df):
    nhs_df['Age bracket'] = pd.cut(
        nhs_df['Age'], 
        bins=[0, 18, 25, 45, 65, 85, 150], 
        labels=['0-17', '18-24', '25-44', '45-64', '65-84', '85-'], 
        include_lowest=True
    )
    nhs_df = nhs_df.drop('Age', 1)
    return nhs_df


if __name__ == "__main__":
    main()
