-- *******************************************************************
-- 03_indexes_constraints.sql: Add Keys and Indexes for Performance and Integrity
-- *******************************************************************


-- -------------------------------------------------------------------
-- 1. Constraints and Indexes for warehouse.transactions_processed
--    (Optimizing for ML model input and data analysis)
-- -------------------------------------------------------------------

-- The PRIMARY KEY 'transaction_id' was defined during table creation,
-- which automatically created a unique index for it.

-- Index the target variable 'is_fraud' for quick analysis of fraud cases
CREATE INDEX idx_transactions_processed_is_fraud
ON warehouse.transactions_processed (is_fraud);

-- Index time components for time-series filtering and analysis
CREATE INDEX idx_transactions_processed_time_components
ON warehouse.transactions_processed (trans_month, trans_day, trans_hour);

-- Index location data if spatial analysis/filtering is common
CREATE INDEX idx_transactions_processed_location
ON warehouse.transactions_processed (lat, long);


-- -------------------------------------------------------------------
-- 2. Constraints and Indexes for public.predictions
--    (Ensuring data integrity and fast lookups of prediction results)
-- -------------------------------------------------------------------

-- Add Foreign Key constraint linking back to the processed table
-- This ensures that every prediction corresponds to a valid processed transaction ID.
ALTER TABLE public.predictions
ADD CONSTRAINT fk_predictions_transaction
FOREIGN KEY (transaction_id) REFERENCES warehouse.transactions_processed(transaction_id);

-- Index the 'transaction_id' in the predictions table for efficient lookups
-- (e.g., "Show me the prediction results for transaction 1234")
CREATE INDEX idx_predictions_transaction_id
ON public.predictions (transaction_id);

-- Index the timestamp column, as users often query for recent predictions
CREATE INDEX idx_predictions_timestamp
ON public.predictions (prediction_timestamp);


-- -------------------------------------------------------------------
-- 3. Constraints and Indexes for public.explanations
--    (Ensuring data integrity and linking explanations to predictions)
-- -------------------------------------------------------------------

-- Add Foreign Key constraint linking back to the processed table
ALTER TABLE public.explanations
ADD CONSTRAINT fk_explanations_transaction
FOREIGN KEY (transaction_id) REFERENCES warehouse.transactions_processed(transaction_id);

-- Index the 'transaction_id' in the explanations table for efficient lookups
CREATE INDEX idx_explanations_transaction_id
ON public.explanations (transaction_id);


-- -------------------------------------------------------------------
-- 4. Indexes for raw.transactions_raw
--    (Useful for efficient data loading and validation processes)
-- -------------------------------------------------------------------

-- Index the business key 'trans_num' to help efficiently cross-reference 
-- raw records when loading or validating against other tables.
CREATE INDEX idx_transactions_raw_trans_num
ON raw.transactions_raw (trans_num);

-- Index cc_num if you need to quickly check raw history for specific cards
CREATE INDEX idx_transactions_raw_cc_num
ON raw.transactions_raw (cc_num);
