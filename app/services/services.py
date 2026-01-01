from fastapi import HTTPException, Depends, Response
from sqlalchemy.orm import Session
import logging
from sqlalchemy import func
from app.database.dbsession import get_db


logger = logging.getLogger(__name__)


def _slug_creator(name:str, db_table_name, db:Session=Depends(get_db)):
    try:
        slug = '0000'
        slug_count = db.query(func.count(db_table_name.id)).filter(db_table_name.slug == name).scalar()
        
        if not slug_count:
#            for i in range(0000,9999):
#                slug_all = str(name)+'-'+str(i)
#            if db.query(db_table_name).filter(db_table_name.slug == slug_all).first():
            return 0
        return int(slug_count)+1
    except Exception as e:
        raise 'Ошибка при обращении к БД для формирования slug'