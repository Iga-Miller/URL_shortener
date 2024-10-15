from celery import Celery
from hashlib import md5
from sqlalchemy.orm import Session
from app.db import get_db, URLMapping  

celery_app = Celery(
    'tasks',
    broker='amqp://guest:guest@rabbitmq//',
    backend='rpc://'
)

@celery_app.task
def shorten_url_task(original_url: str):
    db: Session = next(get_db())

    try:
        existing_url_mapping = db.query(URLMapping).filter(URLMapping.original_url == original_url).first()
        if existing_url_mapping:
            return existing_url_mapping.short_url

        shortened_url = md5(original_url.encode()).hexdigest()[:6]

        while db.query(URLMapping).filter(URLMapping.short_url == shortened_url).first():
            shortened_url = md5((original_url + shortened_url).encode()).hexdigest()[:6]

        db_url_mapping = URLMapping(original_url=original_url, short_url=shortened_url)
        db.add(db_url_mapping)
        db.commit()

        print("Wszystkie URL-e w bazie:")
        for mapping in db.query(URLMapping).all():
            print(f"{mapping.original_url} -> {mapping.short_url}")

        return shortened_url

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()





