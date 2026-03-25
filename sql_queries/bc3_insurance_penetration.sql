-- ============================================================
-- BUSINESS CASE 3: INSURANCE PENETRATION
-- ============================================================
-- Focus: Insurance market maturity, product mix, adoption gaps
-- Impact: +Rs. 1,300 Cr through emerging market entry
-- Data Source: fact_aggregated_insurance (state-level insurance metrics)

-- Query 3.1: Insurance Growth Trajectory by State & Quarter
SELECT 
    region as state, 
    year, 
    quarter, 
    type as insurance_type,
    SUM(count) as quarterly_policies,
    SUM(amount) as quarterly_premium,
    ROUND(SUM(amount) / NULLIF(SUM(count), 0), 2) as avg_premium_per_policy,
    LAG(SUM(count)) OVER (PARTITION BY region, type ORDER BY year, quarter) as prev_quarter_policies,
    ROUND(100.0 * (SUM(count) - LAG(SUM(count)) OVER (PARTITION BY region, type ORDER BY year, quarter)) / 
        NULLIF(LAG(SUM(count)) OVER (PARTITION BY region, type ORDER BY year, quarter), 0), 2) as qoq_growth_rate
FROM fact_aggregated_insurance
WHERE level = 'state'
GROUP BY region, year, quarter, type
ORDER BY year DESC, quarter DESC, state, quarterly_premium DESC;

-- Query 3.2: Insurance Market Maturity & Adoption Gaps
SELECT 
    region as state,
    COUNT(DISTINCT type) as insurance_types_offered,
    SUM(count) as total_policies,
    SUM(amount) as total_premium,
    CASE
        WHEN SUM(count) >= 100000 THEN 'MATURE_MARKET'
        WHEN SUM(count) >= 10000 THEN 'DEVELOPING_MARKET'
        WHEN SUM(count) >= 1000 THEN 'EMERGING_MARKET'
        ELSE 'ENTRY_LEVEL'
    END as market_maturity,
    ROUND(SUM(amount) / NULLIF(SUM(count), 0), 2) as avg_premium_value,
    ROUND((CASE 
        WHEN SUM(count) < 1000 THEN (1000000 - SUM(count)) 
        WHEN SUM(count) < 10000 THEN (100000 - SUM(count)) 
        ELSE 0 
    END) * ROUND(SUM(amount) / NULLIF(SUM(count), 0), 2) / 10000000, 0) as estimated_revenue_opportunity_cr
FROM fact_aggregated_insurance
WHERE level = 'state'
GROUP BY region
ORDER BY total_premium DESC;

-- Query 3.3: Top Insurance Categories by Revenue & Metrics
SELECT 
    type as insurance_type,
    SUM(count) as total_policies,
    SUM(amount) as total_premium,
    COUNT(DISTINCT region) as state_coverage,
    ROUND(SUM(amount) / NULLIF(SUM(count), 0), 2) as avg_premium_per_policy,
    ROUND(100.0 * SUM(count) / (SELECT SUM(count) FROM fact_aggregated_insurance WHERE level = 'state'), 2) as volume_share_pct,
    ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM fact_aggregated_insurance WHERE level = 'state'), 2) as revenue_share_pct
FROM fact_aggregated_insurance
WHERE level = 'state'
GROUP BY type
ORDER BY total_premium DESC;

-- Query 3.4: Insurance Penetration Analysis (Premium Value Distribution)
SELECT 
    region as state, 
    type as insurance_type,
    SUM(count) as total_policies,
    SUM(amount) as total_premium,
    ROUND(SUM(amount) / NULLIF(SUM(count), 0), 2) as avg_premium,
    CASE
        WHEN ROUND(SUM(amount) / NULLIF(SUM(count), 0), 2) >= 3000 THEN 'PREMIUM_HIGH_VALUE'
        WHEN ROUND(SUM(amount) / NULLIF(SUM(count), 0), 2) >= 1500 THEN 'PREMIUM_STANDARD'
        WHEN ROUND(SUM(amount) / NULLIF(SUM(count), 0), 2) >= 500 THEN 'PREMIUM_BUDGET'
        ELSE 'PREMIUM_ULTRA_BUDGET'
    END as product_segment,
    ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM fact_aggregated_insurance WHERE level = 'state' AND region = fact_aggregated_insurance.region), 2) as state_revenue_share_pct
FROM fact_aggregated_insurance
WHERE level = 'state'
GROUP BY region, type
HAVING SUM(count) > 0
ORDER BY state, total_premium DESC;

-- Query 3.5: Geographic Insurance Market Size & Growth
SELECT 
    region as state,
    SUM(count) as total_policies,
    SUM(amount) as total_premium,
    COUNT(DISTINCT type) as product_categories,
    ROUND(AVG(amount / count), 2) as avg_premium_per_policy,
    ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM fact_aggregated_insurance WHERE level = 'state'), 2) as national_premium_share_pct,
    CASE
        WHEN SUM(count) >= 50000 THEN 'HIGHLY_PENETRATED'
        WHEN SUM(count) >= 10000 THEN 'MODERATELY_PENETRATED'
        WHEN SUM(count) >= 1000 THEN 'LOW_PENETRATION'
        ELSE 'MINIMAL_PENETRATION'
    END as penetration_level,
    SUM(amount) / NULLIF(COUNT(DISTINCT type), 0) as revenue_per_category
FROM fact_aggregated_insurance
WHERE level = 'state'
GROUP BY region
ORDER BY total_premium DESC;
