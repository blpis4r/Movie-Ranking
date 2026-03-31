from operations.operations import *

def run_analysis(type_of_media=None, n=10000, start_year=None, end_year=None):
    data_akas, data_basics, data_ratings = load_datasets()

    data_region = alt_into_region(data_akas)

    data_final = concat_region_rating(type_of_media, data_basics, data_region, data_ratings, start_year, end_year)

    regions_all = how_many_regions_all(data_final)

    regions_exploded = how_many_regions_exploded(data_final)

    how_many_coprod_and_unk(regions_all, data_final)

    enough_votes = with_enough_votes(data_final, n)

    top_compare = count_region_in_top(enough_votes)