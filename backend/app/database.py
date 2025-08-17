"""
Database compatibility layer - maintains backward compatibility
"""

# Import everything from models to maintain existing imports
from app.models import *

# Maintain backward compatibility for existing imports
from app.models.base import Base, engine, SessionLocal, get_db, create_tables
from app.models.user import User, hash_password, verify_password, create_default_admin, update_user_activity
from app.models.product import ProductMaster
from app.models.store import Store
from app.models.inventory import Inventory
from app.models.returns import Returns
from app.models.partners import NGOPartner, LiquidationPartner
from app.models.recommendations import RemediationRecommendation, ReturnRemediation