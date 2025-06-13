from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Optional
import fastf1
import pandas as pd
import logging
from app.models.schemas import SessionInfo, LapData, DriverStanding

router = APIRouter()
logger = logging.getLogger(__name__)

# @app.get("/")
# def read_root():
#     """Root endpoint with API information"""
#     return {
#         "message": "F1 Data API",
#         "version": "1.0.0",
#         "endpoints": {
#             "session_info": "/session/{year}/{gp}/{session_type}",
#             "lap_times": "/session/{year}/{gp}/{session_type}/laps",
#             "qualifying_results": "/session/{year}/{gp}/qualifying/results",
#             "race_results": "/session/{year}/{gp}/race/results"
#         }
#     }

@router.get("/session/{year}/{gp}/{session_type}", 
    response_model=SessionInfo,
    summary="Get Session Information",
    description="Retrieves basic information about a specific F1 session including date, total laps, and drivers.")
async def get_session_info(
    year: int = Path(..., description="Year of the race", ge=1950, le=2025),
    gp: str = Path(..., description="Name of the Grand Prix"),
    session_type: str = Path(..., description="Type of session (FP1, FP2, FP3, Q, S, R)")
):
    """Get basic session information"""
    try:
        logger.info(f"Fetching session: {year} {gp} {session_type}")
        
        # Load session data
        session = fastf1.get_session(year, gp, session_type)
        session.load()
        
        # Get driver list
        drivers = session.drivers.to_list() if hasattr(session, 'drivers') else []
        driver_names = []
        
        for driver in drivers:
            try:
                driver_info = session.get_driver(driver)
                driver_names.append(f"{driver_info['Abbreviation']} - {driver_info['FullName']}")
            except:
                driver_names.append(str(driver))
        
        return SessionInfo(
            session_name=f"{year} {gp} {session_type}",
            date=session.date.strftime("%Y-%m-%d") if session.date else "Unknown",
            total_laps=len(session.laps),
            drivers=driver_names
        )
        
    except Exception as e:
        logger.error(f"Error fetching session info: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error fetching session: {str(e)}")

@router.get("/session/{year}/{gp}/{session_type}/laps",
    response_model=List[LapData],
    summary="Get Lap Times",
    description="Retrieves lap times and sector times for a specific session. Can be filtered by driver.")
async def get_lap_times(
    year: int = Path(..., description="Year of the race", ge=1950, le=2025),
    gp: str = Path(..., description="Name of the Grand Prix"),
    session_type: str = Path(..., description="Type of session (FP1, FP2, FP3, Q, S, R)"),
    driver: Optional[str] = Query(None, description="Driver abbreviation (e.g., HAM, VER)")
):
    """Get lap times for a session, optionally filtered by driver"""
    try:
        logger.info(f"Fetching lap times: {year} {gp} {session_type} driver:{driver}")
        
        session = fastf1.get_session(year, gp, session_type)
        session.load()
        
        laps = session.laps
        
        # Filter by driver if specified
        if driver:
            laps = laps[laps['Driver'] == driver.upper()]
        
        # Convert to list of dictionaries
        lap_data = []
        for _, lap in laps.iterrows():
            lap_data.append(LapData(
                driver=lap['Driver'],
                lap_number=int(lap['LapNumber']),
                lap_time=str(lap['LapTime']) if pd.notna(lap['LapTime']) else None,
                sector_1=str(lap['Sector1Time']) if pd.notna(lap['Sector1Time']) else None,
                sector_2=str(lap['Sector2Time']) if pd.notna(lap['Sector2Time']) else None,
                sector_3=str(lap['Sector3Time']) if pd.notna(lap['Sector3Time']) else None
            ))
        
        return lap_data[:100]  # Limit to first 100 laps to avoid huge responses
        
    except Exception as e:
        logger.error(f"Error fetching lap times: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error fetching lap times: {str(e)}")

@router.get("/session/{year}/{gp}/qualifying/results",
    response_model=List[DriverStanding],
    summary="Get Qualifying Results",
    description="Retrieves the final qualifying results including positions and best lap times.")
async def get_qualifying_results(
    year: int = Path(..., description="Year of the race", ge=1950, le=2025),
    gp: str = Path(..., description="Name of the Grand Prix")
):
    """Get qualifying results"""
    try:
        logger.info(f"Fetching qualifying results: {year} {gp}")
        
        session = fastf1.get_session(year, gp, 'Q')
        session.load()
        
        results = session.results
        standings = []
        
        for _, driver in results.iterrows():
            standings.append(DriverStanding(
                position=int(driver['Position']) if pd.notna(driver['Position']) else 0,
                driver=f"{driver['Abbreviation']} - {driver['FullName']}",
                team=driver['TeamName'] if pd.notna(driver['TeamName']) else "Unknown",
                time=str(driver['Q3']) if pd.notna(driver['Q3']) else str(driver['Q2']) if pd.notna(driver['Q2']) else str(driver['Q1']) if pd.notna(driver['Q1']) else None
            ))
        
        return sorted(standings, key=lambda x: x.position)
        
    except Exception as e:
        logger.error(f"Error fetching qualifying results: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error fetching qualifying results: {str(e)}")

@router.get("/session/{year}/{gp}/race/results",
    response_model=List[DriverStanding],
    summary="Get Race Results",
    description="Retrieves the final race results including positions and race times.")
async def get_race_results(
    year: int = Path(..., description="Year of the race", ge=1950, le=2025),
    gp: str = Path(..., description="Name of the Grand Prix")
):
    """Get race results"""
    try:
        logger.info(f"Fetching race results: {year} {gp}")
        
        session = fastf1.get_session(year, gp, 'R')
        session.load()
        
        results = session.results
        standings = []
        
        for _, driver in results.iterrows():
            standings.append(DriverStanding(
                position=int(driver['Position']) if pd.notna(driver['Position']) else 0,
                driver=f"{driver['Abbreviation']} - {driver['FullName']}",
                team=driver['TeamName'] if pd.notna(driver['TeamName']) else "Unknown",
                time=str(driver['Time']) if pd.notna(driver['Time']) else "DNF"
            ))
        
        return sorted(standings, key=lambda x: x.position)
        
    except Exception as e:
        logger.error(f"Error fetching race results: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error fetching race results: {str(e)}")