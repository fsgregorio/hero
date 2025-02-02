"""
API module for querying social media account data.

This FastAPI application provides endpoints to:
- Retrieve accounts by category.
- Retrieve accounts with over 1 million followers.
- Identify accounts with significant subscriber growth in the last 30 days.
- Upload new account data for ingestion.
"""

from fastapi import FastAPI, Depends, HTTPException, Query, File, UploadFile
import shutil
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from .database import SessionLocal
from .models import Account, Category, AccountCategory, Historical
from .ingestion import ingest_data
import pandas as pd
from datetime import datetime, timedelta

app = FastAPI()

def get_db():
    """
    Dependency to provide a database session.
    Ensures proper connection management.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/accounts/category/{category_name}")
def get_accounts_by_category(
    category_name: str, 
    db: Session = Depends(get_db), 
    offset: int = Query(0, alias="offset"),
    limit: int = Query(10, alias="limit")
):
    """
    Retrieve accounts belonging to a specific category.
    
    :param category_name: Name of the category.
    :param db: Database session dependency.
    :param offset: Pagination offset.
    :param limit: Number of results to return.
    """
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    account_ids = db.query(AccountCategory.account_id).filter(AccountCategory.category_id == category.id).all()
    accounts = (
        db.query(Account)
        .filter(Account.account_id.in_([acc[0] for acc in account_ids]))
        .offset(offset)
        .limit(limit)
        .all()
    )
    
    return {"category": category_name, "accounts": [account.account_id for account in accounts]}

@app.get("/accounts/million-plus")
def get_large_accounts(
    db: Session = Depends(get_db),
    offset: int = Query(0, alias="offset"),
    limit: int = Query(10, alias="limit")
):
    """
    Retrieve accounts with over 1 million followers.
    
    :param db: Database session dependency.
    :param offset: Pagination offset.
    :param limit: Number of results to return.
    """
    accounts = (
        db.query(Account)
        .join(Historical)
        .filter(Historical.subscriber_count > 1_000_000)
        .distinct()
        .offset(offset)
        .limit(limit)
        .all()
    )
    return {"accounts": [account.account_id for account in accounts]}

@app.get("/accounts/growth")
def get_high_growth_accounts(
    db: Session = Depends(get_db),
    offset: int = Query(0, alias="offset"),
    limit: int = Query(10, alias="limit")
):
    """
    Retrieve accounts with over 10% subscriber growth in the last 30 days.
    
    :param db: Database session dependency.
    :param offset: Pagination offset.
    :param limit: Number of results to return.
    """
    max_date_query = text("SELECT MAX(date) FROM historical")
    max_date_value = db.execute(max_date_query).scalar()
    if not max_date_value:
        return {"message": "No data found"}
    max_date = max_date_value if isinstance(max_date_value, datetime) else datetime.fromisoformat(max_date_value)
    analysis_window = max_date - timedelta(days=30)
    
    recent_entries_query = text("""
        SELECT account_id, subscriber_count, date
        FROM historical
        WHERE date > :analysis_window
    """)
    recent_entries = pd.read_sql(
        recent_entries_query,
        db.bind,
        params={"analysis_window": analysis_window.isoformat()}
    )
    if recent_entries.empty:
        return {"message": "No recent data found"}
    
    sorted_records = recent_entries.sort_values(by=["account_id", "date"])
    initial_snapshot = (
        sorted_records.drop_duplicates(subset=["account_id"], keep="first")
        [["account_id", "subscriber_count"]]
        .rename(columns={"subscriber_count": "baseline_subscribers"})
    )
    latest_snapshot = (
        sorted_records.drop_duplicates(subset=["account_id"], keep="last")
        [["account_id", "subscriber_count"]]
        .rename(columns={"subscriber_count": "current_subscribers"})
    )
    trend_data = initial_snapshot.merge(latest_snapshot, on="account_id", how="inner")
    trend_data["growth_percentage"] = ((trend_data["current_subscribers"] - trend_data["baseline_subscribers"]) / trend_data["baseline_subscribers"] * 100).round(2)
    high_growth_accounts = trend_data[trend_data["growth_percentage"] > 10.]
    paginated_results = high_growth_accounts.iloc[offset:offset+limit]
    return {"high_growth_accounts": paginated_results.to_dict(orient="records")}

@app.post("/accounts/upload")
async def upload_new_accounts(file: UploadFile = File(...)):
    """
    Uploads a new account data file and triggers ingestion.
    
    :param file: Uploaded file containing new account data.
    """
    file_path = f"data/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        ingest_data(file_path)
    except Exception as e:
        return {"error": f"Error processing file: {e}"}
    return {"message": f"File {file.filename} successfully uploaded and processed!"}