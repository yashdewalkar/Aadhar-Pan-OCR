from sqlalchemy import Column, Integer, String, ForeignKey
from ..database.database import Base


class Aadhar(Base):
    __tablename__ = "aadhar"

    id = Column(Integer, primary_key=True, index=True)
    aadhar_number = Column(String(12))  # Specify the length of the aadhar_number column
    name = Column(String(100))  # Specify the length of the name column
    gender = Column(String(10))  # Specify the length of the gender column
    user_id = Column(Integer, ForeignKey("users.id"))
