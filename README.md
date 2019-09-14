kindful_donations
==============================

Hackathon!!!!!

Getting started
===============
Install [pipenv](https://pipenv-fork.readthedocs.io/en/latest/).
Run the following: 
```bash
pipenv shell
pipenv install
```

This _should_ get you set up to run notebooks / scripts / etc

Getting datasets
===============
See kindful! Once you have a donations.csv, stick it in `./data/raw/donations.csv`

Creating data for shiny app
==========================
This will look at the donations csv, and create 2 new files that are used within the shiny app.
```bash
pipenv shell
pipenv install
pipenv run python src/data/make_shiny_datasets.py ./data/raw/donations.csv ./data/processed
```

Project Organization
------------

    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to download or generate data
        │   └── make_dataset.py
        │
        ├── features       <- Scripts to turn raw data into features for modeling
        │   └── build_features.py
        │
        ├── models         <- Scripts to train models and then use trained models to make
        │   │                 predictions
        │   ├── predict_model.py
        │   └── train_model.py
        │
        └── visualization  <- Scripts to create exploratory and results oriented visualizations
            └── visualize.py
    


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

# Google slides presentation
https://docs.google.com/presentation/d/1hfpPCfysCK6GJEdZxV_aKqHdN0UXXxvzDncbPw8VGaA/edit#slide=id.g600c6b4d58_2_4
