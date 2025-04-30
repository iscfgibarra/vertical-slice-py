from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.diamond import Diamond
from repositories.base import BaseRepository

class DiamondRepository(BaseRepository[Diamond]):
    def __init__(self):
        super().__init__(Diamond)

    def get_by_price_range(self, db: Session, min_price: float, max_price: float, skip: int = 0, limit: int = 100) -> List[Diamond]:
        return db.query(self.model).filter(
            and_(
                self.model.price >= min_price,
                self.model.price <= max_price
            )
        ).offset(skip).limit(limit).all()

    def get_by_cut(self, db: Session, cut: str) -> List[Diamond]:
        return db.query(self.model).filter(self.model.cut == cut).all()

    def get_by_color(self, db: Session, color: str) -> List[Diamond]:
        return db.query(self.model).filter(self.model.color == color).all()

    def get_by_clarity(self, db: Session, clarity: str) -> List[Diamond]:
        return db.query(self.model).filter(self.model.clarity == clarity).all()

    def get_by_carat_range(self, db: Session, min_carat: float, max_carat: float) -> List[Diamond]:
        return db.query(self.model).filter(
            and_(
                self.model.carat >= min_carat,
                self.model.carat <= max_carat
            )
        ).all()

    def get_expensive_diamonds(self, db: Session, price_threshold: float = 1000) -> List[Diamond]:
        return db.query(self.model).filter(self.model.price > price_threshold).all() 