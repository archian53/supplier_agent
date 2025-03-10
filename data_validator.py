from logger_config import logger
import pandas as pd
import re

class DataValidator:
    def __init__(self):
        self.required_fields = [
            'supplier_name',
            'product_name',
            'creation_date'
        ]
        
    def validate_data_format(self, data_dict):
        try:
            # Check required fields
            missing_fields = [field for field in self.required_fields if field not in data_dict]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            # Validate data types
            self._validate_data_types(data_dict)
            
            # Validate AI tags
            self._validate_ai_tags(data_dict)
            
            logger.info("Data validation passed successfully")
            return True
        except Exception as e:
            logger.error(f"Data validation failed: {str(e)}")
            raise

    def _validate_data_types(self, data_dict):
        # Add specific data type validations
        if not isinstance(data_dict.get('supplier_name'), str):
            raise ValueError("supplier_name must be a string")
        
        if not isinstance(data_dict.get('product_name'), str):
            raise ValueError("product_name must be a string")

    def _validate_ai_tags(self, data_dict):
        # Ensure AI generated tag is present where needed
        for key, value in data_dict.items():
            if isinstance(value, str) and not value.endswith("[AI generated]"):
                data_dict[key] = f"{value} [AI generated]"

    def validate_unique_entry(self, new_data, existing_data):
        try:
            # Check if combination of supplier and product already exists
            existing_combinations = existing_data[['supplier_name', 'product_name']].values.tolist()
            new_combination = [new_data['supplier_name'], new_data['product_name']]
            
            if new_combination in existing_combinations:
                raise ValueError("This supplier and product combination already exists")
            
            return True
        except Exception as e:
            logger.error(f"Uniqueness validation failed: {str(e)}")
            raise
