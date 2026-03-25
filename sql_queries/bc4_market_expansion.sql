-- ============================================================
-- BUSINESS CASE 4: MARKET EXPANSION
-- ============================================================
-- Focus: State performance analysis, geographic expansion opportunities
-- Impact: +Rs. 2,500 Cr through geographic expansion
-- Data Source: fact_map_transaction (state & district level transaction data)

-- Query 4.1: State-Level Transaction Performance Analytics (Comprehensive)
SELECT 
    region as state,
    SUM(amount) as annual_transaction_value,
    SUM(count) as annual_transaction_count,
    COUNT(DISTINCT type) as payment_categories,
    ROUND(SUM(amount) / NULLIF(SUM(count), 0), 2) as avg_transaction_size,
    ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM fact_map_transaction WHERE level = 'state'), 2) as revenue_market_share_pct,
    ROUND(100.0 * SUM(count) / (SELECT SUM(count) FROM fact_map_transaction WHERE level = 'state'), 2) as volume_market_share_pct,
    CASE
        WHEN ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM fact_map_transaction WHERE level = 'state'), 2) >= 5 THEN 'TIER1_ESTABLISHED'
        WHEN ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM fact_map_transaction WHERE level = 'state'), 2) >= 1.5 THEN 'TIER2_GROWTH'
        ELSE 'TIER3_EXPANSION_OPPORTUNITY'
    END as market_tier
FROM fact_map_transaction
WHERE level = 'state'
GROUP BY region
ORDER BY annual_transaction_value DESC;

-- Query 4.2: Geographic Expansion Opportunity Assessment (Revenue Per User Analysis)
SELECT 
    t.region as state,
    COUNT(DISTINCT t.region) as state_count,
    SUM(t.amount) as transaction_volume,
    ROUND(SUM(t.amount) / NULLIF(COUNT(DISTINCT t.region), 0), 2) as revenue_per_state,
    (SELECT ROUND(SUM(amount) / COUNT(DISTINCT region), 2) FROM fact_map_transaction WHERE level = 'state') as national_avg_revenue_per_state,
    CASE
        WHEN ROUND(SUM(t.amount) / NULLIF(COUNT(DISTINCT t.region), 0), 2) < 
             (SELECT ROUND(SUM(amount) / COUNT(DISTINCT region), 2) * 0.6 FROM fact_map_transaction WHERE level = 'state')
        THEN 'HIGH_EXPANSION_OPPORTUNITY'
        WHEN ROUND(SUM(t.amount) / NULLIF(COUNT(DISTINCT t.region), 0), 2) < 
             (SELECT ROUND(SUM(amount) / COUNT(DISTINCT region), 2) FROM fact_map_transaction WHERE level = 'state')
        THEN 'MODERATE_OPPORTUNITY'
        ELSE 'MATURE_MARKET'
    END as opportunity_classification,
    SUM(t.amount) as potential_revenue_uplift
FROM fact_map_transaction t
WHERE t.level = 'State' AND t.year = (SELECT MAX(year) FROM fact_map_transaction)
GROUP BY t.region
ORDER BY potential_revenue_uplift DESC;

-- Query 4.3: Top Payment Categories by Region  
SELECT 
    region as state, 
    type as transaction_type,
    SUM(amount) as revenue,
    SUM(count) as volume,
    ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM fact_map_transaction t2 WHERE t2.region = fact_map_transaction.region AND t2.level = 'State'), 2) as state_revenue_share_pct,
    ROUND(SUM(amount) / NULLIF(SUM(count), 0), 2) as avg_transaction_value,
    RANK() OVER (PARTITION BY region ORDER BY SUM(amount) DESC) as payment_rank_in_state
FROM fact_map_transaction
WHERE level = 'state'
GROUP BY region, type
HAVING SUM(amount) > 0
ORDER BY state, revenue DESC;

-- Query 4.4: Top Performing Geographic Clusters (District-Level Analysis)
WITH cluster_stats AS (
    SELECT 
        region,
        SUM(amount) as total_amount,
        SUM(count) as total_volume,
        ROW_NUMBER() OVER (ORDER BY SUM(amount) DESC) as rank_num,
        COUNT(*) OVER () as total_count
    FROM fact_map_transaction
    WHERE level = 'District'
    GROUP BY region
)
SELECT 
    region as state,
    ROUND(total_amount, 2) as district_revenue,
    total_volume as district_volume,
    ROUND(total_amount / NULLIF(total_volume, 0), 2) as avg_transaction_value,
    rank_num as revenue_rank_national,
    ROUND(100.0 * total_amount / (SELECT SUM(amount) FROM fact_map_transaction WHERE level = 'District'), 2) as national_share_pct,
    (SELECT COUNT(DISTINCT type) FROM fact_map_transaction t2 WHERE t2.region = cluster_stats.region) as transaction_types,
    CASE
        WHEN rank_num <= (total_count * 0.25) THEN 'TOP_QUARTILE_HIGH_POTENTIAL'
        WHEN rank_num <= (total_count * 0.50) THEN 'ABOVE_MEDIAN_CLUSTERS'
        ELSE 'EMERGING_CLUSTERS'
    END as cluster_classification
FROM cluster_stats
WHERE total_amount > 0
ORDER BY district_revenue DESC;
