# Main Comments
Every script inside the folder **tableScripts**, with the exception of **common.py**, referes to a file in the database. These files save the output in a file inside the folder Data/local. This makes the script run faster after the first execution.

The file **common.py** has some functions that are frequently used.

The connection to the database is done using the file **Database.py** inside the folder **conn**






# CognitiveProfiling_ADNI
This repository will contain the code developed for profiling patients from Alzheimer's Disease Big Data DREAM Challenge #1. 


# Model Data:
The data used on this work was from Alzheimer's Disease Big Data DREAM Challenge #1. This data is present on the Alzheimers Disease Neuroimaging Initiative (ADNI).

This challenge aims to apply an open science approach to identify accurate predictive AD bio-markers rapidly. Later this bio-markers may help the scientific, industrial and regulatory communities to improve AD diagnosis and treatment. AD #1 will be the first in a series of AD Data Challenges. The goal is to leverage genetics and brain imaging combined with cognitive assessments, biomarkers and demographic information.  This information is from cohorts ranging from cognitively normal to individuals with AD.

To know more about this data or the challenge itself, head to this [link](https://www.synapse.org/#!Synapse:syn2290704/wiki/60828).

# Data Confirmation
Confirming data before proceeding is the best way to see if everything is there and if the selected file is the proper one. On this step, the goal is to see if the data loaded is the same as the challenge states. 

Here was found the first problem, the question one from the challenge states that the file to use is ADNI_Training_Q3_APOE then they state that this data has 767 individuals. However, this file only has 628 individuals.  The proper file seems to be ADNI_Training_Q1_APOE which does have the number of individuals stated. Everything in this file matches the table present on the [site](https://www.synapse.org/#!Synapse:syn2290704/wiki/64710).

The table representing the second question was empty. For this reason, there is no way to see if this data is right. However, there might be some way to check this in the future. 

The data for the third question also matches the table present on the [site](https://www.synapse.org/#!Synapse:syn2290704/wiki/64710).

# Data PreProcessing
Data preprocessing is a step that helps to build a model. This technique will transform raw data into an understandable format for the model. Data provided might have some issues like being incomplete, inconsistent, and lacking in certain behaviours or trends and may have some errors. 

The preprocessing task requires some libraries:
- NumPy
- Pandas


## Treating the Neuroassessment Data Files:
As stated before the first goal here is to convert data from each neuro-cognitive assessments into an understandable format for the programming language. In other words, the goal here is to convert text or objects into numeric values or boolean, depending on what we find. 

### MoCA - Montreal Cognitive Assessment
According to [this](https://www.mocatest.org/the-moca-test/) source:

The MoCA Test was validated in the setting of mild cognitive impairment (MCI), and has been subsequently adopted in numerous clinical settings. The sensivity of the MoCA for detecting MCI is 90%, compared to 18% for other leading cognitive screening tools such as the MMSE.

The dataset we have for this assessment has 52 columns with a total of 6895 rows. 

All fields were coming from the data base as an object, and they had to be converted. 

The conversion done is:
* Phase: This dataset has 4 phases:
    * ADNI1  -> 1
    * ADNI2  -> 2
    * ADNI3  -> 3
    * ADNIGO -> 4


ID       -> int

RID      -> int

SITEID   -> int

VISCODE  -> Column Removed the next field represents the same, but with translation

VISCODE2 -> int
 * bl    ->  0
 * m06   ->  6
 * m12   ->  12
 * m24   ->  24
 * m36   ->  36
 * m48   ->  48
 * m60   ->  60
 * m72   ->  72
 * m84   ->  84
 * m96   ->  96
 * m108  ->  108
 * m120  ->  120
 * m132  ->  132
 * m144  ->  144
 * m156  ->  156
 * m168  ->  168
 * m180  ->  180
 * blank ->  Row removed

USERDATE  -> Column removed 

USERDATE2 -> Column removed

update_stamp -> Column removed

The last column was "MOCA" and the blank fields were calculated and normalized from 0-30 to 0-100. 
 ```Python
    Normalization = total * 100 / 30 
 ```

The total was calculated applying some conditions: 
 * If the sum of all serial fields was higher than 3 it gives 3 points, between 1 and 4 it corresponds to 2 points and 1 correct corresponds to 1 point. 

 * The Del fields a 0 corresponds to 1 point and a 1 to 0 points.
 * field Letters corresponds to errors, less than 2 errors gives 1 point.
 * Ffluency grants a point when higher than 10.


Now the values for the test it self for each field blank values got their row removed the rest of the values were converted to int:

TRAILS, CUBE

The field LETTERS represents the number of errors on the given task.

### MMSE - Mini–Mental State Examination

According to [wikipedia](https://en.wikipedia.org/wiki/Mini%E2%80%93Mental_State_Examination)
MMSE is a 30-point test that is used extensively in clinical research settings to measure cognitive impairment. It is commonly used in medicine and allied health to screen for dementia. It is also used to estimate the severity and progression of cognitive impairment and to follow the course of cognitive changes in an individual over time; thus making it an effective way to document an individual's response to treatment. The MMSE's purpose has been not, on its own, to provide a diagnosis for any particular nosological entity.

The dataset for this assessment has 74 columns with a total of 12163 rows.

The common columns got the same value as the previous test:

* Phase - This dataset has 4 phases:
    * ADNI1  -> 1
    * ADNI2  -> 2
    * ADNI3  -> 3
    * ADNIGO -> 4


ID       -> int

RID      -> int

SITEID   -> int