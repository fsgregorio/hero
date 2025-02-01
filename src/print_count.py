import sqlite3

def print_table_counts(db_path="data/social_media.db"):
    # Conecta ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Lista os nomes de todas as tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("📌 Tabelas no banco de dados:", tables)

    # Para cada tabela, executa um SELECT COUNT(*) para contar os registros
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        print(f"📌 Total de registros na tabela '{table_name}': {count}")

    conn.close()

if __name__ == "__main__":
    print_table_counts()
