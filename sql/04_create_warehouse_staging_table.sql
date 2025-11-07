-- Ensure the warehouse schema exists
CREATE SCHEMA IF NOT EXISTS warehouse;

-- Drop the staging table if it already exists to allow for reruns of this script
DROP TABLE IF EXISTS warehouse.transactions_staging;

-- Create the new staging table
CREATE TABLE warehouse.transactions_staging (
    -- Note: Staging tables typically don't use SERIAL PRIMARY KEYs or foreign keys, 
    -- as they are temporary holding areas. We just mirror the column structure.

    transaction_id INTEGER, -- We will insert existing IDs or handle generation in the final merge step
    category INTEGER,
    amt NUMERIC(10, 4),
    gender INTEGER,
    street INTEGER,
    city INTEGER,
    state INTEGER,
    zip INTEGER,
    lat NUMERIC(10, 6),
    long NUMERIC(10, 6),
    city_pop INTEGER,
    job INTEGER,
    merch_lat NUMERIC(10, 6),
    merch_long NUMERIC(10, 6),
    trans_month INTEGER,
    trans_day INTEGER,
    trans_hour INTEGER,
    age INTEGER,
    is_fraud INTEGER
);

-- Optional: Add a note indicating this is a temporary staging table
COMMENT ON TABLE warehouse.transactions_staging IS 'Temporary table for loading processed data before merging into warehouse.transactions_processed.';
