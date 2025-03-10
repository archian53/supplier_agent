import snowflake.connector
import pandas as pd
from logger_config import logger
import os

class SnowflakeConnector:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        try:
            # Log credential presence (not the actual values)
            required_vars = [
                'SNOWFLAKE_USER', 'SNOWFLAKE_PASSWORD', 'SNOWFLAKE_ACCOUNT',
                'SNOWFLAKE_WAREHOUSE', 'SNOWFLAKE_DATABASE', 'SNOWFLAKE_SCHEMA'
            ]

            missing_vars = [var for var in required_vars if not os.getenv(var)]
            if missing_vars:
                logger.error(f"Missing required Snowflake credentials: {', '.join(missing_vars)}")
                return

            logger.info("All required Snowflake credentials are present")

            self.conn = snowflake.connector.connect(
                user=os.getenv('SNOWFLAKE_USER'),
                password=os.getenv('SNOWFLAKE_PASSWORD'),
                account=os.getenv('SNOWFLAKE_ACCOUNT'),
                warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
                database=os.getenv('SNOWFLAKE_DATABASE'),
                schema=os.getenv('SNOWFLAKE_SCHEMA')
            )
            logger.info("Successfully connected to Snowflake")
        except Exception as e:
            logger.error(f"Failed to connect to Snowflake: {str(e)}")
            raise

    def get_table_data(self, table_name):
        try:
            if not self.conn:
                logger.error("No Snowflake connection available")
                raise Exception("Snowflake connection not established")

            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, self.conn)
            return df
        except Exception as e:
            logger.error(f"Error fetching data from table {table_name}: {str(e)}")
            raise

    def insert_ai_generated_row(self, table_name, data_dict):
        try:
            if not self.conn:
                logger.error("No Snowflake connection available")
                raise Exception("Snowflake connection not established")

            columns = ', '.join(data_dict.keys())
            placeholders = ', '.join(['%s'] * len(data_dict))
            values = tuple(data_dict.values())

            query = f"""
                INSERT INTO {table_name} ({columns})
                VALUES ({placeholders})
            """

            cursor = self.conn.cursor()
            cursor.execute(query, values)
            self.conn.commit()
            cursor.close()

            logger.info(f"Successfully inserted AI generated row into {table_name}")
        except Exception as e:
            logger.error(f"Error inserting data into table {table_name}: {str(e)}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("Snowflake connection closed")