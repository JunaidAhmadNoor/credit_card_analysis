
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


CREATE TABLE IF NOT EXISTS monthly_trends (
    year_month         TEXT,
    total_spend         REAL,
    avg_transaction     REAL,
    transaction_count   INTEGER,
    fraud_count         INTEGER,
    fraud_rate_pct      REAL
);


CREATE TABLE IF NOT EXISTS spend_by_city (
    city              TEXT,
    state             TEXT,
    lat               REAL,
    long              REAL,
    total_spend       REAL,
    transaction_count INTEGER
);


CREATE TABLE IF NOT EXISTS spend_by_category (
    category_display   TEXT,
    category           TEXT,
    total_spend        REAL,
    transaction_count  INTEGER
);
