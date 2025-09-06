from sqlalchemy import Column, Integer, String
from app.database import Base
from app.database import Base

class ProductMaster(Base):
    __tablename__ = "product_master"

    id = Column(Integer, primary_key=True)
    SKU_ID = Column(String, index=True)
    Product_Name = Column(String)
    Brand = Column(String)
    Brand_Code = Column(String)
    Category = Column(String)
    Sub_Category = Column(String)
    Pack_Size = Column(String)
    Unit_Of_Measure = Column(String)
    Storage_Type = Column(String)
    Supplier_Name = Column(String)
