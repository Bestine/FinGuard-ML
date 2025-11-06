-- RAW DATA
-- First, drop the table if it already exists to prevent errors
-- and ensure you are working with a fresh structure.
DROP TABLE IF EXISTS raw.transactions_raw;

CREATE TABLE raw.transactions_raw (
    trans_date_trans_time VARCHAR(255), -- Storing as VARCHAR for raw input, will process to timestamp later
    cc_num VARCHAR(255), -- Store credit card numbers as text
    merchant VARCHAR(255),
    category VARCHAR(255),
    amt NUMERIC(10, 2), -- Amount with 2 decimal places
    first VARCHAR(255),
    last VARCHAR(255),
    gender VARCHAR(10),
    street VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(2),
    zip VARCHAR(10),
    lat NUMERIC(10, 6),
    long NUMERIC(10, 6),
    city_pop INTEGER,
    job VARCHAR(255),
    dob VARCHAR(255), -- Storing as VARCHAR for raw input
    trans_num VARCHAR(255), -- Transaction number as text
    unix_time BIGINT, -- Unix timestamp as big integer
    merch_lat NUMERIC(10, 6),
    merch_long NUMERIC(10, 6),
    is_fraud INTEGER -- Assuming 0 or 1 for fraud status
);


-- TRANSFORMED DATA 
-- First, drop the table if it already exists to prevent errors
-- and ensure you are working with a fresh structure.
DROP TABLE IF EXISTS warehouse.transactions_processed;

-- Now create the table with the desired numeric features
CREATE TABLE warehouse.transactions_processed (
    transaction_id SERIAL PRIMARY KEY, -- System-generated surrogate key for database management

    -- All features below are numeric, representing encoded/transformed data points
    category INTEGER,        -- Assuming category is label-encoded or one-hot-encoded to an integer
    amt NUMERIC(10, 4),      -- Amount, likely standardized or scaled
    gender INTEGER,          -- 0 or 1, or other integer encoding
    street INTEGER,          -- Encoded street information
    city INTEGER,            -- Encoded city information
    state INTEGER,           -- Encoded state information
    zip INTEGER,             -- Encoded zip code as an integer
    lat NUMERIC(10, 6),      -- Latitude, still a numeric value
    long NUMERIC(10, 6),     -- Longitude, still a numeric value
    city_pop INTEGER,        -- City population, an integer
    job INTEGER,             -- Encoded job title
    merch_lat NUMERIC(10, 6),-- Merchant latitude
    merch_long NUMERIC(10, 6),-- Merchant longitude
    trans_month INTEGER,     -- Numeric representation of the month (1-12)
    trans_day INTEGER,       -- Numeric representation of the day (1-31)
    trans_hour INTEGER,      -- Numeric representation of the hour (0-23)
    age INTEGER,             -- Age calculated as an integer
    is_fraud INTEGER         -- Target variable, likely 0 or 1
);

-- PREDICTIONS DATA 
-- First, drop the table if it already exists to prevent errors
-- and ensure you are working with a fresh structure.
DROP TABLE IF EXISTS public.predictions;

CREATE TABLE public.predictions (
    prediction_id SERIAL PRIMARY KEY,
    transaction_id INTEGER REFERENCES warehouse.transactions_processed(transaction_id), -- Foreign key to processed table
    prediction_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    predicted_fraud_probability NUMERIC(5, 4),
    predicted_is_fraud BOOLEAN,
    model_version VARCHAR(255)
);

-- EXPLANATIONS DATA 
-- First, drop the table if it already exists to prevent errors
-- and ensure you are working with a fresh structure.
DROP TABLE IF EXISTS public.explanations;

CREATE TABLE public.explanations (
    explanation_id SERIAL PRIMARY KEY,
    transaction_id INTEGER REFERENCES warehouse.transactions_processed(transaction_id), -- Foreign key
    explanation_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    feature_importance JSONB, -- Use JSONB for storing flexible, semi-structured data like feature weights/SHAP values
    explanation_text TEXT
);
