-- ============================================================
-- BUSINESS CASE 2: DEVICE ENGAGEMENT
-- ============================================================
-- Focus: User engagement, registration trends, app opens analysis
-- Impact: +Rs. 650 Cr through OS-specific optimization
-- Data Source: fact_aggregated_user (state-level user metrics)

-- Query 2.1: State-Level User Registration & Engagement Metrics
SELECT 
    region as state,
    SUM(count) as total_users,
    COUNT(DISTINCT device) as device_types,
    MIN(year) as first_year,
    MAX(year) as latest_year,
    CASE
        WHEN SUM(count) > 5000000 THEN 'HIGHLY_ENGAGED'
        WHEN SUM(count) > 1000000 THEN 'MODERATELY_ENGAGED'
        WHEN SUM(count) > 100000 THEN 'LOW_ENGAGEMENT'
        ELSE 'DORMANT'
    END as engagement_level,
    ROUND(100.0 * SUM(count) / (SELECT SUM(count) FROM fact_aggregated_user WHERE level = 'state'), 2) as user_market_share_pct
FROM fact_aggregated_user
WHERE level = 'state'
GROUP BY region
ORDER BY total_users DESC;

-- Query 2.2: User Engagement Trends by Quarter & Year
SELECT 
    region as state, 
    year, 
    quarter,
    count as registered_users,
    LAG(count) OVER (PARTITION BY region ORDER BY year, quarter) as prev_quarter_users,
    ROUND(100.0 * (count - LAG(count) OVER (PARTITION BY region ORDER BY year, quarter)) / 
        NULLIF(LAG(count) OVER (PARTITION BY region ORDER BY year, quarter), 0), 2) as qoq_user_growth_pct
FROM fact_aggregated_user
WHERE level = 'state'
ORDER BY year DESC, quarter DESC, state;

-- Query 2.3: Top User Growth States Classification
SELECT 
    region as state,
    SUM(CASE WHEN quarter = 1 THEN count ELSE 0 END) as q1_users,
    SUM(CASE WHEN quarter = 4 THEN count ELSE 0 END) as q4_users,
    ROUND(100.0 * (SUM(CASE WHEN quarter = 4 THEN count ELSE 0 END) - 
        SUM(CASE WHEN quarter = 1 THEN count ELSE 0 END)) / 
        NULLIF(SUM(CASE WHEN quarter = 1 THEN count ELSE 0 END), 0), 2) as annual_user_growth_pct,
    CASE
        WHEN ROUND(100.0 * (SUM(CASE WHEN quarter = 4 THEN count ELSE 0 END) - 
            SUM(CASE WHEN quarter = 1 THEN count ELSE 0 END)) / 
            NULLIF(SUM(CASE WHEN quarter = 1 THEN count ELSE 0 END), 0), 2) >= 30 THEN 'HIGH_GROWTH_30_PLUS'
        WHEN ROUND(100.0 * (SUM(CASE WHEN quarter = 4 THEN count ELSE 0 END) - 
            SUM(CASE WHEN quarter = 1 THEN count ELSE 0 END)) / 
            NULLIF(SUM(CASE WHEN quarter = 1 THEN count ELSE 0 END), 0), 2) >= 10 THEN 'MODERATE_GROWTH_10_30'
        ELSE 'LOW_GROWTH_0_10'
    END as growth_classification
FROM fact_aggregated_user
WHERE level = 'state' AND year >= (SELECT MAX(year) - 1 FROM fact_aggregated_user)
GROUP BY region
ORDER BY annual_user_growth_pct DESC;

-- Query 2.4: Device Type Engagement Breakdown by State
SELECT 
    region as state,
    device,
    SUM(count) as device_users,
    COUNT(DISTINCT year) as years_active,
    ROUND(100.0 * SUM(count) / (SELECT SUM(count) FROM fact_aggregated_user WHERE level = 'state' AND region = fact_aggregated_user.region), 2) as device_share_pct
FROM fact_aggregated_user
WHERE level = 'state'
GROUP BY region, device
ORDER BY state, device_users DESC;

-- Query 2.5: Top Device Types Nationally
SELECT 
    device,
    SUM(count) as total_users,
    COUNT(DISTINCT region) as states_covered,
    ROUND(100.0 * SUM(count) / (SELECT SUM(count) FROM fact_aggregated_user WHERE level = 'state'), 2) as national_share_pct,
    MAX(count) as max_users_in_state,
    ROUND(AVG(count), 0) as avg_users_per_state
FROM fact_aggregated_user
WHERE level = 'state'
GROUP BY device
ORDER BY total_users DESC;

-- Query 2.6: Device Efficiency & Growth Score (Latest Year)
SELECT 
    region as state,
    device,
    SUM(count) as total_users,
    ROUND(100.0 * SUM(count) / (SELECT SUM(count) FROM fact_aggregated_user WHERE level = 'state'), 2) as engagement_share_pct,
    CASE
        WHEN SUM(count) > 5000000 THEN 'EXCELLENT_LEADER (>5M)'
        WHEN SUM(count) > 1000000 THEN 'STRONG_PERFORMER (1-5M)'
        WHEN SUM(count) > 100000 THEN 'MODERATE_GROWTH (100K-1M)'
        ELSE 'EMERGING_MARKET (<100K)'
    END as efficiency_classification,
    ROW_NUMBER() OVER (PARTITION BY device ORDER BY SUM(count) DESC) as device_rank
FROM fact_aggregated_user
WHERE level = 'state' AND year = (SELECT MAX(year) FROM fact_aggregated_user)
GROUP BY region, device
ORDER BY device, total_users DESC;
