# CognitiveProfiling_ADNI
This repository will contain the code developed for profiling patients from Alzheimer's Disease Big Data DREAM Challenge #1. 


# Model Data:
The data used on this work was from Alzheimer's Disease Big Data DREAM Challenge #1. This data is present on the Alzheimers Disease Neuroimaging Initiative (ADNI).

This challenge aims to apply an open science approach to identify accurate predictive AD bio-markers rapidly. Later this bio-markers may help the scientific, industrial and regulatory communities to improve AD diagnosis and treatment. AD #1 will be the first in a series of AD Data Challenges. The goal is to leverage genetics and brain imaging combined with cognitive assessments, biomarkers and demographic information.  This information is from cohorts ranging from cognitively normal to individuals with AD.

To know more about this data or the challenge itself, head to this [link](https://www.synapse.org/#!Synapse:syn2290704/wiki/60828).

# Data Confirmation
Confirming data before proceeding is the best way to see if everything is there and if the selected file is the proper one. On this step, the goal is to see if the data loaded is the same as the challenge states. 

Here I found the first problem, the question one from the challenge states that the file to use is **ADNI_Training_Q3_APOE** then they state that this data has 767 individuals. However, this file only has 628 individuals. I believe this is an error. The proper file is **ADNI_Training_Q1_APOE** which does have the number of individuals stated. Everything seems to be according to the table presented on their [site](https://www.synapse.org/#!Synapse:syn2290704/wiki/64710).

# Data PreProcessing
Data preprocessing is a step that helps to build a model. This technique will transform raw data into an understandable format for the model. Data provided might have some issues like being incomplete, inconsistent, and lacking in certain behaviours or trends and may have some errors. 

The preprocessing task requires some libraries:
- NumPy
- Pandas


Starting from the file **ADNI_Training_Q1_APOE_July22.2014** 



