import re
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "credit_card_transactions.csv"
OUTPUT_DIR = PROJECT_ROOT / "output"

CHUNK_SIZE = None


def normalize_merchant(name: str) -> str:

    if not isinstance(name, str) or not name.strip():
        return ""
    s = name.strip()
    # Remove fraud_ prefix 
    if s.lower().startswith("fraud_"):
        s = s[6:].strip()
    # Replace commas and multiple spaces with single space
    s = re.sub(r"[,]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    # Remove trailing " 001", " 002", etc. to group "Starbucks 001" vs "Starbucks 002"
    s = re.sub(r"\s+0*\d{1,5}$", "", s)
    return s.strip()


def load_and_clean(csv_path: Path) -> pd.DataFrame:
    """Load data"""
    print(f"Loading...")
    df = pd.read_csv(csv_path)

    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    df["trans_date_trans_time"] = pd.to_datetime(df["trans_date_trans_time"], errors="coerce")
    df["dob"] = pd.to_datetime(df["dob"], errors="coerce")

    df["user_id"] = pd.factorize(df["cc_num"], sort=False)[0] + 1

    # Drop rows with missing critical fields
    before = len(df)
    df = df.dropna(subset=["amt", "trans_date_trans_time"])
    if len(df) < before:
        print(f"  Dropped {before - len(df)} rows with missing amt or trans_date_trans_time.")
    df["merch_zipcode"] = df["merch_zipcode"].fillna(0).astype("Int64")

    # Merchant normalization
    df["merchant_normalized"] = df["merchant"].astype(str).apply(normalize_merchant)

    df["category_display"] = df["category"].astype(str).str.replace("_", " ", regex=False)

    # Time dimensions
    df["year"] = df["trans_date_trans_time"].dt.year
    df["month"] = df["trans_date_trans_time"].dt.month
    df["year_month"] = df["trans_date_trans_time"].dt.to_period("M").astype(str)

    return df


def export_for_power_bi(df: pd.DataFrame, out_dir: Path) -> None:
    """Export main fact table and optional aggregates to out_dir."""
    out_dir.mkdir(parents=True, exist_ok=True)

    fact = df[
        [
            "trans_date_trans_time",
            "year",
            "month",
            "year_month",
            "user_id",
            "cc_num",
            "merchant",
            "merchant_normalized",
            "category",
            "category_display",
            "amt",
            "first",
            "last",
            "gender",
            "city",
            "state",
            "zip",
            "lat",
            "long",
            "city_pop",
            "is_fraud",
            "merch_lat",
            "merch_long",
            "merch_zipcode",
        ]
    ].copy()
    fact.columns = [
        "trans_datetime",
        "year",
        "month",
        "year_month",
        "user_id",
        "cc_num",
        "merchant_raw",
        "merchant",
        "category",
        "category_display",
        "amount",
        "first_name",
        "last_name",
        "gender",
        "city",
        "state",
        "zip",
        "lat",
        "long",
        "city_pop",
        "is_fraud",
        "merch_lat",
        "merch_long",
        "merch_zipcode",
    ]
    out_fact = out_dir / "credit_card_for_power_bi.csv"
    fact.to_csv(out_fact, index=False, date_format="%Y-%m-%d %H:%M:%S")

    monthly = (
        df.groupby("year_month")
        .agg(
            total_spend=("amt", "sum"),
            avg_transaction=("amt", "mean"),
            transaction_count=("amt", "count"),
            fraud_count=("is_fraud", "sum"),
        )
        .reset_index()
    )
    monthly["fraud_rate_pct"] = (monthly["fraud_count"] / monthly["transaction_count"] * 100).round(2)
    monthly.to_csv(out_dir / "monthly_trends.csv", index=False)

    # Spend by city
    by_city = (
        df.groupby(["city", "state", "lat", "long"])
        .agg(total_spend=("amt", "sum"), transaction_count=("amt", "count"))
        .reset_index()
    )
    by_city.to_csv(out_dir / "spend_by_city.csv", index=False)

    # Spend by category
    by_category = (
        df.groupby(["category_display", "category"])
        .agg(total_spend=("amt", "sum"), transaction_count=("amt", "count"))
        .reset_index()
    )
    by_category.to_csv(out_dir / "spend_by_category.csv", index=False)


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_PATH}")
    df = load_and_clean(DATA_PATH)
    export_for_power_bi(df, OUTPUT_DIR)


if __name__ == "__main__":
    main()
