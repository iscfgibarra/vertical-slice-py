# Diamond Inventory Management System

A modern diamond inventory management system built with FastAPI, SQLAlchemy, and CQRS pattern using MediatR.

## Project Structure

```
project/
├── core/
│   ├── interfaces/
│   │   └── mediator.py      # Base interfaces for CQRS
│   └── mediator.py          # Concrete mediator implementation
├── features/
│   └── diamonds/
│       ├── commands/        # Write operations
│       │   └── create_diamond.py
│       └── queries/         # Read operations
│           └── get_diamonds_by_price_range.py
├── models/
│   └── diamond.py          # Database models
├── repositories/
│   ├── base.py             # Base repository
│   └── diamond_repository.py # Diamond-specific repository
├── config/
│   └── database.py         # Database configuration
├── app.py                  # FastAPI application
└── main.py                 # Example usage
```

## Architecture

The project follows a Vertical Slice Architecture with CQRS pattern:

- **Vertical Slices**: Features are organized by business capability
- **CQRS**: Commands (write) and Queries (read) are separated
- **MediatR**: Implements the mediator pattern for handling commands and queries
- **Repository Pattern**: Abstracts database operations

## Features

- Create new diamonds
- Query diamonds by price range
- SQLite database for data persistence
- FastAPI for REST API endpoints
- Automatic API documentation

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the FastAPI server:
   ```bash
   uvicorn app:app --reload
   ```

2. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Create Diamond
- **POST** `/diamonds/`
- Creates a new diamond in the database
- Request body:
  ```json
  {
    "carat": 1.0,
    "cut": "Ideal",
    "color": "D",
    "clarity": "IF",
    "depth": 60.0,
    "table": 55.0,
    "price": 10000,
    "x": 6.0,
    "y": 6.0,
    "z": 3.6
  }
  ```

### Get Diamonds by Price Range
- **GET** `/diamonds/price-range/?min_price=1000&max_price=2000`
- Returns diamonds within the specified price range
- Query parameters:
  - `min_price`: Minimum price
  - `max_price`: Maximum price

## Development

### Adding New Features

1. Create a new command or query in the appropriate feature folder:
   ```python
   # features/diamonds/queries/get_diamonds_by_cut.py
   class GetDiamondsByCutQuery(IRequest[List[Diamond]]):
       def __init__(self, cut: str):
           self.cut = cut

   class GetDiamondsByCutHandler(IRequestHandler[List[Diamond]]):
       def __init__(self, db: Session):
           self.db = db
           self.repository = DiamondRepository()

       async def handle(self, request: GetDiamondsByCutQuery) -> List[Diamond]:
           return self.repository.get_by_cut(self.db, request.cut)
   ```

2. Register the handler in `app.py`:
   ```python
   @app.on_event("startup")
   async def startup_event():
       # ... existing registrations ...
       mediator.register_handler(GetDiamondsByCutQuery, GetDiamondsByCutHandler(db))
   ```

3. Add the endpoint:
   ```python
   @app.get("/diamonds/cut/{cut}", response_model=List[DiamondResponse])
   async def get_diamonds_by_cut(cut: str, db: Session = Depends(get_db)):
       query = GetDiamondsByCutQuery(cut=cut)
       return await mediator.send(query)
   ```

## Testing

Run the example usage:
```bash
python main.py
```

## License

MIT License