# Social Media Account Data API

## Overview
This project is a take-home assessment designed to demonstrate skills in Data Engineering, Analytics, and API development. The application processes and normalizes social media account data, ingests it into a database, and provides queryable endpoints.

## Tools & Libraries Used
- **Python 3.11**
- **FastAPI** (for API development)
- **SQLite** (for database storage)
- **SQLAlchemy** (ORM for database interaction)
- **Pandas** (for data transformation)
- **Uvicorn** (for running the FastAPI server)
- **Docker** (for containerization)
- **pytest & unittest** (for API testing)

## Project Architecture
- **Data Ingestion**: Processes and inserts raw Parquet data into the database.
- **Database**: SQLite-based relational model following 3NF principles.
- **API Endpoints**: Provides access to social media account data.
- **Testing Suite**: Ensures the correctness of API endpoints.
- **Docker Integration**: Facilitates easy setup and deployment.

## Database Model
The database follows **Third Normal Form (3NF)** to ensure data integrity and avoid redundancy. The key entities:

- **Account**: Represents a social media account.
- **Category**: Stores category names.
- **AccountCategory**: Many-to-many relationship between accounts and categories.
- **Historical**: Tracks subscriber count over time.

### Entity Relationship Diagram (ERD)
*(Include an ERD image if possible)*


## Setup & Running the Application

### Local Setup
1. Clone the repository:
   ```sh
    git clone https://github.com/your-repo.git
    cd your-repo
    ```

2. Install dependencies::
    ```sh
    pip install -r requirements.txt
    ```

3. Run the FastAPI application:
    ```sh
    uvicorn src.main:app --reload
    ```

### 🐳 Running with Docker
1.  Build the Docker container:
    ```sh
    docker build -t my-fastapi-app .
    ```

2. Run the application:
    ```sh
    docker run -p 8000:8000 my-fastapi-app
    ```

## API Endpoints

FastAPI automatically generates interactive API documentation.
You can access it at:

Swagger UI: http://127.0.0.1:8000/docs#/ 

*You need the API to be running.

## Running Test

Run unit tests with:
    ```
    docker run -p 8000:8000 my-fastapi-app
    ```
## Explanation of Design Choices

#### Why SQLite?
- Lightweight & Easy to Set Up: No need for external database servers.
- Great for Prototyping: Quick schema validation before scaling.
- Supported by SQLAlchemy: Seamless integration with ORM.

#### Why FastAPI?
- High Performance: Uses ASGI for speed.
- Auto-generated OpenAPI Documentation.
- Dependency Injection for Database Sessions.

#### Why 3NF Normalization?
- Avoids data redundancy.
- Ensures data consistency.
- Optimizes query performance.

## Future Improvements

#### Migrate to PostgreSQL
- Scalability: Supports larger datasets.
- Indexing & Performance Optimizations.

Explore DuckDB for Analytical Queries
- Optimized for Columnar Storage.
- Great for Fast Aggregations.

Database Optimizations
- Indexing strategies for faster queries.
- Sharding & Replication if migrating to PostgreSQL.
- Partitioning large tables for performance gains.

Deploy on Cloud
- Use AWS Lambda or Google Cloud Run for serverless deployment.