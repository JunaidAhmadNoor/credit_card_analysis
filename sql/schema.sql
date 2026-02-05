-- Credit Card Transactions: table definitions (reference)
-- SQLite creates these automatically when loading via load_to_sql.py.
-- Use this for SQL Server / PostgreSQL if you load data there.

-- Main fact table (one row per transaction)
CREATE TABLE IF NOT EXISTS transactions (
    trans_datetime  DATETIME,
    year            INTEGER,
    month           INTEGER,
    year_month      TEXT,
    user_id         INTEGER,
    cc_num          TEXT,
    merchant_raw    TEXT,
    merchant        TEXT,
    category        TEXT,
    category_display TEXT,
    amount          REAL,
    first_name      TEXT,
    last_name       TEXT,
    gender          TEXT,
    city            TEXT,
    state           TEXT,
    zip             TEXT,
    lat             REAL,
    long            REAL,
    city_pop        INTEGER,
    is_fraud        INTEGER,
    merch_lat       REAL,
    merch_long      REAL,
    merch_zipcode   INTEGER
);

-- Pre-aggregated: one row per month
CREATE TABLE IF NOT EXISTS monthly_trends (
    year_month         TEXT,
    total_spend         REAL,
    avg_transaction     REAL,
    transaction_count   INTEGER,
    fraud_count         INTEGER,
    fraud_rate_pct      REAL
);

-- Pre-aggregated: one row per city
CREATE TABLE IF NOT EXISTS spend_by_city (
    city              TEXT,
    state             TEXT,
    lat               REAL,
    long              REAL,
    total_spend       REAL,
    transaction_count INTEGER
);

-- Pre-aggregated: one row per category
CREATE TABLE IF NOT EXISTS spend_by_category (
    category_display   TEXT,
    category           TEXT,
    total_spend        REAL,
    transaction_count  INTEGER
);
