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

    breakpoint()
    print('done.')


def load_nhs_london_ae_data():
    nhs_london_ae_df = pd.read_csv(filepaths.mock_nhs_ae_dataset)
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
            ['Lower layer super output area', 'Index of Multiple Deprivation']
        ].drop_duplicates(), 
        on='Lower layer super output area'
    )
    _, bins = pd.qcut(
        postcodes_df['Index of Multiple Deprivation'], 10, retbins=True, labels=False
    )
    nhs_df['Index of Multiple Deprivation Decile'] = pd.cut(
        nhs_df['Index of Multiple Deprivation'], bins=bins, labels=False, include_lowest=True) + 1

    nhs_df = nhs_df.drop('Index of Multiple Deprivation', 1)

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
    nhs_df['Arrival Hour Range'] = arrival_times.dt.strftime('%H')

    hours_map = {
        '00': '00-03', '01': '00-03', '02': '00-03', '03': '00-03', '04': '04-07', 
        '05': '04-07', '06': '04-07', '07': '04-07', '08': '08-11', '09': '08-11', 
        '10': '08-11', '11': '08-11', '12': '12-15', '13': '12-15', '14': '12-15', 
        '15': '12-15', '16': '16-19', '17': '16-19', '18': '16-19', '19': '16-19', 
        '20': '20-23', '21': '20-23', '22': '20-23', '23': '20-23'
    }

    nhs_df['Arrival Hour Range'] = nhs_df['Arrival Hour Range'].map(hours_map)
    nhs_df = nhs_df.drop('Arrival Time', 1)
    return nhs_df


if __name__ == "__main__":
    main()
