from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from core.mediator import Mediator
from core.models.pagination import PagedResponse
from features import (
    CreateDiamondCommand,
    CreateDiamondHandler,
    GetDiamondsByPriceRangeQuery,
    GetDiamondsByPriceRangeHandler
)

from models.diamond_schema import DiamondCreate, DiamondResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = next(get_db())
    mediator.register_handler(GetDiamondsByPriceRangeQuery, GetDiamondsByPriceRangeHandler(db))
    mediator.register_handler(CreateDiamondCommand, CreateDiamondHandler(db))
    yield

app = FastAPI(
    title="Diamond API",
    description="API for managing diamond inventory using CQRS pattern and Vertical Slice Architecture.",
    version="1.0.0",
    lifespan=lifespan
)

# Initialize mediator
mediator = Mediator()

@app.post("/diamonds/", response_model=DiamondResponse)
async def create_diamond(diamond: DiamondCreate, db: Session = Depends(get_db)):
    """Create a new diamond in the database."""
    command = CreateDiamondCommand(
        carat=diamond.carat,
        cut=diamond.cut,
        color=diamond.color,
        clarity=diamond.clarity,
        depth=diamond.depth,
        table=diamond.table,
        price=diamond.price,
        x=diamond.x,
        y=diamond.y,
        z=diamond.z
    )
    try:
        created_diamond = await mediator.send(command)
        return DiamondResponse.model_validate(created_diamond)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/diamonds/price-range/", response_model=PagedResponse[DiamondResponse])
async def get_diamonds_by_price_range(
    min_price: float,
    max_price: float,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get diamonds within a specific price range with pagination.
    
    - **min_price**: Minimum price to filter by
    - **max_price**: Maximum price to filter by
    - **page**: Page number (default: 1)
    - **size**: Number of items per page (default: 10, max: 100)
    """
    query = GetDiamondsByPriceRangeQuery(
        min_price=min_price,
        max_price=max_price,
        page=page,
        size=size
    )
    try:
        result = await mediator.send(query)
        # Convert SQLAlchemy models to Pydantic models
        result.items = [DiamondResponse.model_validate(diamond) for diamond in result.items]
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 