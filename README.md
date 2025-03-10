# AI-Powered Data Analysis System

A web application that combines React frontend with FastAPI backend for AI-powered data analysis and entry system.

## Features

- React-based frontend with Material-UI components
- FastAPI backend with PostgreSQL database
- AI-powered data analysis using OpenAI GPT-4
- Web scraping capabilities for data enrichment
- Data validation and processing pipeline

## Setup

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL database

### Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
OPENAI_API_KEY=your_openai_api_key
```

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install frontend dependencies:
```bash
cd frontend
npm install
```

### Running the Application

1. Start the backend server:
```bash
uvicorn main:app --host 0.0.0.0 --port 5000
```

2. Start the frontend development server:
```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Project Structure

```
├── frontend/           # React frontend application
│   ├── src/           # Source files
│   └── public/        # Static files
├── main.py            # FastAPI backend application
├── database_connector.py  # Database connection handling
├── web_scraper.py     # Web scraping utilities
├── ai_processor.py    # AI processing logic
└── data_validator.py  # Data validation utilities
```
