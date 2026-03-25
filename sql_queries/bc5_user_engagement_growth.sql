-- ============================================================
-- BUSINESS CASE 5: USER ENGAGEMENT GROWTH
-- ============================================================
-- Focus: User growth trajectory, engagement lifecycle, retention
-- Impact: +Rs. 900 Cr through retention optimization
-- Data Source: fact_aggregated_user (state-level user data)

-- Query 5.1: User Growth Trajectory by Quarter (Acquisition Momentum)
SELECT 
    region as state, 
    year, 
    quarter,
    count as quarterly_users,
    LAG(count) OVER (PARTITION BY region ORDER BY year, quarter) as prev_quarter_users,
    ROUND(100.0 * (count - LAG(count) OVER (PARTITION BY region ORDER BY year, quarter)) / 
        NULLIF(LAG(count) OVER (PARTITION BY region ORDER BY year, quarter), 0), 2) as qoq_growth_rate,
    SUM(count) OVER (PARTITION BY region ORDER BY year, quarter) as cumulative_users,
    CASE
        WHEN ROUND(100.0 * (count - LAG(count) OVER (PARTITION BY region ORDER BY year, quarter)) / 
            NULLIF(LAG(count) OVER (PARTITION BY region ORDER BY year, quarter), 0), 2) > 25 THEN 'RAPID_GROWTH'
        WHEN ROUND(100.0 * (count - LAG(count) OVER (PARTITION BY region ORDER BY year, quarter)) / 
            NULLIF(LAG(count) OVER (PARTITION BY region ORDER BY year, quarter), 0), 2) > 5 THEN 'STEADY_GROWTH'
        ELSE 'STAGNANT'
    END as growth_stage
FROM fact_aggregated_user
WHERE level = 'state'
ORDER BY year DESC, quarter DESC, state;

-- Query 5.2: Top Growth States Classification & Rankings
SELECT 
    region as state,
    SUM(CASE WHEN quarter = 1 THEN count ELSE 0 END) as baseline_users,
    SUM(CASE WHEN quarter = 4 THEN count ELSE 0 END) as current_users,
    ROUND(100.0 * (SUM(CASE WHEN quarter = 4 THEN count ELSE 0 END) - 
        SUM(CASE WHEN quarter = 1 THEN count ELSE 0 END)) / 
        NULLIF(SUM(CASE WHEN quarter = 1 THEN count ELSE 0 END), 0), 2) as annual_growth_rate,
    CASE
        WHEN ROUND(100.0 * (SUM(CASE WHEN quarter = 4 THEN count ELSE 0 END) - 
            SUM(CASE WHEN quarter = 1 THEN count ELSE 0 END)) / 
            NULLIF(SUM(CASE WHEN quarter = 1 THEN count ELSE 0 END), 0), 2) >= 50 THEN 'TIER1_HYPER_GROWTH_50PLUS'
        WHEN ROUND(100.0 * (SUM(CASE WHEN quarter = 4 THEN count ELSE 0 END) - 
            SUM(CASE WHEN quarter = 1 THEN count ELSE 0 END)) / 
            NULLIF(SUM(CASE WHEN quarter = 1 THEN count ELSE 0 END), 0), 2) >= 20 THEN 'TIER2_STRONG_GROWTH_20_50'
        ELSE 'TIER3_MODEST_GROWTH_0_20'
    END as growth_tier
FROM fact_aggregated_user
WHERE level = 'state' AND year >= (SELECT MAX(year) - 1 FROM fact_aggregated_user)
GROUP BY region
ORDER BY annual_growth_rate DESC;

-- Query 5.3: User Base Size & Growth Segmentation
SELECT 
    region as state,
    SUM(count) as total_users,
    COUNT(DISTINCT year) as years_active,
    COUNT(DISTINCT quarter) as quarters_active,
    ROUND(AVG(count), 0) as avg_quarterly_users,
    MAX(count) as peak_users,
    MIN(count) as minimum_users,
    ROUND(100.0 * (MAX(count) - MIN(count)) / NULLIF(MIN(count), 0), 2) as lifetime_growth_pct,
    CASE
        WHEN SUM(count) > 5000000 THEN 'SEGMENT_A_MAJOR_MARKETS (>5M)'
        WHEN SUM(count) > 1000000 THEN 'SEGMENT_B_GROWTH_MARKETS (1-5M)'
        WHEN SUM(count) > 100000 THEN 'SEGMENT_C_EMERGING (100K-1M)'
        ELSE 'SEGMENT_D_STARTUP (<100K)'
    END as market_segment
FROM fact_aggregated_user
WHERE level = 'state'
GROUP BY region
ORDER BY total_users DESC;

-- Query 5.4: Seasonal Engagement Patterns (Quarterly Comparison)
SELECT 
    quarter,
    SUM(count) as total_q_users,
    COUNT(DISTINCT region) as states_active,
    ROUND(AVG(count), 0) as avg_state_users,
    ROUND(100.0 * SUM(count) / (SELECT MAX(quarterly_total) FROM (SELECT SUM(count) as quarterly_total FROM fact_aggregated_user WHERE level = 'state' GROUP BY quarter)), 2) as seasonal_index,
    CASE
        WHEN ROUND(100.0 * SUM(count) / (SELECT AVG(total_quarterly) FROM (SELECT SUM(count) as total_quarterly FROM fact_aggregated_user WHERE level = 'state' GROUP BY quarter)), 2) > 110 THEN 'PEAK_SEASON'
        WHEN ROUND(100.0 * SUM(count) / (SELECT AVG(total_quarterly) FROM (SELECT SUM(count) as total_quarterly FROM fact_aggregated_user WHERE level = 'state' GROUP BY quarter)), 2) < 90 THEN 'OFF_SEASON'
        ELSE 'NORMAL_SEASON'
    END as seasonal_classification
FROM fact_aggregated_user
WHERE level = 'state'
GROUP BY quarter
ORDER BY quarter;

-- Query 5.5: User Engagement Score & Segmentation (Latest Year)
SELECT 
    region as state,
    SUM(count) as total_users,
    COUNT(DISTINCT device) as active_device_types,
    CASE
        WHEN SUM(count) > 5000000 THEN 'SEGMENT_A_SUPER_ENGAGED (>5M)'
        WHEN SUM(count) > 1000000 THEN 'SEGMENT_B_HIGHLY_ENGAGED (1-5M)'
        WHEN SUM(count) > 100000 THEN 'SEGMENT_C_MODERATELY_ENGAGED (100K-1M)'
        WHEN SUM(count) > 10000 THEN 'SEGMENT_D_LOW_ENGAGED (10K-100K)'
        ELSE 'SEGMENT_E_DORMANT (<10K)'
    END as engagement_segment,
    CASE
        WHEN SUM(count) > 5000000 THEN 'LARGE_USER_BASE'
        WHEN SUM(count) > 1000000 THEN 'MEDIUM_USER_BASE'
        ELSE 'SMALL_USER_BASE'
    END as user_base_tier,
    CASE
        WHEN SUM(count) < 100000 THEN 'AT_RISK_CHURN'
        WHEN SUM(count) < 1000000 THEN 'CHURN_PREVENTION_NEEDED'
        ELSE 'HEALTHY_ENGAGEMENT'
    END as engagement_health_status,
    ROW_NUMBER() OVER (ORDER BY SUM(count) DESC) as state_ranking
FROM fact_aggregated_user
WHERE level = 'state' AND year = (SELECT MAX(year) FROM fact_aggregated_user)
GROUP BY region
ORDER BY total_users DESC;
