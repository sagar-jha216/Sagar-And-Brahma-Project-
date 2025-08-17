"""
Configuration settings for ShrinkSense Backend
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "ShrinkSense Backend"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./shrinksense_new.db"
    MIGRATION_DATABASE_URL: str = "sqlite:///./shrinksense_inventory.sqlite"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SESSION_TIMEOUT_MINUTES: int = 60
    
    # CORS settings
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    @property
    def origins_list(self) -> List[str]:
        """Convert comma-separated origins to list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    # Migration settings
    AUTO_MIGRATE: bool = True
    EXCEL_FILE_PATH: str = "ShrinkSense_Complete_System_20250812_122053.xlsx"
    KPI_FILE_PATH: str = "Retail_Leader_Board_KPIs.xlsx"
    REMEDIATION_FILE_PATH: str = "Remediation_Recommendations_20250812_122359.xlsx"
    RETURN_REMEDIATION_FILE_PATH: str = "Return_Remediation_Recommendations_20250812_122433.xlsx"
    SHRINKAGE_RETURN_KPIS_FILE_PATH: str = "Shrinkage_and_Return_KPIs_20250812_122555.xlsx"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

def get_settings() -> Settings:
    return Settings()