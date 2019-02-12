# Synthetic Data Workshop

## Usage

Synthetic data workshop - looks at steps to create a synthetic dataset for NHS A&amp;E data

## Overview

- Generate mock NHS A&E data

## Pre-work

- Try out e-learning course!
- Check out the full UKAN 12 steps.

<!-- - Who will be using this data?
- How will we test if we have kept the utility of the dataset? Describe the test.
- Do a small data ecosystem map. -->

### Setup

First, make sure you have [Python3 installed](https://www.python.org/downloads/).

Download this repository either as a zip or using Git.

Change direcory in to the repo, install a virtualenv and install the dependent libaries.

```bash
cd /path/to/repo/synthetic_data_workshop/
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Generate mock NHS A&E dataset

Now let's create the actual data we'll use.

```bash
python workshop/generate.py
```

Voila! That's it. You'll now see a `mock_nhs_ae_dataset.csv` file in the `/data` directory. Open it up and have a browse.

---

## Anonymisation Steps

For this stage we're going to be loosely following [the anonymisation techniques used when creating NHS synthetic data for A&H in England](https://odileeds.org/blog/2019-01-24-exploring-methods-for-creating-synthetic-a-e-data).

### Where a patient lives
  
### Individual hospitals

### Time in the data

### Patient demographics

### Health care coding

---

## Synthesising

For each of three we'll run our tests we defined and observe the results. These are three modes available in Data Synthesizer toolkit.

### Identify variables with correlation

> In the end I have used a stepwise Pearson's correlation to identify the variables with the least relationship to any other variable in the extract.

Explain Bayesian Networks.

### Random mode - generate random values for this column

### Independent attribute mode - keep the patterns of each individual column

### Correlated attribute mode - include correlations between columns in the data

---

### Post-publication

- How are you going to monitor it
- Shoehorn in a bunch of UKAN steps 10 to 12 type questions
