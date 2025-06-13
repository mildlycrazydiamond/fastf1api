from pydantic import BaseModel
from typing import List, Optional

class SessionInfo(BaseModel):
    session_name: str
    date: str
    total_laps: int
    drivers: List[str]

class LapData(BaseModel):
    driver: str
    lap_number: int
    lap_time: Optional[str]
    sector_1: Optional[str]
    sector_2: Optional[str]
    sector_3: Optional[str]
    
class DriverStanding(BaseModel):
    position: int
    driver: str
    team: str
    time: Optional[str]