from pydantic import BaseModel

class DiamondBase(BaseModel):
    carat: float
    cut: str
    color: str
    clarity: str
    depth: float
    table: float
    price: int
    x: float
    y: float
    z: float

class DiamondCreate(DiamondBase):
    pass

class DiamondResponse(DiamondBase):
    id: int

    class Config:
        from_attributes = True 