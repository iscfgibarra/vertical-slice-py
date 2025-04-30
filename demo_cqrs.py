from config.database import engine, Base, get_db
from core.mediator import Mediator
from sqlalchemy.orm import Session


# Create database tables
Base.metadata.create_all(bind=engine)

from features.diamonds.queries.get_diamonds_by_price_range import (
    GetDiamondsByPriceRangeQuery,
    GetDiamondsByPriceRangeHandler
)
from features.diamonds.commands.create_diamond import (
    CreateDiamondCommand,
    CreateDiamondHandler
)


async def demonstrate_cqrs():
    # Create database session
    db = Session(engine)

    # Create mediator
    mediator = Mediator()

    # Register handlers
    mediator.register_handler(GetDiamondsByPriceRangeQuery, GetDiamondsByPriceRangeHandler(db))
    mediator.register_handler(CreateDiamondCommand, CreateDiamondHandler(db))

    try:
        # Example 1: Create a new diamond using command
        create_command = CreateDiamondCommand(
            carat=1.0,
            cut="Ideal",
            color="D",
            clarity="IF",
            depth=60.0,
            table=55.0,
            price=10000,
            x=6.0,
            y=6.0,
            z=3.6
        )
        created_diamond = await mediator.send(create_command)
        print(f"\nCreated new diamond with ID: {created_diamond.id}")

        # Example 2: Query diamonds by price range
        query = GetDiamondsByPriceRangeQuery(min_price=1000, max_price=2000)
        diamonds = await mediator.send(query)
        print(f"\nDiamonds between $1000 and $2000: {len(diamonds)}")

    finally:
        db.close()