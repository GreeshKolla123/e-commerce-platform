from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    email: str
    password: str

class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
    category: str

class OrderSchema(BaseModel):
    user_id: int
    total: float
    status: str

class OrderItemSchema(BaseModel):
    order_id: int
    product_id: int
    quantity: int

class CartSchema(BaseModel):
    user_id: int
    product_id: int
    quantity: int
