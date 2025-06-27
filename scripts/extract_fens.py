import argparse
import chess.pgn
import csv
import os

# extract_fens.py
# This script extracts final FENs and ratings from a Lichess PGN file and saves them to a CSV file.
# Usage: python extract_fens.py --input-pgn <path_to_pgn> --max-games <number> --out <output_csv>

DEFAULT_PGN = "/mnt/d/Data/lichess/lichess_db_standard_rated_2025-02.pgn"
DEFAULT_OUT = "data/extracted_games.csv"
DEFAULT_N = 1000

def main():
    parser = argparse.ArgumentParser(description="Extract final FENs and ratings from a Lichess PGN file.")
    parser.add_argument("--input-pgn", default=DEFAULT_PGN, help=f"Path to source PGN file (default: {DEFAULT_PGN})")
    parser.add_argument("--max-games", type=int, default=DEFAULT_N, help=f"Number of games to extract (default: {DEFAULT_N})")
    parser.add_argument("--out", default=DEFAULT_OUT, help=f"Destination CSV filename (default: {DEFAULT_OUT})")
    args = parser.parse_args()

    # Make sure output dir exists
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    with open(args.input_pgn, encoding="utf-8", errors="ignore") as pgn_file, \
         open(args.out, "w", newline='', encoding="utf-8") as csvfile:

        writer = csv.writer(csvfile)
        writer.writerow(["game_idx", "white_elo", "black_elo", "final_fen"])  # CSV header

        for idx in range(args.max_games):
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break

            white_elo = game.headers.get("WhiteElo")
            black_elo = game.headers.get("BlackElo")
            final_fen = game.end().board().fen()
            writer.writerow([idx, white_elo, black_elo, final_fen])

            if (idx+1) % 100 == 0:
                print(f"Extracted {idx+1} games...")

    print(f"Done! {idx+1 if game else idx} games written to {args.out}")

if __name__ == "__main__":
    main()
