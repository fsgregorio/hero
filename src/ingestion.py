import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import SessionLocal, engine
from models import Account, Category, AccountCategory, Historical
from transformation import load_and_transform_data

def ingest_data(file_path: str):
    """
    Loads transformed data and inserts it into the database.
    Ensures unique accounts, categories, and avoids duplicating historical data.
    
    Steps:
    1. Load and transform the raw data using transformation.py.
    2. Remove duplicate accounts and categories before processing.
    3. Insert unique accounts into the accounts table.
    4. Insert unique categories into the categories table.
    5. Process relationships and historical data using caching and bulk insert.
       (Verifica se já existe um registro histórico para evitar duplicação.)
    6. Commit changes to the database.
    """
    print("📌 Loading and transforming data...")
    df = load_and_transform_data(file_path)  # Apply transformations before ingestion
    print("✅ Data transformation completed!")
    
    # Remove duplicate accounts and categories before processing
    unique_accounts = df[['account_id']].drop_duplicates()
    unique_categories = df[['categories']].drop_duplicates()
    
    db = SessionLocal()
    
    print("📌 Inserting unique accounts...")
    # Step 3: Insert unique accounts
    for _, row in unique_accounts.iterrows():
        account = db.query(Account).filter_by(account_id=row['account_id']).first()
        if not account:
            account = Account(account_id=row['account_id'])
            db.add(account)
    print("✅ Unique accounts inserted!")
    
    print("📌 Inserting unique categories...")
    # Step 4: Insert unique categories
    for _, row in unique_categories.iterrows():
        category = db.query(Category).filter_by(name=row['categories']).first()
        if not category:
            category = Category(name=row['categories'])
            db.add(category)
    print("✅ Unique categories inserted!")
    
    db.commit()
    
    print("📌 Processing relationships and historical data...")
    
    # --- Otimizações para relacionamentos e históricos ---
    
    # 1. Carrega todas as contas e categorias em cache para acesso rápido
    accounts_cache = {account.account_id: account for account in db.query(Account).all()}
    categories_cache = {category.name: category for category in db.query(Category).all()}
    
    # 2. Carrega as associações existentes para evitar duplicação
    existing_assocs = {(assoc.account_id, assoc.category_id) for assoc in db.query(AccountCategory).all()}
    
    # 3. Listas para acumular novos registros para bulk insert
    new_assocs = []
    new_histories = []
    # Set para controlar combinações já inseridas (account_id, date)
    inserted_historicals = set()
    
    # 4. Itera sobre as linhas do DataFrame usando itertuples (mais rápido que iterrows)
    for row in df.itertuples(index=False):
        account = accounts_cache.get(row.account_id)
        category = categories_cache.get(row.categories)
        
        # Caso alguma informação não seja encontrada, pula a linha
        if account is None or category is None:
            continue
        
        # Cria a associação se ela não existir
        if (account.account_id, category.id) not in existing_assocs:
            new_assocs.append(AccountCategory(account_id=account.account_id, category_id=category.id))
            existing_assocs.add((account.account_id, category.id))
        
        # Define a chave para histórico
        hist_key = (account.account_id, row.date)
        # Se essa combinação já foi inserida (ou verificada previamente), pula
        if hist_key in inserted_historicals:
            continue
        
        # Verifica se já existe um registro histórico para esta conta e data no banco
        existing_history = db.query(Historical).filter_by(
            account_id=account.account_id,
            date=row.date
        ).first()
        if not existing_history:
            new_histories.append(Historical(
                account_id=account.account_id,
                subscriber_count=row.subscriber_count,
                date=row.date
            ))
            # Marca a combinação como inserida para evitar duplicatas na mesma execução
            inserted_historicals.add(hist_key)
        else:
            # Mesmo se o registro já existir no banco, podemos marcar para não inserir novamente
            inserted_historicals.add(hist_key)
    
    # 5. Bulk insert: insere os novos registros em bloco
    if new_assocs:
        db.bulk_save_objects(new_assocs)
    if new_histories:
        db.bulk_save_objects(new_histories)
    
    print("✅ Relationships and historical data processed!")
    
    db.commit()
    print("✅ Data ingestion completed successfully!")
    
    db.close()

if __name__ == "__main__":
    file_path = "data/sample_accounts.parquet"
    print("📌 Starting data ingestion...")
    ingest_data(file_path)
    print("🚀 Ingestion process finished!")
