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
This folder contains three subfolders; raw, processed, and splits.

The script used to extract the data are also in this subfolder, ``data_extract.py`` and ``data_access.py``

### tld
Contains the python scrips to run all models, they will save their data into the results folder

### pics
Contains the figures contained in the packages and further figures that were not included in the paper.
 


# Python Packages
Python Version: Python 3.8.10

- gensim                   4.0.1                      
- Keras                    2.4.3              
- keras-nightly            2.5.0.dev2021032900
- Keras-Preprocessing      1.1.2                     
- matplotlib               3.4.2                        
- networkx                 2.6.2              
- nltk                     3.6.2              
- numpy                    1.19.5                      
- pandas                   1.2.4                         
- pymongo                  3.11.4                   
- regex                    2021.4.4                
- scikit-learn             0.24.2             
- scipy                    1.6.3              
- seaborn                  0.11.1                       
- sklearn                  0.0                      
- spacy                    3.0.6              
- spacy-legacy             3.0.5                   
- stanza                   1.2                
- tensorboard              2.5.0              
- tensorboard-data-server  0.6.1              
- tensorboard-plugin-wit   1.8.0              
- tensorflow               2.5.0              
- tensorflow-addons        0.13.0             
- tqdm                     4.60.0             

# Steps for Replication
1. Download the extraced data from Montgomery et al.
2. Install the python packages on your machine or in a virtual environments
3. Run the ``data_extract.py`` script.

