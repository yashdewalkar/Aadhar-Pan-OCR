from sqlalchemy import Column, Integer, String, ForeignKey
from ..database.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))  # Specify the length of the name column
    email = Column(String(100))  # Specify the length of the email column
    password = Column(String(255))  # Specify the length of the password column

    blogs = relationship('Blog', back_populates="creator")