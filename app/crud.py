from sqlalchemy.orm import Session
from . import models, schemas

def get_item(db: Session, item_id: int):
    # Get a single item by its ID
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    # Get a list of items, with pagination
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate):
    # Create a new item in the database
    # Unpack the Pydantic model's dict into the SQLAlchemy model
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item) # Refresh to get the new ID and any default DB values
    return db_item

def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    # Update an existing item
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        # Update the attributes
        db_item.name = item.name
        db_item.description = item.description
        db_item.price = item.price
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    # Delete an item
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return {"ok": True}
    return {"ok": False}
