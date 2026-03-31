import argparse
from analysing import run_analysis

def movie_type(typed):
    choices=['M', 'TV', 'S']
    if typed not in choices:
        raise argparse.ArgumentTypeError(
            f"Invalid type: '{typed}'. Choose from: {', '.join(choices)}.'"
        )
    return typed

def parsing():
    parser = argparse.ArgumentParser(description='Welcome into the Movie Ranking Program! ')

    parser.add_argument('-start_year', default=None, type=int, dest='start_year',
                        help="Start year for analysis. From when do you want to start your analysis?")
    parser.add_argument('-end_year', default=None, type=int, dest="end_year",
                        help='End year for analysis. Where do you want to end your analysis?')
    parser.add_argument('-type_of_media', default=None, type=movie_type, dest='type_of_media',
                        help="What type of media you want to analyze? Movies - M, Tv Series - TV, or Shorts - S? Type M, TV or S. Otherwise, all types will be included.")
    parser.add_argument('-n', default=10000, type=int, dest='n',
                        help="How many votes is sufficient for you? The base is 10000.")

    args = parser.parse_args()

    result = run_analysis(
        start_year=args.start_year,
        end_year=args.end_year,
        type_of_media=args.type_of_media,
        n=args.n
    )

if __name__ == "__main__":
    parsing()




