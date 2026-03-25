-- PhonePe Transaction Insights Database (PostgreSQL)
-- Phase 2: Database Setup & Data Modeling
-- Generated: 2026-03-24T18:25:44.587977


-- Table: fact_aggregated_transaction
CREATE TABLE IF NOT EXISTS fact_aggregated_transaction (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    -- ... (convert remaining columns from MySQL DDL)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: fact_aggregated_user
CREATE TABLE IF NOT EXISTS fact_aggregated_user (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    -- ... (convert remaining columns from MySQL DDL)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: fact_aggregated_insurance
CREATE TABLE IF NOT EXISTS fact_aggregated_insurance (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    -- ... (convert remaining columns from MySQL DDL)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: fact_map_transaction
CREATE TABLE IF NOT EXISTS fact_map_transaction (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    -- ... (convert remaining columns from MySQL DDL)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: fact_map_user
CREATE TABLE IF NOT EXISTS fact_map_user (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    -- ... (convert remaining columns from MySQL DDL)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: fact_map_insurance
CREATE TABLE IF NOT EXISTS fact_map_insurance (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    -- ... (convert remaining columns from MySQL DDL)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: fact_top_transaction
CREATE TABLE IF NOT EXISTS fact_top_transaction (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    -- ... (convert remaining columns from MySQL DDL)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: fact_top_user
CREATE TABLE IF NOT EXISTS fact_top_user (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    -- ... (convert remaining columns from MySQL DDL)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: fact_top_insurance
CREATE TABLE IF NOT EXISTS fact_top_insurance (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    -- ... (convert remaining columns from MySQL DDL)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
