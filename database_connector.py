import os
import pandas as pd
from sqlalchemy import create_engine, text
from logger_config import logger

class DatabaseConnector:
    def __init__(self):
        self.engine = None
        self.connect()

    def connect(self):
        try:
            database_url = os.getenv('DATABASE_URL')
            if not database_url:
                raise ValueError("DATABASE_URL environment variable is not set")
            
            self.engine = create_engine(database_url)
            
            # Create table if it doesn't exist
            self._create_table()
            logger.info("Successfully connected to database")
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise

    def _create_table(self):
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS supplier_products (
                id SERIAL PRIMARY KEY,
                supplier_name VARCHAR(255) NOT NULL,
                product_name VARCHAR(255) NOT NULL,
                creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(supplier_name, product_name)
            )
            """
            with self.engine.connect() as conn:
                conn.execute(text(create_table_query))
                conn.commit()
            logger.info("Table created/verified successfully")
        except Exception as e:
            logger.error(f"Error creating table: {str(e)}")
            raise

    def get_table_data(self, table_name):
        try:
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, self.engine)
            return df
        except Exception as e:
            logger.error(f"Error fetching data from table {table_name}: {str(e)}")
            raise

    def insert_ai_generated_row(self, table_name, data_dict):
        try:
            columns = ', '.join(data_dict.keys())
            placeholders = ', '.join([':' + key for key in data_dict.keys()])
            
            query = f"""
                INSERT INTO {table_name} ({columns})
                VALUES ({placeholders})
            """
            
            with self.engine.connect() as conn:
                conn.execute(text(query), data_dict)
                conn.commit()
            
            logger.info(f"Successfully inserted AI generated row into {table_name}")
        except Exception as e:
            logger.error(f"Error inserting data into table {table_name}: {str(e)}")
            raise
