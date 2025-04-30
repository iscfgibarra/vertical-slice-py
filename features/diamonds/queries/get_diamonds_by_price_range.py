from typing import List
from core.interfaces.mediator import IRequest, IRequestHandler
from core.models.pagination import PagedResponse
from models.diamond import Diamond
from models.diamond_schema import DiamondResponse
from repositories.diamond_repository import DiamondRepository
from sqlalchemy.orm import Session
from sqlalchemy import func


class GetDiamondsByPriceRangeQuery(IRequest[PagedResponse[DiamondResponse]]):
    def __init__(self, min_price: float, max_price: float, page: int = 1, size: int = 10):
        self.min_price = min_price
        self.max_price = max_price
        self.page = max(1, page)  # Ensure page is at least 1
        self.size = max(1, min(size, 100))  # Ensure size is between 1 and 100


class GetDiamondsByPriceRangeHandler(IRequestHandler[PagedResponse[DiamondResponse]]):
    def __init__(self, db: Session):
        self.db = db
        self.repository = DiamondRepository()

    async def handle(self, request: GetDiamondsByPriceRangeQuery) -> PagedResponse[DiamondResponse]:
        # Calculate offset
        offset = (request.page - 1) * request.size

        # Get total count
        total = self.db.query(func.count(Diamond.id)).filter(
            Diamond.price >= request.min_price,
            Diamond.price <= request.max_price
        ).scalar()

        # Get paginated results
        items = self.repository.get_by_price_range(
            self.db,
            min_price=request.min_price,
            max_price=request.max_price,
            skip=offset,
            limit=request.size
        )

        # Convert SQLAlchemy models to Pydantic models
        pydantic_items = [DiamondResponse.model_validate(diamond) for diamond in items]

        return PagedResponse.create(
            items=pydantic_items,
            total=total,
            page=request.page,
            size=request.size
        )
