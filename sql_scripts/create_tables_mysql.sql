-- PhonePe Transaction Insights Database
-- Phase 2: Database Setup & Data Modeling
-- Generated: 2026-03-24T18:25:44.567543

-- Create database
CREATE DATABASE IF NOT EXISTS phonpe_analytics;
USE phonpe_analytics;


-- Table: fact_aggregated_transaction

CREATE TABLE IF NOT EXISTS fact_aggregated_transaction (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    year INT NOT NULL,
    quarter INT NOT NULL,
    level VARCHAR(50) NOT NULL,
    region VARCHAR(100),
    category VARCHAR(50),
    type VARCHAR(50),
    count BIGINT NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_year_quarter_level (year, quarter, level),
    INDEX idx_region (region),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: fact_aggregated_user

CREATE TABLE IF NOT EXISTS fact_aggregated_user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    year INT NOT NULL,
    quarter INT NOT NULL,
    level VARCHAR(50) NOT NULL,
    region VARCHAR(100),
    device VARCHAR(100) NOT NULL,
    count BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_year_quarter_level (year, quarter, level),
    INDEX idx_device (device)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: fact_aggregated_insurance

CREATE TABLE IF NOT EXISTS fact_aggregated_insurance (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    year INT NOT NULL,
    quarter INT NOT NULL,
    level VARCHAR(50) NOT NULL,
    region VARCHAR(100),
    category VARCHAR(50),
    type VARCHAR(50),
    count BIGINT NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_year_quarter_level (year, quarter, level),
    INDEX idx_region (region)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: fact_map_transaction

CREATE TABLE IF NOT EXISTS fact_map_transaction (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    year INT NOT NULL,
    quarter INT NOT NULL,
    level VARCHAR(50) NOT NULL,
    region VARCHAR(100),
    type VARCHAR(50),
    count BIGINT NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_year_quarter (year, quarter),
    INDEX idx_region (region)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: fact_map_user

CREATE TABLE IF NOT EXISTS fact_map_user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    year INT NOT NULL,
    quarter INT NOT NULL,
    level VARCHAR(50) NOT NULL,
    region VARCHAR(100),
    registered_users BIGINT NOT NULL,
    app_opens BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_year_quarter (year, quarter),
    INDEX idx_region (region)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: fact_map_insurance

CREATE TABLE IF NOT EXISTS fact_map_insurance (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    year INT NOT NULL,
    quarter INT NOT NULL,
    level VARCHAR(50) NOT NULL,
    region VARCHAR(100),
    type VARCHAR(50),
    count BIGINT NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_year_quarter (year, quarter),
    INDEX idx_region (region)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: fact_top_transaction

CREATE TABLE IF NOT EXISTS fact_top_transaction (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    year INT NOT NULL,
    quarter INT NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_name VARCHAR(100) NOT NULL,
    rank INT NOT NULL,
    state VARCHAR(100),
    type VARCHAR(50),
    count BIGINT NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_year_quarter (year, quarter),
    INDEX idx_entity_type (entity_type),
    INDEX idx_rank (rank)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: fact_top_user

CREATE TABLE IF NOT EXISTS fact_top_user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    year INT NOT NULL,
    quarter INT NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_name VARCHAR(100) NOT NULL,
    rank INT NOT NULL,
    registered_users BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_year_quarter (year, quarter),
    INDEX idx_entity_type (entity_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Table: fact_top_insurance

CREATE TABLE IF NOT EXISTS fact_top_insurance (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    year INT NOT NULL,
    quarter INT NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_name VARCHAR(100) NOT NULL,
    rank INT NOT NULL,
    state VARCHAR(100),
    type VARCHAR(50),
    count BIGINT NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_year_quarter (year, quarter),
    INDEX idx_entity_type (entity_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

