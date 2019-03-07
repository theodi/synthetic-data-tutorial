# Synthetic Data for Anonymisation Tutorial

## Some questions

**What is this?**

A hands-on tutorial to show how to create synthetic data using some Python libraries.

**Wait, what is this "synthetic data" you speak of?**

It's data's that is created by an automated process which contains many of the statistical patterns of an original dataset. If you do this well enough, you can release the synthetic data knowing that you've kept a lot of the useful information in the dataset while removing most, if not all, of the personal information.

**Who is this tutorial for?**

For any person who programs who wants to learn about data anonymisation in general or more specifically about synthetic data.

**What is it not for?**
Non-programmers. Although I think this tutorial is still worth a browse to get some of the main ideas in what goes in to anonymising a dataset. However, if you're looking for info on how to create synthetic data using the latest and greatest deep learning techniques, this is not the tutorial for you.

**Who are you?**

We're the Open Data Institute. We work with companies and governments to build an open, trustworthy data ecosystem. Anonymisation and synthetic data are some of the many, many ways we can responsbily increase access to data. If you want to learn more, [check out our site](http://theodi.org).

**Why did you make this?**

We have an [R&D programme](https://theodi.org/project/data-innovation-for-uk-research-and-development/) that looks in to how to support innovation, improve data infrastructure and encourage ethical data sharing. One of the projects within this is about [managing the risks of re-identification](https://theodi.org/project/rd-broaden-access-to-personal-data-while-protecting-privacy-and-creating-a-fair-market/) in shared and open data. As you can see in the "Key outputs" section, we have other material from the project, but we thought it'd be good to have something specifically aimed specifically at programming people interested in anonymisation and want to get stuck in and learn by doing.

**Speaking of which, can I just get to the tutorial now?**

Sure! Let's go.

## Overview

This tutorial is inspired by the [NHS England with ODI Leeds' research](https://odileeds.org/events/synae/) in to creating a synthetic dataset from their hospitals accident and emergency admissions. Please do read about their project, as it's really interesting and great for learning about the trade-offs in creating synthetic data.

Just to be clear, we're not using their exact data, but create our own simplified version of it.

In this tutorial you will:

1. Create an A&E dataset which will contain personal information.
2. Run some anonymisation steps over this dataset to generate a new dataset.
3. Take this pseudoanonymous dataset and generate multiple synthetic datasets from it.

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
python tutorial/generate.py
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

### References

- [A comparative study of synthetic dataset generation techniques](https://dl.comp.nus.edu.sg/bitstream/handle/1900.100/7050/TRA6-18.pdf?sequence=1&isAllowed=y) - Ashish Dandekar, Remmy A. M. Zen, Stéphane Bressan
- [Exploring methods for synthetic A&E data](https://odileeds.org/blog/2019-01-24-exploring-methods-for-creating-synthetic-a-e-data) - Jonathan Pearson, NHS with Open Data Institute Leeds.
- [DataSynthesizer Github Repository](https://github.com/DataResponsibly/DataSynthesizer)
- [DataSynthesizer: Privacy-Preserving Synthetic Datasets](https://faculty.washington.edu/billhowe/publications/pdfs/ping17datasynthesizer.pdf) Haoyue Ping, Julia Stoyanovich, Bill Howe. 2017.
