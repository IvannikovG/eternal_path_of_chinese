from sqlalchemy.orm import Session
from models import ChineseRecord


def get_record_by_id(db: Session, record_id: str):
    record = db.query(ChineseRecord).\
        filter(ChineseRecord.resource["resource"]["hieroglyph_id"].astext == record_id).first()
    print(record, record_id)
    return record


def get_records(db: Session):
    return db.query(ChineseRecord).all()
