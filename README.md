Credit Card Analysis
Download data from this link "https://www.kaggle.com/datasets/priyamchoksi/credit-card-transactions-dataset" and then create a new folder "data" and place the data file in the folder

Then run this command "python scripts/clean_transactions.py"
Then run this command "python scripts/load_to_sql.py"

Power Query
1 - credit_card_for_power_bi
        `trans_datetime` - Date/Time
        `amount` - Decimal;
        `is_fraud` - Whole number

2 - monthly_trends
        `year_month` - Text (or create a Date from it)
        numeric columns as Decimal

3 - spend_by_city
        `lat`, `long` - Decimal
        `total_spend` - Decimal

4 - spend_by_category
        `total_spend` - Decimal


SQL

1 - Total Spend
    SELECT SUM(amount) AS total_spend FROM transactions;

2 - Average Transaction Value
    SELECT AVG(amount) AS avg_transaction FROM transactions;

3 - Fraud Rate (%)
    SELECT 
        SUM(is_fraud) * 100.0 / COUNT(*) AS fraud_rate_pct 
    FROM transactions;

4 - Monthly trends 
    SELECT * FROM monthly_trends ORDER BY year_month;

5 - Spend by city
    SELECT * FROM spend_by_city ORDER BY total_spend DESC;

6 - Spend by category 
    SELECT * FROM spend_by_category ORDER BY total_spend DESC;

7 - Monthly totals
    SELECT 
        year_month,
        SUM(amount) AS total_spend,
        AVG(amount) AS avg_transaction,
        COUNT(*) AS transaction_count,
        SUM(is_fraud) AS fraud_count,
        ROUND(SUM(is_fraud) * 100.0 / COUNT(*), 2) AS fraud_rate_pct
    FROM transactions
    GROUP BY year_month
    ORDER BY year_month;

8 - Top 10 cities by spend
    SELECT city, state, SUM(amount) AS total_spend, COUNT(*) AS tx_count
    FROM transactions
    GROUP BY city, state
    ORDER BY total_spend DESC
    LIMIT 10;

9 - Top 10 categories by spend
    SELECT category_display, SUM(amount) AS total_spend, COUNT(*) AS tx_count
    FROM transactions
    GROUP BY category_display
    ORDER BY total_spend DESC
    LIMIT 10;

10 - Fraud rate by state
    SELECT 
        state,
        COUNT(*) AS transactions,
        SUM(is_fraud) AS fraud_count,
        ROUND(SUM(is_fraud) * 100.0 / COUNT(*), 2) AS fraud_rate_pct
    FROM transactions
    GROUP BY state
    ORDER BY fraud_rate_pct DESC;
