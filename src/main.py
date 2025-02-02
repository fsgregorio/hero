import uvicorn
from fastapi import FastAPI
from .api import app as api_app

# Criando a instância principal do FastAPI
app = FastAPI()

# Incluindo os endpoints definidos em api.py
app.include_router(api_app.router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
