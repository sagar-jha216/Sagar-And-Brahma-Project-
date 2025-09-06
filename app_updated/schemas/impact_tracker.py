from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class ImpactTrackerFilterParams(BaseModel):
    region: Optional[str] = Field(None, alias="region")
    store_ids: Optional[List[str]] = Field(None, alias="selectedStores") 
    channels: Optional[List[str]] = Field(None, alias="selectedChannels")
    selected_date: Optional[date] = Field(None, alias="selectedDate")

    class Config:
        allow_population_by_field_name = True

class SummaryComparison(BaseModel):
    percentage: float
    trend_direction: str
    compare_to: str

class SummaryData(BaseModel):
    todays_loss_mitigation: int
    todays_loss_mitigation_comparison: SummaryComparison
    month_to_date_loss_mitigation: int
    month_to_date_loss_mitigation_comparison: SummaryComparison
    year_to_date_loss_mitigation: int
    year_to_date_loss_mitigation_comparison: SummaryComparison
    shrinkage_alerts_triggered: int
    avg_time_for_resolution: int
    incident_frequency: int

class ChartDataPoint(BaseModel):
    date: Optional[str] = None
    store: Optional[str] = None
    value: int

class ShrinkReportRow(BaseModel):
    date: str
    store: str
    shrinkage_type: str
    estimated_loss: int
    root_cause: str
    action_taken: str
    impact_score: int
    follow_up_date: str

class ImpactTrackerResponse(BaseModel):
    summary: SummaryData
    last_7_days_loss_mitigation: List[ChartDataPoint]
    monthly_loss_mitigation_per_store: List[ChartDataPoint]
    weekly_shrink_report: List[ShrinkReportRow]