import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql.annotation import Annotated
from starlette import status

import database
import models

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database.engine)

models.base.metadata.create_all(bind=database.engine)

app = FastAPI()


class Record_Base(BaseModel):
    title: str
    content: str
    user_id: int


class User_Base(BaseModel):
    username: str
    first_name: str
    second_name: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/records/', status_code=status.HTTP_201_CREATED)
async def create_record(record: Record_Base, db: Session = Depends(get_db)):
    db_record = models.Record(**record.dict())
    print(db_record)
    db.add(db_record)
    db.commit()
    return db_record


@app.get('/records/{record_id}', status_code=status.HTTP_200_OK)
async def read_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail='Record not found')
    return record


@app.delete('/records/{record_id}', status_code=status.HTTP_200_OK)
async def delete_record(record_id: int, db: Session = Depends(get_db)):
    db_record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail='Record not found')
    db.delete(db_record)
    db.commit()


@app.put('/records/{record_id}', status_code=status.HTTP_200_OK)
async def update_record(record_id: int, record: Record_Base, db: Session = Depends(get_db)):
    db_record = db.query(models.Record).filter(models.Record.id == record_id).first()
    if db_record is None:
        raise HTTPException(status_code=404, detail='Record not found')
    db.query(models.Record).filter(models.Record.id == record_id).update(record.dict(), synchronize_session=False)
    db.commit()
    return db_record


@app.post('/users/', status_code=status.HTTP_201_CREATED)
async def create_user(user: User_Base, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    return db_user


@app.get('/users/{user_id}', status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@app.delete('/user/{user_id}', status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    db.delete(db_user)
    db.commit()


@app.put('/user/{user_id}', status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: User_Base, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    db.query(models.User).filter(models.User.id == user_id).update(user.dict(), synchronize_session=False)
    db.commit()
    return db_user


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
