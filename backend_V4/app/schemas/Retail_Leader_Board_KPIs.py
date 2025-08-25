from pydantic import BaseModel

class RetailKPIBase(BaseModel):
    category: str
    inventory_accuracy: float
    damage_percent: float
    dump_percent: float
    expired_percent: float
    aged_percent: float
    return_percent: float

class RetailKPICreate(RetailKPIBase):
    pass

class RetailKPIResponse(RetailKPIBase):
    id: int

    class Config:
        orm_mode = True
