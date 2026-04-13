import argparse
import gzip
import shutil
import sys
import urllib.request
from pathlib import Path

DATASETS_URL = "https://datasets.imdbws.com/"

REQ_DATASETS = {
    "title.akas.tsv.gz",
    "title.basics.tsv.gz",
    "title.ratings.tsv.gz"
}

DATASETS_DIR = Path(__file__).parent / "datasets"

def _progress_hook(block_num, block_size, total_size):
    downloaded = block_num * block_size
    if total_size > 0:
        percent = min(100, downloaded*100//total_size)
        mb_downloaded = downloaded/(1024*1024)
        mb_total = total_size/(1024*1024)
        filled = int(30*percent/100)
        bar = '█' * filled + '░' * (30 - filled)
        sys.stdout.write(
            f"\r {bar} {percent}% "
            f"{round(mb_downloaded,3)}/{round(mb_total,3)} MB"
        )
    else:
        mb_downloaded = downloaded / (1024*1024)
        sys.stdout.write(
            f"\r Downloaded: {mb_downloaded} MB"
        )
    sys.stdout.flush()

def download_dataset(name):
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)
    gz_path = DATASETS_DIR / name
    tsv_name = name.replace('.gz', '')
    tsv_path = DATASETS_DIR / tsv_name

    if tsv_path.exists():
        print(f"Dataset {tsv_path} already exists. Skipped.")
        return True

    print(f"Downloading {name}...")
    try:
        urllib.request.urlretrieve(DATASETS_URL + name, gz_path, reporthook=_progress_hook)
        print()
    except Exception as e:
        print(f"Error downloading {name}: {e}")
        return False

    try:
        with gzip.open(gz_path, 'rb') as f_in, open(tsv_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        gz_path.unlink()
        print(f"Extraction of {name}: done.")
    except Exception as e:
        print(f"Error extracting {name}: {e}")
        return False

    return True

def cmd_download(args):
    for ds in REQ_DATASETS:
        download_dataset(ds)
    print(f"Downloading: done.")

def cmd_analyze(args, analyze_parser):
    if len(sys.argv) == 2:
        analyze_parser.print_help()
        sys.exit(0)

    missing = []
    for ds in sorted(REQ_DATASETS):
        tsv = ds.replace('.gz', '')
        if not (DATASETS_DIR / tsv).exists():
            missing.append(tsv)
    if missing:
        print(f"Missing required datasets: {', '.join(missing)}")
        print(f"Run python script.py download to fetch them.")
        sys.exit(1)

    try:
        from analysing import run_analysis
    except ImportError as e:
        print(f"Import error: {e}")
        print(f"Make sure all dependencies are installed. Run pip install -r requirements.txt")
        sys.exit(1)

    run_analysis(
        start_year=args.start_year,
        end_year=args.end_year,
        type_of_media=args.type_of_media,
        votes=args.votes
    )

def movie_type(typed):
    choices=['M', 'TV', 'S']
    if typed not in choices:
        raise argparse.ArgumentTypeError(
            f"Invalid type: '{typed}'. Choose from: {', '.join(choices)}.'"
        )
    return typed

def parsing():
    parser = argparse.ArgumentParser(description='Welcome into the Movie Ranking Program! Remember to assure that you have all required datasets first.')
    
    sub = parser.add_subparsers(dest='command', title='commands')
    
    dp = sub.add_parser('download', help='Download data for analysing.')
    dp.add_argument('dataset', nargs='?', default=None, metavar='DATASET',
                    help='The name of the dataset to download.')

    ap = sub.add_parser('analyze', help='Run analysis.')
    ap.add_argument('-start_year', default=None, type=int, dest='start_year',
                        help="Start year for analysis. From when do you want to start your analysis?")
    ap.add_argument('-end_year', default=None, type=int, dest="end_year",
                        help='End year for analysis. Where do you want to end your analysis?')
    ap.add_argument('-type_of_media', default=None, type=movie_type, dest='type_of_media',
                        help="What type of media you want to analyze? Movies - M, Tv Series - TV, or Shorts - S? Type M, TV or S. Otherwise, all types will be included.")
    ap.add_argument('-votes', default=10000, type=int, dest='votes',
                        help="How many votes is sufficient for you? The base is 10000.")

    return parser, ap

def main():
    parser, analyze_parser = parsing()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)
    elif args.command == 'download':
        cmd_download(args)
    elif args.command == 'analyze':
        cmd_analyze(args, analyze_parser)

if __name__ == "__main__":
    main()




