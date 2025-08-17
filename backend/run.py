#!/usr/bin/env python3
"""
ShrinkSense Backend Startup Script
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.config import get_settings

def main():
    """Main entry point for the application"""
    settings = get_settings()
    
    print(f"🚀 Starting {settings.APP_NAME} v{settings.VERSION}")
    print(f"📡 Server: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 API Docs: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"🔧 Debug Mode: {settings.DEBUG}")
    
    # Check if Excel files exist for migration
    excel_files = [
        settings.EXCEL_FILE_PATH,
        settings.KPI_FILE_PATH,
        settings.REMEDIATION_FILE_PATH,
        settings.RETURN_REMEDIATION_FILE_PATH,
        settings.SHRINKAGE_RETURN_KPIS_FILE_PATH
    ]
    
    existing_files = [f for f in excel_files if f and os.path.exists(f)]
    if existing_files:
        print(f"📊 Found {len(existing_files)} Excel files for migration")
    else:
        print("⚠️  No Excel files found - migration will be skipped")
    
    print("-" * 50)
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1  # Single worker to prevent migration conflicts
    )

if __name__ == "__main__":
    main()