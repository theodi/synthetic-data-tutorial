# Synthetic Data Workshop

## Usage

Synthetic data workshop - looks at steps to create a synthetic dataset for NHS A&amp;E data

## Overview

### 1. Look at the use cases - pre-work

- Who will be using this data?
- How will we test if we have kept the utility of the dataset? Describe the test.
- Do a small data ecosystem map.

---

### 2. Anonymisation Steps

For this stage we're going to be loosely following how the NHS itself used anonymisation techniques when creating their synthetic data.

#### Where a patient lives
  
#### Individual hospitals

#### Time in the data

#### Patient demographics

#### Health care coding

---

### 3. Synthesising

For each of three we'll run our tests we defined and observe the results. These are three modes available in Data Synthesizer toolkit.

#### Identify variables with correlation

> In the end I have used a stepwise Pearson's correlation to identify the variables with the least relationship to any other variable in the extract.

Explain Bayesian Networks.

#### Random mode - generate random values for this column

#### Independent attritute mode - keep the patterns of each individual column

#### Correlated attribute mode - include correlations between columns in the data


---

### 4. Post-publication

- How are you going to monitor it
- Shoehorn in a bunch of UKAN steps 10 to 12 type questions
