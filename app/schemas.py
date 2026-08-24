from pydantic import BaseModel, ConfigDict

# Base schema with common attributes
class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float

# Schema for creating an item (inherits from ItemBase)
class ItemCreate(ItemBase):
    pass

# Schema for reading/returning an item (inherits from ItemBase)
# This will include the ID, which is created by the database.
class Item(ItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
