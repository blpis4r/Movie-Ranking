# Introduction

## Movie analysis

This is a program performing an analysis on a database of movies from IMDb. Using this, you can see which movies are rated the best, which countries excel in cinematography and how many films they produce. 

Additionally, you can specify your analysis with optional parameters. You can learn more about this in the section below.

## Datasets

Datasets are available [here](https://datasets.imdbws.com/) with [description](https://developer.imdb.com/non-commercial-datasets/) of their content and data.

## Requirements

To run this analysis, you must install pandas package.

Please install all necessary dependencies before executing the analysis.

```
pip install -r requirements.txt
```

## Options and functions

To run analysis, it is required to download all necessary datasets. Run:
```
python3 scripy.py download
```
It will download all necessary datasets which aren't already in your directory.

<br/><br/>

There are options that may specify your analysis with a special parameters. There are required parameters, and optional parameters.

You can specify which type of media you want to analyze - movies, TV series, or short movies.
```
python3 script.py analyze -type_of_media=
```

You also can specify years from which you want to analyze movies - passing the start and end years of the analysis.
```
python3 script.py analyze -start_year= -end_year=
```

To include only entities with enough votes, use:
```
python3 script.py analyze -votes=
```
If not specified, the base number 10,000 will be used.