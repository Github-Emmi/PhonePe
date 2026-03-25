"""
PhonePe Transaction Insights - ETL Pipeline
Phase 3: ETL Pipeline Development

This package contains all ETL modules for data loading, transformation,
aggregation, and database operations.

Modules:
  - data_loader.py: Load data from CSV/JSON files
  - data_transformer.py: Clean and standardize data
  - data_aggregator.py: Compute metrics and aggregations
  - database_loader.py: Database operations and insertions
  - pipeline_orchestrator.py: Main ETL pipeline orchestration

Version: 1.0
"""

from .data_loader import DataLoader
from .data_transformer import DataTransformer
from .data_aggregator import DataAggregator
from .database_loader import DatabaseLoader
from .pipeline_orchestrator import ETLPipeline

__all__ = [
    'DataLoader',
    'DataTransformer',
    'DataAggregator',
    'DatabaseLoader',
    'ETLPipeline'
]

__version__ = '1.0'
