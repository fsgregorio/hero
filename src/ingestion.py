"""
Module for ingesting transformed social media account data into the database.

This module loads and processes data to ensure unique accounts, categories, 
and historical records before inserting them efficiently into the database.

Steps:
1. Load and transform raw data.
2. Filter and insert unique accounts.
3. Filter and insert unique categories.
4. Process relationships and historical data.
5. Optimize insertion using caching and bulk inserts.
"""

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .database import SessionLocal, engine
from .models import Account, Category, AccountCategory, Historical
from .transformation import load_and_transform_data

def ingest_data(file_path: str):
    """
    Loads transformed data and inserts it into the database.
    Ensures unique accounts, categories, and avoids duplicating historical data.

    :param file_path: Path to the Parquet file containing raw data.
    """
    print("📌 Loading and transforming data...")
    df = load_and_transform_data(file_path)
    print("✅ Data transformation completed!")
    
    # Remove duplicate accounts and categories before processing
    unique_accounts = df[['account_id']].drop_duplicates()
    unique_categories = df[['categories']].drop_duplicates()
    
    db = SessionLocal()
    
    print("📌 Inserting unique accounts...")
    for _, row in unique_accounts.iterrows():
        if not db.query(Account).filter_by(account_id=row['account_id']).first():
            db.add(Account(account_id=row['account_id']))
    print("✅ Unique accounts inserted!")
    
    print("📌 Inserting unique categories...")
    for _, row in unique_categories.iterrows():
        if not db.query(Category).filter_by(name=row['categories']).first():
            db.add(Category(name=row['categories']))
    print("✅ Unique categories inserted!")
    
    db.commit()
    
    print("📌 Processing relationships and historical data...")
    
    # Caching existing accounts and categories
    accounts_cache = {acc.account_id: acc for acc in db.query(Account).all()}
    categories_cache = {cat.name: cat for cat in db.query(Category).all()}
    existing_assocs = {(assoc.account_id, assoc.category_id) for assoc in db.query(AccountCategory).all()}
    
    new_assocs = []
    new_histories = []
    inserted_historicals = set()
    
    for row in df.itertuples(index=False):
        account = accounts_cache.get(row.account_id)
        category = categories_cache.get(row.categories)
        
        if account and category:
            if (account.account_id, category.id) not in existing_assocs:
                new_assocs.append(AccountCategory(account_id=account.account_id, category_id=category.id))
                existing_assocs.add((account.account_id, category.id))
            
            hist_key = (account.account_id, row.date)
            if hist_key not in inserted_historicals:
                if not db.query(Historical).filter_by(account_id=account.account_id, date=row.date).first():
                    new_histories.append(Historical(account_id=account.account_id, subscriber_count=row.subscriber_count, date=row.date))
                inserted_historicals.add(hist_key)
    
    if new_assocs:
        db.bulk_save_objects(new_assocs)
    if new_histories:
        db.bulk_save_objects(new_histories)
    
    print("✅ Relationships and historical data processed!")
    
    db.commit()
    db.close()
    print("✅ Data ingestion completed successfully!")

if __name__ == "__main__":
    file_path = "data/sample_accounts.parquet"
    print("📌 Starting data ingestion...")
    ingest_data(file_path)
    print("🚀 Ingestion process finished!")
