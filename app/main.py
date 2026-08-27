from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

# Import our own modules
from . import crud, models, schemas
from .database import SessionLocal, engine
from .auth import create_access_token, get_current_user

# Create the database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Item CRUD API", description="A simple CRUD API for items", version="1.0.0")

# Dependency: This function will provide a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# AUTH - POST /token (Login)
@app.post("/token", tags=["Authentication"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != "admin" or form_data.password != "secretpassword":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username atau password salah"
        )
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# CREATE - POST /items/ (Terproteksi Auth Token)
@app.post("/items/", response_model=schemas.Item, status_code=201, summary="Create a new item", tags=["Items"])
def create_item(
    item: schemas.ItemCreate, 
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    Create a new item with all the information:

    - **name**: each item must have a name
    - **description**: a longer description (optional)
    - **price**: the price of the item (required)
    """
    return crud.create_item(db=db, item=item)

# READ (ALL) - GET /items/
@app.get("/items/", response_model=List[schemas.Item], summary="Get a list of items", tags=["Items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of items from the database.

    - **skip**: number of records to skip (for pagination)
    - **limit**: maximum number of records to return (for pagination)
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

# READ (ONE) - GET /items/{item_id}
@app.get("/items/{item_id}", response_model=schemas.Item, summary="Get a single item by ID", tags=["Items"])
def read_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get a single item by its unique ID.

    - **item_id**: the ID of the item to retrieve
    """
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# UPDATE - PUT /items/{item_id}
@app.put("/items/{item_id}", response_model=schemas.Item, summary="Update an existing item", tags=["Items"])
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Update the details of an existing item.

    - **item_id**: the ID of the item to update
    - **item**: the updated item data
    """
    db_item = crud.update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# DELETE - DELETE /items/{item_id}
@app.delete("/items/{item_id}", summary="Delete an item by ID", tags=["Items"])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete an item from the database.

    - **item_id**: the ID of the item to delete
    """
    result = crud.delete_item(db, item_id=item_id)
    if not result.get("ok"):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": f"Item {item_id} deleted successfully"}

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Item CRUD API. Go to /docs to see the interactive documentation."}

@app.get("/health")
def health_check():
    return {"message": "OK"}

