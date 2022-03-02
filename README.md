# Automated Detection of Typed Links in Issue Trackers

This repository contains the data, experiments, and analysis for the RE2022 submission "Automated Detection of Typed Links in Issue Trackers".

Upon acceptance this repository and its data will be made fully public on Zenodo and GitHub.

## Structure of the Repository
There are three subfolders;
- data
- tld
- pics

### data
Contains the data we used for our analysis and machine learning models.
This folder contains the following subfolders; raw, processed, splits, results.

The script used to extract the data are also in this subfolder, ``data_extract.py`` and ``data_access.py``
Overviews for user numbers per repository and other properties are saved in ``repo_overview.csv`` and ``user_numbers.csv``

### tld
Contains the python scrips to run all models, they will save their data into the results folder

### pics
Contains the figures contained in the packages and further figures that were not included in the paper.

### Jupyter Notebooks

#### BERT_results_correlations
Extracts the results on the test data from the results folder and calculates the precision, recall, and F1-score per repository.
It also calculates the correlations of the macro F1-scores to properties of the repositories and link types.

#### Create_Word_Models
Creates word2vec and fasttext models and embedding vectors for SCCNN and DCCNN experiments, these are saved under data.

#### DetailedTestdata_Top3Prediction
Connects the results on the test data to their input texts, contains an analyze to the text length and the results of the optimization strategy "Top3 Prediction" which predicts the top 3 possible labels based on the logits, can be adapted to top k prediciton.

#### Preprocessing
Preprocesses the raw data extracted with ``data_extract.py``. Cleans issues and links. Issues are removed when they have no title and links are checked for duplicates etc., the script also adds 'non-links'.

#### Linktype_Properties
Calculates the cosine similarity of the issue texts of linked issues, as well as their lengths and the absolute difference.
Saves the result as a .csv in data for further analysis.

#### Random_Majority_results
Calculates the F1-score and accuracy of the random and majority baseline.

#### Repository_Properties
Calculates the numbers of Table 1 and 2, then saves Table 1 as .csv for further analysis.

#### SCCNN_DCCNN_results
Calculates the F1-score of the SCCNN and DCCNN architectures.
 

# Steps for Replication
1. Download the extraced data from Montgomery et al.
2. Install the python packages on your machine or in a virtual environments
3. Run the ``data_extract.py`` script to extract issues and links to data/raw
4. Preprocess the data with the jupyter notebook, this adds the processed data into data/processed
5. Run the experiments
6. Run the jupyter notebooks BERT_results_correlations.ipynb to see results

