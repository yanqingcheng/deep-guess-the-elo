import os
import pandas as pd
import chess
import chess.svg
import cairosvg

# ---- Configurable paths and parameters ----
IN_CSV = "data/extracted_games.csv"
OUT_IMG_DIR = "data/images_exp1/"
OUT_LABELS_CSV = "data/images_exp1_labels.csv"
N_ROWS = 1000  # Set to None for all rows

os.makedirs(OUT_IMG_DIR, exist_ok=True)
records = []

def elo_bucket(white, black):
    """Basic experiment 1 bucketing: noob (<1200), club (1200–2200), master (>2200)."""
    try:
        elo = min(int(white), int(black))
    except Exception:
        return None
    if elo < 1200:
        return "noob"
    elif elo > 2200:
        return "master"
    else:
        return "club"

# ---- Main script ----
df = pd.read_csv(IN_CSV)
if N_ROWS:
    df = df.head(N_ROWS)

for idx, row in df.iterrows():
    white_elo = row["white_elo"]
    black_elo = row["black_elo"]
    fen = row["final_fen"]
    label = elo_bucket(white_elo, black_elo)
    if label is None:
        continue  # skip if rating is missing or malformed

    filename = f"{label}_{idx}.png"
    outpath = os.path.join(OUT_IMG_DIR, filename)

    # FEN to SVG to PNG
    board = chess.Board(fen)
    svg = chess.svg.board(board=board)
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=outpath)

    records.append({"filename": filename, "label": label})

    if idx % 100 == 0:
        print(f"Saved {idx} images...")

# Save label mapping for fastai
labels_df = pd.DataFrame(records)
labels_df.to_csv(OUT_LABELS_CSV, index=False)
print(f"Image generation complete! Saved {len(records)} images and labels to {OUT_IMG_DIR} and {OUT_LABELS_CSV}")
