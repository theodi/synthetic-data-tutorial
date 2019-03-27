'''
This generates synthetic data from the hospital_ae_data_deidentify.csv
file. It generates three types of synthetic data and saves them in 
different files. 
'''

import random 
import os

import pandas as pd
import numpy as np

import filepaths
from DataDescriber import DataDescriber
from DataGenerator import DataGenerator
from ModelInspector import ModelInspector
from lib.utils import read_json_file


attribute_to_datatype = {
    'Attendance ID': 'String', 
    'Time in A&E (mins)': 'Integer', 
    'Treatment': 'String', 
    'Gender': 'String', 
    'Index of Multiple Deprivation Decile': 'Integer',
    'Hospital ID': 'String', 
    'Arrival Date': 'String', 
    'Arrival hour range': 'String',  
    'Age bracket': 'String'
}

attribute_is_categorical = {
    'Attendance ID': False, 
    'Time in A&E (mins)': False, 
    'Treatment': True, 
    'Gender': True, 
    'Index of Multiple Deprivation Decile': False,
    'Hospital ID': True, 
    'Arrival Date': True, 
    'Arrival hour range': True,  
    'Age bracket': True
}

attribute_to_is_candidate_key = {
    'Attendance ID': True
}


def main():
    # "_df" is the usual way people refer to a Pandas DataFrame object
    hospital_ae_df = pd.read_csv(filepaths.hospital_ae_data_deidentify)
    category_threshold = hospital_ae_df['Treatment'].nunique()

    # let's generate the same amount of rows (though we don't have to)
    num_rows = len(hospital_ae_df)

    # iterate through the 3 modes to generate synthetic data
    for mode in ['random', 'independent', 'correlated']: 
        print('generating synthetic data for', mode, 'mode...')
        description_filepath = describe_synthetic_data(
            mode, category_threshold)
        generate_synthetic_data(mode, num_rows, description_filepath)
        compare_synthetic_data(mode, hospital_ae_df, description_filepath)


    print('done.')


def describe_synthetic_data(
        mode: str, category_threshold: int) -> str:
    '''
    Describes the synthetic data and saves it to the data/ directory.

    Keyword arguments:
    mode -- what type of synthetic data
    category_threshold -- limit at which categories are considered blah
    num_rows -- number of rows in the synthetic dataset
    '''
    describer = DataDescriber(category_threshold=category_threshold)

    if mode == 'random':
        describer.describe_dataset_in_random_mode(
            filepaths.hospital_ae_data_deidentify,
            attribute_to_datatype=attribute_to_datatype,
            attribute_to_is_categorical=attribute_is_categorical)

        description_filepath = filepaths.hospital_ae_description_random
    
    elif mode == 'independent':
        describer.describe_dataset_in_independent_attribute_mode(
            filepaths.hospital_ae_data_deidentify,
            attribute_to_datatype=attribute_to_datatype,
            attribute_to_is_categorical=attribute_is_categorical)

        description_filepath = filepaths.hospital_ae_description_independent
    
    elif mode == 'correlated':
        # Increase epsilon value to reduce the injected noises. 
        # Set epsilon=0 to turn off differential privacy. We're not using 
        # differential privacy in this tutorial.
        epsilon = 0

        # The maximum number of parents in Bayesian network
        # i.e., the maximum number of incoming edges.
        degree_of_bayesian_network = 1

        describer.describe_dataset_in_correlated_attribute_mode(
            dataset_file=filepaths.hospital_ae_data_deidentify, 
            epsilon=epsilon, 
            k=degree_of_bayesian_network,
            attribute_to_datatype=attribute_to_datatype,
            attribute_to_is_categorical=attribute_is_categorical,
            attribute_to_is_candidate_key=attribute_to_is_candidate_key)

        description_filepath = filepaths.hospital_ae_description_correlated

    describer.save_dataset_description_to_file(description_filepath)

    return description_filepath


def generate_synthetic_data(
        mode: str, num_rows: int, description_filepath: str):
    '''
    Generates the synthetic data and saves it to the data/ directory.

    Keyword arguments:
    mode -- what type of synthetic data
    num_rows -- number of rows in the synthetic dataset
    description_filepath -- filepath to the data description
    '''
    generator = DataGenerator()

    if mode == 'random':
        generate_function = generator.generate_dataset_in_random_mode
        data_filepath = filepaths.hospital_ae_data_synthetic_random 
            
    elif mode == 'independent':
        generate_function = generator.generate_dataset_in_independent_mode
        data_filepath = filepaths.hospital_ae_data_synthetic_independent 
    
    elif mode == 'correlated':
        generate_function = generator.generate_dataset_in_correlated_attribute_mode
        data_filepath = filepaths.hospital_ae_data_synthetic_correlated

    generate_function(num_rows, description_filepath)    
    generator.save_synthetic_data(data_filepath)

 
    print('done.')


def compare_synthetic_data(mode, hospital_ae_df, description_filepath):
    if mode == 'random':
        synthetic_df_filepath = filepaths.hospital_ae_data_synthetic_random
    elif mode == 'independent':
        synthetic_df_filepath = filepaths.hospital_ae_data_synthetic_independent
    elif mode == 'correlated':
        synthetic_df_filepath = filepaths.hospital_ae_data_synthetic_correlated

    synthetic_df = pd.read_csv(synthetic_df_filepath)

    # Read attribute description from the dataset description file.
    attribute_description = read_json_file(
        description_filepath)['attribute_description']

    
    inspector = ModelInspector(
        hospital_ae_df, synthetic_df, attribute_description)

    for attribute in synthetic_df.columns:
        figure_filepath = os.path.join(
            filepaths.plots_dir, 
            mode + '_' + attribute + '.png'
        )
        inspector.compare_histograms(attribute, figure_filepath)



if __name__ == "__main__":
    main()
