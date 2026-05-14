from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

senha_pura = os.getenv("fiap_tecchalleng_4_lstm")

if not senha_pura:
    raise ValueError("Senha não encontrada no .env")

senha = urllib.parse.quote_plus(senha_pura)

DATABASE_URL = f"postgresql://postgres.jgwihomfyrkfpabbmwiu:{senha}@aws-1-sa-east-1.pooler.supabase.com:5432/postgres"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "connect_timeout": 10,
        "sslmode": "require"
    }
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()