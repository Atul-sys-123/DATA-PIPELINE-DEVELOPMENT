# etl_automation.py
import pandas as pd
import requests
import yaml
import logging
from sqlalchemy import create_engine
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('etl_pipeline.log'),
        logging.StreamHandler()
    ]
)

class ETLPipeline:
    def __init__(self, config_path):
        self.config = self._load_config(config_path)
        self.source_config = self.config['source']
        self.target_config = self.config['target']
        self.transform_config = self.config.get('transformations', {})

    @staticmethod
    def _load_config(config_path):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logging.error(f"Error loading config file: {str(e)}")
            raise

    def extract(self):
        """Extract data from source"""
        logging.info(f"Extracting data from {self.source_config['type']}")
        
        try:
            if self.source_config['type'] == 'csv':
                return pd.read_csv(self.source_config['path'])
            elif self.source_config['type'] == 'api':
                response = requests.get(self.source_config['url'])
                response.raise_for_status()
                return pd.DataFrame(response.json())
            elif self.source_config['type'] == 'database':
                engine = create_engine(self.source_config['connection_string'])
                return pd.read_sql_table(self.source_config['table'], engine)
            else:
                raise ValueError("Unsupported source type")
        except Exception as e:
            logging.error(f"Extraction failed: {str(e)}")
            raise

    def transform(self, df):
        """Apply data transformations"""
        logging.info("Applying transformations")
        
        # Handle missing values
        if self.transform_config.get('handle_missing_values'):
            for col, strategy in self.transform_config['handle_missing_values'].items():
                if strategy == 'drop':
                    df = df.dropna(subset=[col])
                elif strategy == 'fill':
                    df[col] = df[col].fillna(self.transform_config['fill_values'][col])

        # Remove duplicates
        if self.transform_config.get('remove_duplicates'):
            df = df.drop_duplicates(subset=self.transform_config['remove_duplicates'])

        # Type conversions
        if self.transform_config.get('type_conversions'):
            for col, dtype in self.transform_config['type_conversions'].items():
                df[col] = df[col].astype(dtype)

        # Add audit column
        df['etl_timestamp'] = datetime.now()
        
        return df

    def load(self, df):
        """Load data to destination"""
        logging.info(f"Loading data to {self.target_config['type']}")
        
        try:
            if self.target_config['type'] == 'csv':
                df.to_csv(self.target_config['path'], index=False)
            elif self.target_config['type'] == 'database':
                engine = create_engine(self.target_config['connection_string'])
                df.to_sql(
                    name=self.target_config['table'],
                    con=engine,
                    if_exists=self.target_config.get('if_exists', 'append'),
                    index=False
                )
            else:
                raise ValueError("Unsupported target type")
        except Exception as e:
            logging.error(f"Loading failed: {str(e)}")
            raise

    def validate(self, df):
        """Basic data validation"""
        logging.info("Performing data validation")
        
        if df.empty:
            raise ValueError("Empty dataframe after transformation")
        
        required_columns = self.transform_config.get('required_columns', [])
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        logging.info(f"Data validation passed. Shape: {df.shape}")

    def run(self):
        """Execute ETL pipeline"""
        try:
            # Extract
            raw_data = self.extract()
            
            # Transform
            transformed_data = self.transform(raw_data)
            
            # Validate
            self.validate(transformed_data)
            
            # Load
            self.load(transformed_data)
            
            logging.info("ETL process completed successfully")
        except Exception as e:
            logging.error(f"ETL process failed: {str(e)}")
            raise

if __name__ == "__main__":
    # Example usage
    pipeline = ETLPipeline('etl_config.yaml')
    pipeline.run()

import os

def _load_config(self, config_path):
    """Load configuration from YAML file with existence check"""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {os.path.abspath(config_path)}")
    
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        logging.error(f"Invalid YAML format: {str(e)}")
        raise