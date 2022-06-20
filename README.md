# Automated Detection of Typed Links in Issue Trackers
[![DOI](https://zenodo.org/badge/462716832.svg)](https://zenodo.org/badge/latestdoi/462716832)

This repository contains the data, experiments, and analysis for the RE2022 submission "Automated Detection of Typed Links in Issue Trackers".
With this repository you should be able to replicate the experiments or use the model on your own datasets.

## Author Information

- Clara Marie Lüders, University of Hamburg
- Tim Pietz, University of Hamburg
- Walid Maalej, University of Hamburg

## Description of Artifact
There are three subfolders;
- data
- tld
- pics

### data
Contains the data we used for our analysis and machine learning models.
This folder contains the following subfolders; raw, processed, splits, results.
The folder also contains the scripts ``data_extract.py`` and ``data_access.py`` and a few intermittent results from some analysis (.csv files), f.e overviews for user numbers per repository and other properties are saved in ``repo_overview.csv`` and ``user_numbers.csv``.

We used the JIRA data from here: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5901956.svg)](https://doi.org/10.5281/zenodo.5901956).

The script ``data_extract.py`` uses ``data_access.py`` to access the MongoDB. ``data_extract.py`` goes through all the entries inside one collection and saves all issues and all links into ``raw``. It also contains a function to calculate the number of contributors (result already saved as .csv in the data folder). Please run the ``data_extract.py`` script in the data folder as thet path is set accordingly. The extract functions for the issues and links use `JiraRepos` as a database name, so if you have another name, change it accordingly.

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

## System Requirements
Due to the size of the Jira dataset, we recommend a system with at least 24 GB memory available.
If you want to use the replication package
- **with Docker,** you will need a x86 architecture environment with [Docker Compose](https://docs.docker.com/compose/install/) installed.
- **without Docker,** you will need to use a Linux system running on a x86 architecture with a working `conda` distribution like [Miniconda](https://docs.conda.io/en/latest/miniconda.html) and a [MongoDB](https://www.mongodb.com/try/download/community) server.
 
## Installation Instructions
### With Docker
1. Clone the repository
2. Start the docker services with
   ```bash
   docker compose up -d
   ```
   The compose first build a docker image for the replication package, installing a Jupyter Notebook server alongside all the neccessary Python dependencies.
   Additionally, it also spins up a MongoDB instance that automatically initializes with the Jira dataset from Montgomery et al. (<a href="https://doi.org/10.5281/zenodo.5901956"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.5901956.svg" alt="DOI"></a>).
3. Observe the MongoDB container with
   ```
   docker compose logs mongo -f
   ```
   and wait for the import to finish.
   The MongoDB instance will countinuously print out log messages relating to the import at least every 5 seconds.
   After the import has finished, it will print a `"Waiting for connections"` message and the frequency of log messages decreases significantly.
   Depending on your network connection, the import process might take 20-30 minutes.
3. View the Python image outputs with
   ```
   docker compose logs lynx -f
   ```
   and look for a message like
   ```
   Jupyter Notebook 6.4.12 is running at:
   http://79f633f1551b:8888/?token=[…]
    or http://127.0.0.1:8888/?token=[…]
   ```
4. Open the Jupyter Notebook instance using the link displayed in the logs.
5. Follow the steps in the "Steps to Reproduce" section below.
   In the steps where you need to run a Python script, you can use the terminal built into the Jupyter UI.
   The Jupyter notebook Docker container volume mounts you locally cloned repository.
   All of the outputs are thus saved in the repository directory of your machine.

### Without Docker
1. Download the Jira Dataset from Montgomery et al. (<a href="https://doi.org/10.5281/zenodo.5901956"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.5901956.svg" alt="DOI"></a>).
   Follow the instructions detailed in the `README.md` of step 3 on the site to import the data into your MongoDB server.
2. Setup the python environment specified in the `conda.yml` and activate it with
   ```
   conda env create -f conda.yml
   conda activate tld
   ```

## Steps to Reproduce
1. Run the ``data_extract.py`` script to extract issues and links into the `data/raw` directory.
   You can specify the MongoDB access details using CLI arguments
   ```
   python data/data_extract.py --host [host] --port [port] --username [username] --password [password]
   ```
   With the Docker Compose setup, use `--host mongo` and leave out the other arguments.
2. Preprocess the data with the jupyter notebook ``Preproccesing.ipynb``, this adds the processed data into data/processed
3. Run the experiments as detailed in the next README section "Running the experiments"
4. Run the jupyter notebook `BERT_results_correlations.ipynb` to see the results

### Running the experiments
To train a BERT-based typed link detection model, run the `tld.models.bert` module.
The module takes the training configuration as CLI parameters.
For example, the following command replicates the paper results for the `redhat` repository. 
```
python -m tld.models.bert \
  --model bert-base-uncased \
  --tracker redhat \
  --train-batch-size 48 \
  --eval-batch-size 128 \
  --n-epochs 30
```

To train one of the CNN-based models, run the `tld.models.cnn` module.
Select a model architecture with the `--model` CLI argument, using either `sccnn` or `dccnn`.
For example, the following command replicates our SCCNN results for the `redhat` repository.
```
python -m tld.models.cnn \
  --model sccnn \
  --tracker redhat
```

## Using your own data

Create an ``issue.csv`` containing all issues and a ``link.csv`` containing all links in your dataset.
The ``issue.csv`` should contain at least a column for the id, title, description, and resolution (needed to create random non-links). 
The ``link.csv`` should contain a column for issue_id_1, issue_id_2, linktype, and name (we used issue_id_1+issue_id_2+linktype, but in general a unique identifier for a link).
These are the neseccary columns to run the deep learning models.
Some analysis, f.e. ``Repository_Properties.ipynb`` contains analysis regarding the (sub-)projects and issue belongs to, so these will not run correctly if there is no ``projectid`` column.
If your data contains link types that are not in the JIRA dataset, you might need to provide a new entry into the dictionary found in ``tld/linktypes.py``
