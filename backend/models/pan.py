from sqlalchemy import Column, Integer, String, ForeignKey
from ..database.database import Base


class Pan(Base):
    __tablename__ = "pan"

    id = Column(Integer, primary_key=True, index=True)
    pan_number = Column(String(10))  # Specify the length of the pan_number column
    name = Column(String(100))  # Specify the length of the name column
    father_name = Column(String(100))  # Specify the length of the father_name column
    dob = Column(String(10))  # Specify the length of the dob column
    user_id = Column(Integer, ForeignKey("users.id"))