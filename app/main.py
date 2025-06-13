from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
import fastf1
import logging
from app.api import sessions
from app.api.health import router as health_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="F1 Data API",
    description="A FastAPI backend for Formula 1 data using Fast F1 library",
    version="1.0.0",
    docs_url=None,  # Disable default docs
    redoc_url=None  # Disable default redoc
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enable Fast F1 cache
fastf1.Cache.enable_cache('cache')

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="F1 Data API",
        version="1.0.0",
        description="A FastAPI backend for Formula 1 data using Fast F1 library",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
    )

# Include routers with tags
app.include_router(sessions.router, prefix="/api", tags=["Sessions"])
app.include_router(health_router, prefix="/api", tags=["Health"])

@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "F1 Data API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "session_info": "/api/session/{year}/{gp}/{session_type}",
            "lap_times": "/api/session/{year}/{gp}/{session_type}/laps",
            "qualifying_results": "/api/session/{year}/{gp}/qualifying/results",
            "race_results": "/api/session/{year}/{gp}/race/results"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)