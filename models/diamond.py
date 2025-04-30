from sqlalchemy import Column, Integer, Float, String
from config.database import Base

class Diamond(Base):
    __tablename__ = "diamonds"

    id = Column(Integer, primary_key=True, index=True)
    carat = Column(Float)
    cut = Column(String)
    color = Column(String)
    clarity = Column(String)
    depth = Column(Float)
    table = Column(Float)
    price = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float) 