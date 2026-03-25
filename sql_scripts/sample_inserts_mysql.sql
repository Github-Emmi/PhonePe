-- Sample DML: INSERT Statements
-- These are template statements - use Python/Pandas for batch inserts

-- Sample: fact_aggregated_transaction
INSERT INTO fact_aggregated_transaction (year, quarter, level, region, category, type, count, amount) VALUES
  (2020, 1, 'country', 'india', 'Peer-to-peer payments', 'TOTAL', 693998661, 2320557268853.59),
  (2020, 1, 'country', 'india', 'Merchant payments', 'TOTAL', 566355270, 231298042209.84),
  (2020, 1, 'country', 'india', 'Recharge & bill payments', 'TOTAL', 351300991, 140373550367.16);
