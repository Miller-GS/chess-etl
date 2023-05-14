from twic import TWICClient
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "execution_date", help="The execution date of the DAG in YYYY-MM-DD format"
    )
    args = parser.parse_args()

    pgn_content = fetch_pgn_from_twic(args.execution_date)
    write_pgns(pgn_content, args.execution_date)


def fetch_pgn_from_twic(execution_date) -> str:
    client = TWICClient()
    return client.download_pgn_from_date(execution_date)


def write_pgns(pgn_content: str, execution_date: str) -> None:
    with open(f"/local_files/pgns/{execution_date}.pgn", "w+") as f:
        f.write(pgn_content)


if __name__ == "__main__":
    main()
