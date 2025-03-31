"""
MCP: Meme Creation Platform

A Model Control Protocol server for creating memes with the Imgflip API.
"""

__version__ = "1.0.0"

from dotenv import load_dotenv
found_env_file = load_dotenv(override=True)  # take environment variables

if found_env_file:
    print("Environment variables loaded from .env file.")
else:
    print("No .env file found. Using system environment variables.")