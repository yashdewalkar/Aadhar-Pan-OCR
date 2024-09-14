from sqlalchemy import Column, Integer, String, ForeignKey
from ..database.database import Base
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = "blog"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))  # Specify the length of the title column
    body = Column(String(20000))  # You can specify the length of the body column based on your requirements
    published = Column(String(10))  # Specify the length of the published column
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="blogs")
     