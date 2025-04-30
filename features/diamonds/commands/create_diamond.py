from core.interfaces.mediator import IRequest, IRequestHandler
from models.diamond import Diamond
from repositories.diamond_repository import DiamondRepository
from sqlalchemy.orm import Session

class CreateDiamondCommand(IRequest[Diamond]):
    def __init__(self, carat: float, cut: str, color: str, clarity: str,
                 depth: float, table: float, price: int, x: float, y: float, z: float):
        self.carat = carat
        self.cut = cut
        self.color = color
        self.clarity = clarity
        self.depth = depth
        self.table = table
        self.price = price
        self.x = x
        self.y = y
        self.z = z

class CreateDiamondHandler(IRequestHandler[Diamond]):
    def __init__(self, db: Session):
        self.db = db
        self.repository = DiamondRepository()

    async def handle(self, request: CreateDiamondCommand) -> Diamond:
        diamond_data = {
            "carat": request.carat,
            "cut": request.cut,
            "color": request.color,
            "clarity": request.clarity,
            "depth": request.depth,
            "table": request.table,
            "price": request.price,
            "x": request.x,
            "y": request.y,
            "z": request.z
        }
        return self.repository.create(self.db, diamond_data) 