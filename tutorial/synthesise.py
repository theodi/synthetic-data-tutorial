'''
This generates synthetic data from the hospital_ae_data_deidentify.csv
file. It generates three types of synthetic data and saves them in 
different files. 
'''

import random 
import os
import time

import pandas as pd
import numpy as np

import filepaths
from DataDescriber import DataDescriber
from DataGenerator import DataGenerator
from ModelInspector import ModelInspector
from lib.utils import read_json_file


attribute_to_datatype = {
    # 'Attendance ID': 'String', 
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
    # 'Attendance ID': False, 
    'Time in A&E (mins)': False, 
    'Treatment': True, 
    'Gender': True, 
    'Index of Multiple Deprivation Decile': True,
    'Hospital ID': True, 
    'Arrival Date': True, 
    'Arrival hour range': True,  
    'Age bracket': True
}

mode_filepaths = {
    'random': {
        'description': filepaths.hospital_ae_description_random, 
        'data': filepaths.hospital_ae_data_synthetic_random
    },
    'independent': {
        'description': filepaths.hospital_ae_description_independent, 
        'data': filepaths.hospital_ae_data_synthetic_independent
    },
    'correlated': {
        'description': filepaths.hospital_ae_description_correlated, 
        'data': filepaths.hospital_ae_data_synthetic_correlated
    }
}


def main():
    start = time.time()

    # "_df" is the usual way people refer to a Pandas DataFrame object
    hospital_ae_df = pd.read_csv(filepaths.hospital_ae_data_deidentify)
    category_threshold = hospital_ae_df['Treatment'].nunique()

    # let's generate the same amount of rows as original data (though we don't have to)
    num_rows = len(hospital_ae_df)

    # iterate through the 3 modes to generate synthetic data
    for mode in ['random','independent', 'correlated']: 

        print('describing synthetic data for', mode, 'mode...')
        describe_synthetic_data(
                mode, 
                category_threshold, 
                mode_filepaths[mode]['description']
        )

        print('generating synthetic data for', mode, 'mode...')
        generate_synthetic_data(
            mode, 
            num_rows, 
            mode_filepaths[mode]['description'],
            mode_filepaths[mode]['data']
        )

        print('comparing histograms for', mode, 'mode...')
        compare_histograms(
            mode, 
            hospital_ae_df, 
            mode_filepaths[mode]['description'],
            mode_filepaths[mode]['data']
        )

        print('comparing pairwise mutual information for', mode, 'mode...')
        compare_pairwise_mutual_information(
            mode, 
            hospital_ae_df, 
            mode_filepaths[mode]['description'],
            mode_filepaths[mode]['data']
        )

    elapsed = round(time.time() - start, 2)
    print('done in ' + str(elapsed) + ' seconds.')


def describe_synthetic_data(
        mode: str, category_threshold: int, description_filepath:str):
    '''
    Describes the synthetic data and saves it to the data/ directory.

    Keyword arguments:
    mode -- what type of synthetic data
    category_threshold -- limit at which categories are considered blah
    description_filepath -- filepath to the data description
    '''
    describer = DataDescriber(category_threshold=category_threshold)

    if mode == 'random':
        describer.describe_dataset_in_random_mode(
            filepaths.hospital_ae_data_deidentify,
            attribute_to_datatype=attribute_to_datatype,
            attribute_to_is_categorical=attribute_is_categorical)
    
    elif mode == 'independent':
        describer.describe_dataset_in_independent_attribute_mode(
            filepaths.hospital_ae_data_deidentify,
            attribute_to_datatype=attribute_to_datatype,
            attribute_to_is_categorical=attribute_is_categorical)
    
    elif mode == 'correlated':
        # Increase epsilon value to reduce the injected noises. 
        # We're not using differential privacy in this tutorial, 
        # so we'll set epsilon=0 to turn off differential privacy 
        epsilon = 0

        # The maximum number of parents in Bayesian network
        # i.e., the maximum number of incoming edges.
        degree_of_bayesian_network = 1

        describer.describe_dataset_in_correlated_attribute_mode(
            dataset_file=filepaths.hospital_ae_data_deidentify, 
            epsilon=epsilon, 
            k=degree_of_bayesian_network,
            attribute_to_datatype=attribute_to_datatype,
            attribute_to_is_categorical=attribute_is_categorical)
            # attribute_to_is_candidate_key=attribute_to_is_candidate_key)

    describer.save_dataset_description_to_file(description_filepath)


def generate_synthetic_data(
        mode: str, 
        num_rows: int, 
        description_filepath: str,
        synthetic_data_filepath: str
    ):
    '''
    Generates the synthetic data and saves it to the data/ directory.

    Keyword arguments:
    mode -- what type of synthetic data
    num_rows -- number of rows in the synthetic dataset
    description_filepath -- filepath to the data description
    synthetic_data_filepath -- filepath to where synthetic data written
    '''
    generator = DataGenerator()

    if mode == 'random':
        generator.generate_dataset_in_random_mode(num_rows, description_filepath)
            
    elif mode == 'independent':
        generator.generate_dataset_in_independent_mode(num_rows, description_filepath)
    
    elif mode == 'correlated':
        generator.generate_dataset_in_correlated_attribute_mode(num_rows, description_filepath)

    generator.save_synthetic_data(synthetic_data_filepath)


def compare_histograms(
        mode: str, 
        hospital_ae_df: pd.DataFrame, 
        description_filepath: str,
        synthetic_data_filepath: str
    ):
    '''
    Makes comapirson plots showing the histograms for each column in the 
    synthetic data.

    Keyword arguments:
    mode -- what type of synthetic data
    hospital_ae_df -- DataFrame of the original dataset
    description_filepath -- filepath to the data description
    synthetic_data_filepath -- filepath to where synthetic data written
    '''

    synthetic_df = pd.read_csv(synthetic_data_filepath)

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
        # need to replace whitespace in filepath for Markdown reference
        figure_filepath = figure_filepath.replace(' ', '_')
        inspector.compare_histograms(attribute, figure_filepath)

def compare_pairwise_mutual_information(
        mode: str, 
        hospital_ae_df: pd.DataFrame, 
        description_filepath: str,
        synthetic_data_filepath: str
    ):
    '''
    Looks at correlation of attributes by producing heatmap

    Keyword arguments:
    mode -- what type of synthetic data
    hospital_ae_df -- DataFrame of the original dataset
    description_filepath -- filepath to the data description
    synthetic_data_filepath -- filepath to where synthetic data written
    '''

    synthetic_df = pd.read_csv(synthetic_data_filepath)

    attribute_description = read_json_file(
        description_filepath)['attribute_description']

    inspector = ModelInspector(
        hospital_ae_df, synthetic_df, attribute_description)

    figure_filepath = os.path.join(
        filepaths.plots_dir, 
        'mutual_information_heatmap_' + mode + '.png'
    )

    inspector.mutual_information_heatmap(figure_filepath)


if __name__ == "__main__":
    main()
