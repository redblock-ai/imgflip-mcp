from . import server
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)

def main():
    """Main entry point for the package."""
    asyncio.run(server.main())

# Optionally expose other important items at package level
__all__ = ['main', 'server']