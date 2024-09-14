from typing import List, Optional
from pydantic import BaseModel


class PanBase(BaseModel):
    name: str
    pan_number: str
    name:str
    father_name:str
    dob:str
    user_id:int
    
    
class Pan(PanBase):
    class Config():
        orm_mode = True


class ShowPan(BaseModel):
    name: str
    pan_number: str
    name:str
    father_name:str
    dob:str
    user_id:int
    class Config():
        orm_mode = True
