from typing import Union

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from resources import Message, List
from db import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from db_methods import get_records, get_record_by_id

Base.metadata.create_all(bind=engine)

app = FastAPI()

# TODO: 1). Parse #words 2). Implement jobs 3). Implement UI


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return "Index page"


@app.get("/records")
def read_records(db: Session = Depends(get_db)):
    records = get_records(db)
    return records


@app.get("/records/{record_id}")
def read_record(record_id: str, db: Session = Depends(get_db)):
    record = get_record_by_id(db, record_id=str(record_id))
    print(record)

    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)