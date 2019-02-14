import os
from pathlib import Path

this_filepath = Path(os.path.realpath(__file__))
project_root = str(this_filepath.parents[1])
data_dir = os.path.join(project_root, 'data/')

postcodes_london = os.path.join(data_dir, 'postcodes_london.csv')
nhs_hospitals_london = os.path.join(data_dir, 'nhs_hospitals_london.txt')
nhs_ae_treatment_codes = os.path.join(data_dir, 'nhs_ae_treatment_codes.csv')
nhs_ae_gender_codes = os.path.join(data_dir, 'nhs_ae_gender_codes.csv')
london_ethnicities = os.path.join(data_dir, 'london_ethnicities.csv')
mock_nhs_ae_dataset = os.path.join(data_dir, 'mock_nhs_ae.csv')
age_population_london = os.path.join(data_dir, 'age_population_london.csv')
