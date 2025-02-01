from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from database import SessionLocal
from models import Account, Category, AccountCategory, Historical
from ingestion import ingest_data
import pandas as pd
from datetime import datetime, timedelta

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
    """
    Consulta contas com crescimento maior que 10% no último mês.
    """
    # Obter a data mais recente do banco
    max_date_query = text("SELECT MAX(date) FROM historical")
    max_date_value = db.execute(max_date_query).scalar()
    print("max_date_value:", max_date_value, type(max_date_value))
    
    if not max_date_value:
        return {"message": "No data found"}
    
    # Converter max_date_value para datetime, se necessário
    if isinstance(max_date_value, str):
        try:
            max_date = datetime.fromisoformat(max_date_value)
        except Exception as e:
            return {"message": f"Error converting max_date: {e}"}
    else:
        max_date = max_date_value

    # Definir a janela de análise com base na data mais recente
    analysis_window = max_date - timedelta(days=30)
    print("max_date:", max_date)
    print("analysis_window:", analysis_window)
    
    # Obter os dados históricos dentro da janela de análise
    recent_entries_query = text("""
        SELECT account_id, subscriber_count, date
        FROM historical
        WHERE date > :analysis_window
    """)
    
    # Converte analysis_window para string ISO, se necessário
    recent_entries = pd.read_sql(
        recent_entries_query,
        db.bind,
        params={"analysis_window": analysis_window.isoformat()}
    )

    if recent_entries.empty:
        return {"message": "No recent data found"}
    
    # Ordenar registros por conta e data
    sorted_records = recent_entries.sort_values(by=["account_id", "date"])
    
    # Obter o primeiro e o último registro de cada conta
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
    
    # Merge dos snapshots para calcular crescimento
    trend_data = initial_snapshot.merge(latest_snapshot, on="account_id", how="inner")
    trend_data["growth_values"] = trend_data["current_subscribers"] - trend_data["baseline_subscribers"]
    trend_data["growth_percentage"] = ((trend_data["growth_values"] / trend_data["baseline_subscribers"]) * 100).round(2)
    
    # Filtrar contas com crescimento acima de 10%
    high_growth_accounts = trend_data[trend_data["growth_percentage"] > 10.]

    return {"high_growth_accounts": high_growth_accounts.to_dict(orient="records")}


@app.post("/accounts/upload")
def upload_new_accounts():
    file_path = "data/add_accounts.parquet"
    ingest_data(file_path)
    return {"message": "New accounts data ingested successfully!"}
