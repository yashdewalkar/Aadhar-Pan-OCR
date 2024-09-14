from typing import List, Optional
from pydantic import BaseModel


class AadharBase(BaseModel):
    name: str
    aadhar_number: str
    gender:str
    user_id:int
    
    
class Aadhar(AadharBase):
    class Config():
        orm_mode = True


class ShowAadhar(BaseModel):
    aadhar_number: str
    name:str
    gender:str
    user_id:int
    class Config():
        orm_mode = True
