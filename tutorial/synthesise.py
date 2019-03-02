'''
Answers for all the sections of the tutorial
'''
import random 

import pandas as pd
import numpy as np

import filepaths
from DataDescriber import DataDescriber
from DataGenerator import DataGenerator


def main():
    nhs_ae_df = load_nhs_ae_anomymous_data()

    generate_random_synthetic_data(nhs_ae_df)
    print('done.')

def load_nhs_ae_anomymous_data():
    nhs_ae_df = pd.read_csv(filepaths.nhs_ae_anonymous)
    return nhs_ae_df


def generate_random_synthetic_data(nhs_ae_df):
    threshold_value = len(nhs_ae_df['Treatment'].unique().tolist())
    num_tuples_to_generate = len(nhs_ae_df)

    describer = DataDescriber(category_threshold=threshold_value)
    describer.describe_dataset_in_random_mode(filepaths.nhs_ae_anonymous)
    describer.save_dataset_description_to_file(filepaths.nhs_ae_description)

    generator = DataGenerator()
    generator.generate_dataset_in_random_mode(
        num_tuples_to_generate, filepaths.nhs_ae_description)
    generator.save_synthetic_data(filepaths.nhs_ae_synthetic)

if __name__ == "__main__":
    main()
