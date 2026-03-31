# Introduction

## Movie analysis

This is a program performing an analysis on a database of movies from IMDb. Using this, you can see which movies are rated the best, which countries excel in cinematography and how many films they produce. 

Additionaly, you can specify your analysis with optional parameters. You can learn more about this in the section below.

## Datasets

Datasets are available [here](https://datasets.imdbws.com/) with [description](https://developer.imdb.com/non-commercial-datasets/) of their content and data.

Datasets used in this analysis are title.akas.tsv, title.basics.tsv and title.ratings.tsv

## Requirements

To run this analysis, you must install pandas package.

Please install all necessary dependencies before executing the analysis.

```
pip install -r requirements.txt
```

## Options and functions

There are options that may specify your analysis with a special parameters. There are required parameters, and optional parameters.

You must specify which type of media you want to analyze - movies, TV episodes, or short movies.
```
python3 script.py -type_of_media=
```

You can specify years from which you want to analyze movies - passing the start and end years of the analysis.
```
python3 script.py -start_year= -end_year=
```