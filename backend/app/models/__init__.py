"""
Models package for ShrinkSense Backend
"""

from .base import Base, engine, SessionLocal, get_db, create_tables
from .user import User, hash_password, verify_password, create_default_admin, update_user_activity
from .product import ProductMaster
from .store import Store
from .inventory import Inventory
from .returns import Returns
from .partners import NGOPartner, LiquidationPartner
from .recommendations import RemediationRecommendation, ReturnRemediation

__all__ = [
    "Base", "engine", "SessionLocal", "get_db", "create_tables",
    "User", "ProductMaster", "Store", "Inventory", "Returns", 
    "NGOPartner", "LiquidationPartner", "RemediationRecommendation", "ReturnRemediation",
    "hash_password", "verify_password", "create_default_admin", "update_user_activity"
]