# ShrinkSense Backend

A comprehensive backend API for the ShrinkSense Inventory Management System, built with FastAPI and integrated with Excel data migration capabilities.

## Features

- **Authentication System**: JWT-based authentication with session management
- **Data Migration**: Automated Excel to SQLite migration for inventory data
- **Dynamic Shrinkage Calculation**: Real-time shrinkage metrics calculated from waste data
- **Retail Leaderboard APIs**: Category performance and store rankings
- **RESTful APIs**: Comprehensive CRUD operations for all business entities
- **Database Models**: Well-structured SQLAlchemy models for all data entities
- **Security**: Password hashing, token validation, and session timeout
- **Documentation**: Auto-generated API documentation with Swagger UI

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/verify` - Verify token
- `GET /auth/me` - Get current user info
- `POST /auth/create-user` - Create new user (admin only)

### Retail Leaderboard
- `GET /api/retail-leaderboard/dashboard-summary` - Complete dashboard metrics
- `GET /api/retail-leaderboard/shrinkage-metrics` - Category shrinkage with benchmarks

### Other Endpoints
- `GET /` - API root
- `GET /health` - Health check
- `GET /docs` - API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## Shrinkage Calculation

The system calculates shrinkage dynamically from database values:

```
Shrinkage % = (Number_Damaged_Units + Number_Dump_Units + Number_Expired_Units) / Actual_Quantity_Received × 100
```

### Benchmarks (Industry Standards - NRF)

**Category Shrinkage:**
- Fresh Produce: Best <3%, Median 7%, Laggard >12%
- Dry Goods: Best <3.5%, Median 6.5%, Laggard >12%
- General Merchandise: Best <1%, Median 1.8%, Laggard >2.5%

**In-Transit Loss:**
- Best <2%, Median 4%, Laggard >7%

### In-Transit Loss Calculation

```
In-Transit Loss % = (System_Quantity_Received - Actual_Quantity_Received) / System_Quantity_Received × 100
```

## Database Models (Structured)

### Authentication
- **User** (`app/models/user.py`): Authentication and user management

### Core Business Models  
- **ProductMaster** (`app/models/product.py`): Product catalog information
- **Store** (`app/models/store.py`): Store location and capacity data
- **Inventory** (`app/models/inventory.py`): Extended inventory with waste tracking
- **Returns** (`app/models/returns.py`): Product return tracking

### Partner Management
- **NGOPartner** (`app/models/partners.py`): Non-profit organization partnerships
- **LiquidationPartner** (`app/models/partners.py`): Liquidation service providers

### AI Recommendations
- **RemediationRecommendation** (`app/models/recommendations.py`): AI-generated recommendations
- **ReturnRemediation** (`app/models/recommendations.py`): Return processing recommendations

## Architecture

The application follows a clean, modular architecture:

### Model Layer (`app/models/`)
- **Structured database models** with clear separation of concerns
- **Backward compatibility** maintained through `app/database.py` 
- **Extended inventory model** with all Excel columns for dynamic calculations

### Controller Layer (`app/controllers/`)
- **Authentication** (`auth.py`): JWT-based user management
- **Retail Leaderboard** (`retail_leaderboard.py`): Dynamic shrinkage metrics

### Migration System (`app/utils/migration.py`)
- **Automated Excel-to-Database** mapping with column normalization
- **Data validation** and error handling
- **Relationship preservation** between entities

## Quick Start

### Installation

```bash
git clone <repository-url>
cd Backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
# Edit .env with your settings
```

Required Excel files:
- `ShrinkSense_Complete_System_20250812_122053.xlsx`
- `Retail_Leader_Board_KPIs.xlsx`
- `Remediation_Recommendations_20250812_122359.xlsx`
- `Return_Remediation_Recommendations_20250812_122433.xlsx`
- `Shrinkage_and_Return_KPIs_20250812_122555.xlsx`

### Run Application

```bash
python run.py
# Or: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Data Migration

Automatic migration on startup (when `AUTO_MIGRATE=true`):
1. Reads Excel files and maps columns to database schema
2. Normalizes column names (spaces to underscores, lowercase)
3. Handles data validation and error handling
4. Creates proper relationships between entities

## Configuration Options

Key environment variables:
- `DEBUG`: Enable debug mode
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DATABASE_URL`: SQLite database URL
- `SECRET_KEY`: JWT secret key
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration (default: 30)
- `AUTO_MIGRATE`: Enable automatic data migration (default: true)

## Security

- **Default Admin**: Username: `admin`, Password: `admin` (change in production)
- **JWT Tokens**: 30-minute expiration with session timeout
- **Password Hashing**: BCrypt encryption
- **CORS**: Configurable allowed origins

## Development

```bash
# Debug mode
DEBUG=true python run.py

# Testing
pip install pytest pytest-asyncio
pytest

# Code formatting
pip install black flake8
black app/ && flake8 app/
```

## Troubleshooting

**Common Issues:**
- **Migration Errors**: Verify Excel file paths and formats
- **Shrinkage Showing 0%**: Ensure database has waste data columns populated
- **CORS Issues**: Update `ALLOWED_ORIGINS` in configuration
- **Database Errors**: Check file permissions and paths

**Debug Steps:**
1. Check logs for migration status
2. Verify Excel column mapping in migration.py
3. Test API endpoints at `/docs`
4. Validate database schema matches Excel structure

## Performance Monitoring

The system tracks:
- Category-wise shrinkage percentages
- Store performance rankings
- In-transit loss rates
- Inventory turnover metrics
- Return rate analysis

All metrics are calculated dynamically from current database values for real-time insights.