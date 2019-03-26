import os
import sys
from pathlib import Path

this_filepath = Path(os.path.realpath(__file__))
project_root = str(this_filepath.parents[1])
data_dir = os.path.join(project_root, 'data/')

# add the DataSynthesizer repo to the pythonpath
data_synthesizer_dir = os.path.join(project_root, 'DataSynthesizer/')
sys.path.append(data_synthesizer_dir)

postcodes_london = os.path.join(data_dir, 'London postcodes.csv')
hospitals_london = os.path.join(data_dir, 'hospitals_london.txt')
nhs_ae_gender_codes = os.path.join(data_dir, 'nhs_ae_gender_codes.csv')
nhs_ae_treatment_codes = os.path.join(data_dir, 'nhs_ae_treatment_codes.csv')
age_population_london = os.path.join(data_dir, 'age_population_london.csv')

hospital_ae_data = os.path.join(data_dir, 'hospital_ae_data.csv')
hospital_ae_data_deidentify = os.path.join(data_dir, 'hospital_ae_data_deidentify.csv')

hospital_ae_data_synthetic_random = os.path.join(
    data_dir, 'hospital_ae_data_synthetic_random.csv')
# nhs_ae_data_synthetic_independent = os.path.join(data_dir, 'nhs_ae_data_synthetic_independent.csv')
# nhs_ae_data_synthetic_correlated = os.path.join(data_dir, 'nhs_ae_data_synthetic_correlated.csv')

hospital_ae_description_random = os.path.join(
    data_dir, 'hospital_ae_description_random.json')
# nhs_ae_description_independent = os.path.join(data_dir, 'nhs_ae_description_independent.json')
# nhs_ae_description_correlated = os.path.join(data_dir, 'nhs_ae_description_correlated.json')

