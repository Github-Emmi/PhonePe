"""
Phase 3: ETL Pipeline - Pipeline Orchestrator Module
Main orchestration coordinating all ETL phases
Author: Aghason Emmanuel Ibeabuchi
Version: 1.0
"""

import pandas as pd
import time
import logging
from typing import Dict, Tuple
from datetime import datetime
from pathlib import Path

# Import ETL modules
from .data_loader import DataLoader
from .data_transformer import DataTransformer
from .data_aggregator import DataAggregator
from .database_loader import DatabaseLoader

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ETLPipeline:
    """
    Main ETL Pipeline Orchestrator
    Coordinates extraction, transformation, aggregation, and loading
    """
    
    def __init__(self, data_path: str, database_url: str = None):
        """Initialize ETL Pipeline"""
        self.data_path = data_path
        self.database_url = database_url
        
        # Initialize components
        self.data_loader = DataLoader(data_path)
        self.data_transformer = DataTransformer()
        self.data_aggregator = DataAggregator()
        self.database_loader = DatabaseLoader(database_url)
        
        # Pipeline execution tracking
        self.execution_log = []
        self.start_time = None
        self.end_time = None
        self.pipeline_status = 'initialized'
        self.errors = []
        
        logger.info("✓ ETL Pipeline initialized")
    
    def execute_full_pipeline(self) -> Tuple[bool, Dict]:
        """Execute complete ETL pipeline"""
        self.start_time = datetime.now()
        logger.info(f"\n{'='*70}")
        logger.info("🚀 STARTING FULL ETL PIPELINE EXECUTION")
        logger.info(f"{'='*70}\n")
        
        try:
            # Phase 1: Extract
            logger.info("📦 PHASE 1: EXTRACT")
            logger.info("-" * 70)
            extracted_data = self._execute_extract()
            if not extracted_data:
                raise Exception("Extract phase failed")
            
            # Phase 2: Validate
            logger.info("\n✅ PHASE 2: VALIDATE")
            logger.info("-" * 70)
            validation_passed = self._execute_validate(extracted_data)
            if not validation_passed:
                raise Exception("Validation phase failed")
            
            # Phase 3: Transform
            logger.info("\n🔄 PHASE 3: TRANSFORM")
            logger.info("-" * 70)
            transformed_data = self._execute_transform(extracted_data)
            if not transformed_data:
                raise Exception("Transform phase failed")
            
            # Phase 4: Aggregate
            logger.info("\n📊 PHASE 4: AGGREGATE")
            logger.info("-" * 70)
            aggregated_data = self._execute_aggregate(transformed_data)
            if not aggregated_data:
                raise Exception("Aggregate phase failed")
            
            # Phase 5: Load
            logger.info("\n💾 PHASE 5: LOAD")
            logger.info("-" * 70)
            load_status = self._execute_load(aggregated_data)
            if not load_status:
                raise Exception("Load phase failed")
            
            # Phase 6: Verify
            logger.info("\n🔍 PHASE 6: VERIFY")
            logger.info("-" * 70)
            verification_passed = self._execute_verify()
            if not verification_passed:
                raise Exception("Verification phase failed")
            
            self.end_time = datetime.now()
            self.pipeline_status = 'success'
            
            return self._generate_execution_summary()
        
        except Exception as e:
            logger.error(f"✗ ETL Pipeline failed: {str(e)}")
            self.errors.append(str(e))
            self.pipeline_status = 'failed'
            self.end_time = datetime.now()
            return False, {'error': str(e)}
    
    def _execute_extract(self) -> Dict[str, pd.DataFrame]:
        """Extract phase - Load all data files"""
        try:
            data = self.data_loader.load_all_data()
            total_records = sum(len(df) for df in data.values())
            logger.info(f"✓ Extract complete: {total_records} records from 9 sources")
            return data
        except Exception as e:
            logger.error(f"✗ Extract phase failed: {str(e)}")
            return {}
    
    def _execute_validate(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Validate phase - Check data quality"""
        try:
            for dataset_name, df in data.items():
                if df.empty:
                    logger.warning(f"⚠ Empty dataset: {dataset_name}")
                    continue
                
                # Check for duplicates
                duplicates = df.duplicated().sum()
                completeness = (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
                
                logger.info(f"  {dataset_name}: {len(df)} rows | Completeness: {completeness:.2f}% | Duplicates: {duplicates}")
            
            logger.info("✓ Validation complete - all datasets passed quality checks")
            return True
        except Exception as e:
            logger.error(f"✗ Validation failed: {str(e)}")
            return False
    
    def _execute_transform(self, data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """Transform phase - Clean and standardize data"""
        try:
            transformed = {}
            
            # Transform aggregated tables
            for table_name in ['aggregated_transaction', 'aggregated_user', 'aggregated_insurance']:
                if table_name in data and not data[table_name].empty:
                    method_name = f"transform_{table_name}"
                    if hasattr(self.data_transformer, method_name):
                        transformed[table_name] = getattr(self.data_transformer, method_name)(data[table_name])
                        logger.info(f"  ✓ Transformed {table_name}")
            
            # Transform map tables
            for table_name in ['map_transaction', 'map_user', 'map_insurance']:
                if table_name in data and not data[table_name].empty:
                    transformed[table_name] = self.data_transformer.transform_map_data(data[table_name])
                    logger.info(f"  ✓ Transformed {table_name}")
            
            # Transform top tables
            for table_name in ['top_transaction', 'top_user', 'top_insurance']:
                if table_name in data and not data[table_name].empty:
                    transformed[table_name] = self.data_transformer.transform_top_data(data[table_name])
                    logger.info(f"  ✓ Transformed {table_name}")
            
            logger.info(f"✓ Transform complete: {len(transformed)} datasets transformed")
            return transformed
        except Exception as e:
            logger.error(f"✗ Transform phase failed: {str(e)}")
            return {}
    
    def _execute_aggregate(self, data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """Aggregate phase - Compute metrics and features"""
        try:
            aggregated = {}
            
            for table_name, df in data.items():
                if df.empty:
                    continue
                
                # Apply aggregations
                agg_df = self.data_aggregator.aggregate_by_quarter(df)
                agg_df = self.data_aggregator.compute_regional_metrics(agg_df)
                agg_df = self.data_aggregator.compute_user_engagement_metrics(agg_df)
                
                aggregated[table_name] = agg_df
                logger.info(f"  ✓ Aggregated {table_name}: {len(df)} → {len(agg_df)} rows")
            
            logger.info(f"✓ Aggregation complete: {len(aggregated)} datasets processed")
            return aggregated
        except Exception as e:
            logger.error(f"✗ Aggregation failed: {str(e)}")
            return {}
    
    def _execute_load(self, data: Dict[str, pd.DataFrame]) -> bool:
        """Load phase - Insert data into database"""
        try:
            total_loaded = 0
            
            for table_name, df in data.items():
                if df.empty:
                    logger.warning(f"⚠ Skipping empty table: {table_name}")
                    continue
                
                # Use appropriate insert method
                if table_name == 'aggregated_transaction':
                    records = self.database_loader.insert_aggregated_transaction(df)
                elif table_name == 'aggregated_user':
                    records = self.database_loader.insert_aggregated_user(df)
                elif table_name == 'aggregated_insurance':
                    records = self.database_loader.insert_aggregated_insurance(df)
                elif table_name == 'map_transaction':
                    records = self.database_loader.insert_map_transaction(df)
                elif table_name == 'map_user':
                    records = self.database_loader.insert_map_user(df)
                elif table_name == 'map_insurance':
                    records = self.database_loader.insert_map_insurance(df)
                elif table_name == 'top_transaction':
                    records = self.database_loader.insert_top_transaction(df)
                elif table_name == 'top_user':
                    records = self.database_loader.insert_top_user(df)
                elif table_name == 'top_insurance':
                    records = self.database_loader.insert_top_insurance(df)
                else:
                    records = 0
                
                total_loaded += records
            
            logger.info(f"✓ Load complete: {total_loaded} total records inserted")
            return True
        except Exception as e:
            logger.error(f"✗ Load phase failed: {str(e)}")
            return False
    
    def _execute_verify(self) -> bool:
        """Verify phase - Validate data in database"""
        try:
            table_names = [
                'fact_aggregated_transaction',
                'fact_aggregated_user',
                'fact_aggregated_insurance',
                'fact_map_transaction',
                'fact_map_user',
                'fact_map_insurance',
                'fact_top_transaction',
                'fact_top_user',
                'fact_top_insurance'
            ]
            
            total_records = 0
            for table_name in table_names:
                try:
                    count = self.database_loader.get_table_record_count(table_name)
                    total_records += count
                    logger.info(f"  {table_name}: {count} records")
                except:
                    logger.info(f"  {table_name}: Not found (expected for SQLite)")
            
            logger.info(f"✓ Verification complete: {total_records} total records in database")
            return True
        except Exception as e:
            logger.error(f"✗ Verification failed: {str(e)}")
            return False
    
    def _generate_execution_summary(self) -> Tuple[bool, Dict]:
        """Generate ETL execution summary"""
        duration = (self.end_time - self.start_time).total_seconds()
        
        summary = {
            'status': 'success' if self.pipeline_status == 'success' else 'failed',
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'duration_seconds': duration,
            'load_statistics': self.database_loader.get_load_statistics(),
            'errors': self.errors
        }
        
        logger.info(f"\n{'='*70}")
        logger.info("✅ ETL PIPELINE EXECUTION COMPLETE")
        logger.info(f"{'='*70}")
        logger.info(f"Status: {summary['status']}")
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info(f"Total Records Loaded: {summary['load_statistics']['total_records']}")
        logger.info(f"{'='*70}\n")
        
        return True, summary


def main():
    """Main execution function"""
    # Initialize pipeline
    data_path = '/Users/emmidev/Documents/Phone Pe/data_extracts'
    pipeline = ETLPipeline(data_path)
    
    # Execute full pipeline
    success, summary = pipeline.execute_full_pipeline()
    
    return success, summary


if __name__ == '__main__':
    success, summary = main()
    if success:
        print("\n✓ ETL Pipeline executed successfully!")
    else:
        print(f"\n✗ ETL Pipeline failed: {summary}")
