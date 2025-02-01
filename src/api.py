from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Account, Category, AccountCategory, Historical
from ingestion import ingest_data
import pandas as pd

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/accounts/category/{category_name}")
def get_accounts_by_category(category_name: str, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.name == category_name).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    account_ids = db.query(AccountCategory.account_id).filter(AccountCategory.category_id == category.id).all()
    accounts = db.query(Account).filter(Account.account_id.in_([acc[0] for acc in account_ids])).all()
    
    return {"category": category_name, "accounts": [account.account_id for account in accounts]}

@app.get("/accounts/million-plus")
def get_large_accounts(db: Session = Depends(get_db)):
    accounts = db.query(Account).join(Historical).filter(Historical.subscriber_count > 1_000_000).distinct().all()
    return {"accounts": [account.account_id for account in accounts]}

@app.get("/accounts/growth")
def get_high_growth_accounts(db: Session = Depends(get_db)):
    from datetime import datetime, timedelta
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    
    growth_data = (
        db.query(Historical.account_id, Historical.subscriber_count)
        .filter(Historical.date > one_month_ago)
        .all()
    )
    
    growth_dict = {}
    for account_id, subscriber_count in growth_data:
        if account_id not in growth_dict:
            growth_dict[account_id] = []
        growth_dict[account_id].append(subscriber_count)
    
    high_growth_accounts = []
    for account_id, counts in growth_dict.items():
        if len(counts) > 1 and ((counts[-1] - counts[0]) / counts[0]) * 100 > 10:
            high_growth_accounts.append(account_id)
    
    return {"high_growth_accounts": high_growth_accounts}

@app.post("/accounts/upload")
def upload_new_accounts():
    file_path = "data/add_accounts.parquet"
    ingest_data(file_path)
    return {"message": "New accounts data ingested successfully!"}
