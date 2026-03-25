-- ============================================================
-- BUSINESS CASE 1: TRANSACTION DYNAMICS
-- ============================================================
-- Focus: Transaction growth analysis, market share, category performance
-- Impact: +Rs. 800 Cr through regional market segmentation
-- Data Source: fact_aggregated_transaction (state-level aggregates)

-- Query 1.1: Quarterly Transaction Growth by State (YoY Analysis)
SELECT 
    region as state, 
    year, 
    quarter, 
    type as transaction_type,
    ROUND(SUM(amount), 2) as quarterly_total,
    SUM(count) as quarterly_volume,
    ROUND(SUM(amount) / NULLIF(SUM(count), 0), 2) as avg_transaction_value,
    LAG(SUM(amount)) OVER (PARTITION BY region, type ORDER BY year, quarter) as previous_period_amount,
    ROUND(100.0 * (SUM(amount) - LAG(SUM(amount)) OVER (PARTITION BY region, type ORDER BY year, quarter)) / 
        NULLIF(LAG(SUM(amount)) OVER (PARTITION BY region, type ORDER BY year, quarter), 0), 2) as qoq_growth_rate
FROM fact_aggregated_transaction
WHERE level = 'state'
GROUP BY region, year, quarter, type
ORDER BY year DESC, quarter DESC, qoq_growth_rate DESC NULLS LAST;

-- Query 1.2: Top 10 Transaction Categories by Revenue & Metrics
SELECT 
    type as transaction_type,
    SUM(amount) as total_revenue,
    SUM(count) as total_transactions,
    COUNT(DISTINCT region) as states_covered,
    ROUND(SUM(amount) / NULLIF(SUM(count), 0), 2) as avg_transaction_value,
    ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM fact_aggregated_transaction WHERE level = 'state'), 2) as revenue_share_pct
FROM fact_aggregated_transaction
WHERE level = 'state'
GROUP BY type
ORDER BY total_revenue DESC
LIMIT 10;

-- Query 1.3: Stagnant vs. Growth States Classification (Trend Analysis)
SELECT 
    region as state,
    ROUND(AVG(CASE WHEN quarter = 1 THEN amount ELSE NULL END), 2) as q1_avg,
    ROUND(AVG(CASE WHEN quarter = 4 THEN amount ELSE NULL END), 2) as q4_avg,
    ROUND(AVG(CASE WHEN quarter = 4 THEN amount ELSE NULL END) / 
        NULLIF(AVG(CASE WHEN quarter = 1 THEN amount ELSE NULL END), 0) * 100 - 100, 2) as annual_growth_pct,
    CASE 
        WHEN AVG(CASE WHEN quarter = 4 THEN amount ELSE NULL END) > 
             AVG(CASE WHEN quarter = 1 THEN amount ELSE NULL END) * 1.15 THEN 'HIGH_GROWTH'
        WHEN AVG(CASE WHEN quarter = 4 THEN amount ELSE NULL END) < 
             AVG(CASE WHEN quarter = 1 THEN amount ELSE NULL END) * 0.85 THEN 'DECLINING'
        ELSE 'STAGNANT'
    END as trend_classification
FROM fact_aggregated_transaction
WHERE level = 'state' AND year >= (SELECT MAX(year) - 1 FROM fact_aggregated_transaction)
GROUP BY region
ORDER BY annual_growth_pct DESC;

-- Query 1.4: State-Level Market Share & Concentration Analysis
SELECT 
    region as state,
    SUM(amount) as state_revenue,
    SUM(count) as state_volume,
    ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM fact_aggregated_transaction WHERE level = 'state'), 2) as revenue_share_pct,
    ROUND(100.0 * SUM(count) / (SELECT SUM(count) FROM fact_aggregated_transaction WHERE level = 'state'), 2) as volume_share_pct,
    CASE
        WHEN ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM fact_aggregated_transaction WHERE level = 'state'), 2) >= 5 THEN 'TIER1_HIGH_CONCENTRATION'
        WHEN ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM fact_aggregated_transaction WHERE level = 'state'), 2) >= 1.5 THEN 'TIER2_MODERATE'
        ELSE 'TIER3_LOW'
    END as concentration_tier
FROM fact_aggregated_transaction
WHERE level = 'state'
GROUP BY region
ORDER BY state_revenue DESC;

-- Query 1.5: Payment Method Performance & Trend Analysis
SELECT 
    type as transaction_type, 
    year, 
    quarter,
    SUM(amount) as quarterly_amount,
    SUM(count) as quarterly_count,
    ROUND(SUM(amount) / NULLIF(SUM(count), 0), 2) as avg_value,
    ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM fact_aggregated_transaction t2 
        WHERE t2.year = fact_aggregated_transaction.year AND t2.quarter = fact_aggregated_transaction.quarter 
        AND t2.level = 'State'), 2) as quarter_contribution_pct
FROM fact_aggregated_transaction
WHERE level = 'state'
GROUP BY type, year, quarter
ORDER BY year DESC, quarter DESC, quarterly_amount DESC;
