import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'datasets'

def load_dataset_akas(filepath):
    data = []

    for chunk in pd.read_csv(filepath, chunksize=1000000, sep='\t', usecols=['titleId', 'title', 'region']):
        data.append(chunk)

    data = pd.concat(data, ignore_index=True)
    return data

def load_datasets():
    path_akas = 'datasets/title.akas.tsv'
    path_basics = 'datasets/title.basics.tsv'
    path_ratings = 'datasets/title.ratings.tsv'

    data_akas = load_dataset_akas(path_akas)
    data_basics = pd.read_csv(path_basics, sep='\t', usecols=['tconst', 'startYear', 'titleType'])
    data_ratings = pd.read_csv(path_ratings, sep='\t')

    print("Datasets loaded!\n")

    return data_akas, data_basics, data_ratings

def alt_into_region(data1):
    data = data1

    result = []
    current_title_id = None
    original_title = None
    regions = set()

    for row in data.itertuples(index=False):
        title_id = row.titleId
        title = row.title
        region = row.region

        if title_id != current_title_id:
            if current_title_id is not None:
                result.append([current_title_id, original_title, sorted(regions)])
            current_title_id = title_id
            original_title = title
            regions = set()
        if title == original_title and region != r'\N' and pd.notna(region):
            regions.add(str(region))
    if current_title_id is not None:
        result.append((current_title_id, original_title, sorted(regions)))
    data_region = pd.DataFrame(result, columns=['titleId', 'title', 'region'])

    return data_region

def concat_region_rating(type_of_media, data_basics, data_region, data_ratings, start_year, end_year):
    data_year = data_basics
    dataregion = data_region
    data_rating = data_ratings

    data_year["startYear"] = pd.to_numeric(data_year["startYear"], errors='coerce')

    if start_year is not None:
        if end_year is not None:
            data_year = data_year[data_year['startYear'].between(start_year, end_year)]
        else:
            data_year = data_year[data_year['startYear'] >= start_year]
    elif end_year is not None:
        data_year = data_year[data_year['startYear'] <= end_year]

    data_year.rename(columns={'startYear': 'year'}, inplace=True)

    if type_of_media!='':
        if type_of_media == 'M':
            data_year = data_year[data_year['titleType']=='movie']
        elif type_of_media == 'TV':
            data_year = data_year[data_year['titleType']=='tvSeries']
        elif type_of_media == 'S':
            data_year = data_year[data_year['titleType']=='short']


    data = pd.concat([data_year.set_index('tconst'), data_rating.set_index('tconst')], axis=1, join='inner')
    data = data.reset_index()
    data_final = pd.concat([dataregion.set_index('titleId'), data.set_index('tconst')], axis=1, join='inner')

    return data_final

def how_many_regions_all(data_final):
    data = data_final['region']
    data = data.apply(tuple)
    data = data.value_counts().rename_axis('region').to_frame('counts')

    return data

def how_many_regions_exploded(data_final):
    data = data_final['region']
    data = data.explode('region')
    data = data.value_counts().rename_axis('region').to_frame('counts')

    return data

def how_many_coprod_and_unk(how_many_regions_all, data_final):
    data = how_many_regions_all
    data = data.reset_index()

    all_films = len(data_final.index)

    unk = data.loc[data['region'] == (), 'counts']
    unk_sum = unk.sum()

    coprod = data.loc[data['region'].apply(len) > 1, 'counts']
    coprod_sum = coprod.sum()

    print("All films: " + str(all_films))
    print("Unknown production: " + str(unk_sum))
    print("Coproductions: " + str(coprod_sum))

    print("Percent of unknown: " + str(round(unk_sum / all_films * 100, 2)) + " %")
    print("Percent of coprodictions: " + str(round(coprod_sum / all_films * 100, 2)) + " %")
    print("\n")


def with_enough_votes(data_final, votes):
    data = data_final
    data = data.loc[data['numVotes']>votes]
    data = data.sort_values('averageRating', ascending=False)

    print("Top rated movies:")
    print(data[['title', 'region', 'year', 'averageRating']].head(10).to_markdown())
    print("\n")

    return data

def count_region_in_top(enough_votes):
    top_compare = {}
    ranking = [10,20,50,100,200]

    for i in ranking:
        data = enough_votes.head(i)
        top_mentioned = data['region'].explode().value_counts().index.tolist()
        top_compare[str(i)] = pd.Series(top_mentioned)

    top_compare = pd.DataFrame(top_compare)
    top_compare = top_compare.fillna("")

    print("Countries with most movies in top:")
    print(top_compare.head(30).to_markdown())

    return top_compare
