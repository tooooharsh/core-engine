# RentEase Core Engine API

## Setup

1. Create `.env` file:
```bash
cp .env.example .env
```

2. Update `.env` with your values:
```
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=rentease
ANTHROPIC_API_KEY=your_actual_api_key_here
```

3. Start MongoDB (if running locally):
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or using brew (macOS)
brew services start mongodb-community
```

4. Start the API server:
```bash
uv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

5. Access API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health Check
```
GET /health
```

### Create Property
```
POST /api/v1/properties
```

Request body:
```json
{
  "hard_config": {
    "area_sqft": 1200.0,
    "bhk_type": "2BHK",
    "bedrooms": 2,
    "bathrooms": 2,
    "property_type": "apartment"
  },
  "soft_config": {
    "furniture_items": ["sofa", "bed", "dining_table"],
    "appliances": ["fridge", "ac"],
    "amenities": ["parking"]
  },
  "city": "Bangalore",
  "locality": "Koramangala",
  "latitude": 12.9352,
  "longitude": 77.6245,
  "current_rent": 30000.0
}
```

### Get Property by ID
```
GET /api/v1/properties/{property_id}
```

### List All Properties
```
GET /api/v1/properties

# Filter by city
GET /api/v1/properties?city=Bangalore
```

### Analyze Property
```
POST /api/v1/properties/analyze
```

Request body:
```json
{
  "property_id": "your-property-id",
  "radius_km": 2.0,
  "area_tolerance_percent": 15.0
}
```

Response:
```json
{
  "property_id": "your-property-id",
  "filtered_properties_count": 5,
  "banding_result": {
    "bands": {
      "L5": ["prop1"],
      "L3": ["prop2", "prop3"],
      "L1": ["prop4"]
    },
    "parameters_used": ["furnishing_score", "rent_per_sqft"],
    "parameters_rationale": "Categorized based on...",
    "new_property_band": "L3",
    "confidence_score": 0.85
  },
  "iqr_analysis": {
    "q1": 22000.0,
    "median": 25000.0,
    "q3": 28000.0,
    "iqr": 6000.0,
    "recommended_min": 22000.0,
    "recommended_max": 28000.0
  }
}
```

## Testing

The project uses **testcontainers** to run integration tests against a real MongoDB instance in a Docker container. This ensures tests run against actual database behavior.

### Prerequisites
- Docker must be running (supports Docker Desktop or Colima)
- For Colima users, configuration is pre-set in `pyproject.toml`

### Run all tests:
```bash
uv run python -m pytest tests/ -v
```

### Run specific test categories:
```bash
# Unit tests only (models, utils, agents)
uv run python -m pytest tests/models tests/core_engine -v

# Integration tests (database + API with real MongoDB)
uv run python -m pytest tests/database tests/api -v
```

### Test Structure
```
tests/
├── models/           → Domain model tests
├── core_engine/
│   ├── agents/       → Agent unit tests
│   ├── graphs/       → Workflow tests
│   └── utils/        → Utility function tests
├── database/         → Repository integration tests (real MongoDB)
├── api/              → API endpoint integration tests (real MongoDB)
└── conftest.py       → Shared fixtures (MongoDB container)
```

## Architecture

- **FastAPI**: REST API framework
- **Motor**: Async MongoDB driver
- **Pydantic**: Request/response validation
- **LangGraph**: Property analysis workflow
- **Claude API**: LLM-based property banding
- **Testcontainers**: Real MongoDB for integration tests
