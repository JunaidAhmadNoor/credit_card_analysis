import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
DB_PATH = OUTPUT_DIR / "credit_card.db"


def load_csv(path: Path) -> pd.DataFrame:
    """Load CSV file"""
    df = pd.read_csv(path)
    for col in df.columns:
        if "date" in col.lower() or col == "trans_datetime":
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
            except Exception:
                pass
    return df


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not (OUTPUT_DIR / "credit_card_for_power_bi.csv").exists():
        raise FileNotFoundError(
            "Run clean_transactions.py first to create output CSVs."
        )

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)

    try:
        print("Loading credit_card_for_power_bi.csv...")
        fact = load_csv(OUTPUT_DIR / "credit_card_for_power_bi.csv")
        fact.to_sql(
            "transactions",
            conn,
            if_exists="replace",
            index=False,
            method="multi",
            chunksize=40,  # SQLite limit: ~999 variables per statement (rows × columns)
        )

        # Monthly trends
        print("Loading monthly_trends.csv...")
        monthly = load_csv(OUTPUT_DIR / "monthly_trends.csv")
        monthly.to_sql("monthly_trends", conn, if_exists="replace", index=False)

        # Spend by city
        print("Loading spend_by_city.csv...")
        by_city = load_csv(OUTPUT_DIR / "spend_by_city.csv")
        by_city.to_sql("spend_by_city", conn, if_exists="replace", index=False)

        # Spend by category
        print("Loading spend_by_category.csv...")
        by_cat = load_csv(OUTPUT_DIR / "spend_by_category.csv")
        by_cat.to_sql("spend_by_category", conn, if_exists="replace", index=False)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
