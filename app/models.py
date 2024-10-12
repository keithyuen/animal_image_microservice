from sqlalchemy import Column, Integer, String
from app.database import Base

class AnimalImage(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    animal_type = Column(String, index=True)
    image_url = Column(String, index=True)
