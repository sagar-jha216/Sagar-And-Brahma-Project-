#!/usr/bin/env python3
"""
Database cleanup script for ShrinkSense
Removes conflicting database files and allows fresh start
"""

import os
import sys
from pathlib import Path

def cleanup_databases():
    """Remove existing database files"""
    db_files = [
        "shrinksense.db",
        "shrinksense_new.db", 
        "shrinksense_inventory.sqlite",
        "shrink_sense.db"
    ]
    
    removed_count = 0
    for db_file in db_files:
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                print(f"✅ Removed {db_file}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Failed to remove {db_file}: {e}")
        else:
            print(f"⏭️  {db_file} not found")
    
    if removed_count > 0:
        print(f"\n🧹 Cleaned up {removed_count} database files")
        print("✨ Ready for fresh start!")
    else:
        print("\n💡 No database files to clean")

if __name__ == "__main__":
    print("🧹 ShrinkSense Database Cleanup")
    print("-" * 30)
    cleanup_databases()
    print("\nNow run: python run.py")