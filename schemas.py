from pydantic import BaseModel, EmailStr

class CreateTransaction(BaseModel):
    title:str
    amount:float
    category:str

class ResponseTransaction(BaseModel):
    id:int
    owner_id:int

    class Config:
        from_attributes=True

class CreateUser(BaseModel):
    email:EmailStr
    password:str

class ResponseUser(BaseModel):
     id: int
     email: EmailStr

     class Config:
            from_attributes = True

