from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import uvicorn
from database_connector import DatabaseConnector
from web_scraper import WebScraper
from ai_processor import AIProcessor
from data_validator import DataValidator
import logging

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
db = None
web_scraper = WebScraper()
ai_processor = AIProcessor()
data_validator = DataValidator()

class ProductRequest(BaseModel):
    supplier_name: str
    product_name: str
    table_name: str = "supplier_products"

@app.on_event("startup")
async def startup_event():
    global db
    try:
        db = DatabaseConnector()
    except Exception as e:
        logging.error(f"Failed to initialize database connection: {e}")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/data/{table_name}")
async def get_table_data(table_name: str):
    try:
        if not db:
            raise HTTPException(status_code=503, detail="Database connection not available")
        data = db.get_table_data(table_name)
        return {"data": data.to_dict('records')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-entry")
async def generate_entry(request: ProductRequest):
    try:
        if not db:
            raise HTTPException(status_code=503, detail="Database connection not available")

        # Get existing data
        existing_data = db.get_table_data(request.table_name)

        # Scrape web data
        scraped_info = web_scraper.search_product_info(
            request.supplier_name,
            request.product_name
        )

        # Get questions from existing data
        questions = existing_data.columns.tolist()

        # Generate AI responses
        ai_responses = ai_processor.analyze_product_data(
            existing_data.to_dict('records'),
            scraped_info['content'],
            questions
        )

        # Validate responses
        validation_result = ai_processor.validate_ai_responses(
            ai_responses,
            questions
        )

        if validation_result['is_valid']:
            # Prepare data for insertion
            new_data = {
                'supplier_name': request.supplier_name,
                'product_name': request.product_name,
                **ai_responses
            }

            # Validate data
            data_validator.validate_data_format(new_data)
            data_validator.validate_unique_entry(new_data, existing_data)

            # Insert into database
            db.insert_ai_generated_row(
                request.table_name,
                new_data
            )

            return {"status": "success", "message": "Entry generated and inserted successfully"}
        else:
            return {
                "status": "error",
                "message": "Generated data failed validation",
                "validation_details": validation_result
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)