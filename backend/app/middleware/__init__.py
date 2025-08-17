"""
Middleware package for ShrinkSense Backend
"""

from .auth import verify_token

__all__ = ["verify_token"]