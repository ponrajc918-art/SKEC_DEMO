"""Safely recreate synthetic development data. Never permits a production reset."""
import os
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT / "backend"))

if os.getenv("APP_ENV","development") != "development" or os.getenv("ALLOW_DEMO_RESET") != "YES_RESET_DEMO":
    raise SystemExit("Refusing reset. Set APP_ENV=development and ALLOW_DEMO_RESET=YES_RESET_DEMO explicitly.")

from app.core import SessionLocal, engine
from app.models import Base
from app.seed import seed

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
db=SessionLocal()
try:
    seed(db)
finally:
    db.close()
print("Synthetic development data reset successfully.")
