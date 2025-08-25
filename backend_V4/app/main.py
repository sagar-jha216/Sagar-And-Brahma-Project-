# from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes.products import router as product_router  
from app.routes.category import router as category_router
from app.routes.user import router as user_router
# from app.scripts.dataFixing import add_is_admin_column
from app.routes import inventory
from app.routes import liquidation_partners
from app.routes import ngo_partners
from app.routes.remediation_recommendations import router as remediation_recommendations_router
from app.routes import returns as returns_route
from app.routes.return_remediation import router as return_remediation_router
from app.routes.returns import router as returns_router  
from app.routes.stores import router as stores_router  
from app.routes.analytics import router as analytics_router
from app.routes.dashboard_kpis import router as dashboard_kpis_router
from app.routes.dashboard_graphs import router as dashboard_graphs_router
from app.routes import Retail_Leader_Board_KPIs
from app.routes.command_center import router as command_center_router
from app.routes.remediation_recommendations_route import router as remediation_route_router
# from app.scripts import load_user

# Create all tables
Base.metadata.create_all(bind=engine)
# add_is_admin_column()
# Initialize FastAPI app
app = FastAPI(
    title="Shrink Sense",
    description="A simple API to manage Shrink Sense Data",
    version="1.0.0"
)


# CORS middleware (optional but useful for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # You can restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include your product routes
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(category_router, prefix="/category", tags=["Category"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
app.include_router(liquidation_partners.router, prefix="/liquidation_partners", tags=["Liquidation_Partners"])
app.include_router(ngo_partners.router, prefix="/ngo-partners", tags=["NGO Partners"])
app.include_router(remediation_recommendations_router, prefix="/remediation-recommendations", tags=["Remediation Recommendations"])
app.include_router(return_remediation_router, prefix="/return-remediation", tags=["Return Remediation"])
app.include_router(returns_router, prefix="/returns", tags=["Returns"])
app.include_router(stores_router, prefix="/stores", tags=["Stores"])
# app.include_router(user_router, prefix="/users", tags=["Users"])
# app.include_router(user_router, prefix="/auth", tags=["Authentication"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"]) 
app.include_router(dashboard_kpis_router, prefix="/analytics", tags=["Dashboard KPIs"])
app.include_router(dashboard_graphs_router, prefix="/analytics", tags=["Dashboard Graphs"])
app.include_router(Retail_Leader_Board_KPIs.router, prefix="/retail-kpi", tags=["Retail KPI"])
app.include_router(command_center_router, prefix="/analytics", tags=["Command Center"])
app.include_router(remediation_route_router, prefix="/api", tags=["Remediation Recommendations API"])




