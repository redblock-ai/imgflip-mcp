"""
ImgFlip API interaction functions for MCP.
"""

import aiohttp
import json
import logging
import os
from typing import Dict, Any, List

async def get_meme_templates() -> Dict[str, Any]:
    """Get popular meme templates from Imgflip API (used as fallback)"""
    url = "https://api.imgflip.com/get_memes"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                return data
        except aiohttp.ClientError as e:
            logging.error(f"Error connecting to ImgFlip API: {str(e)}")
            return {"success": False, "error_message": f"Connection error: {str(e)}"}
        except json.JSONDecodeError:
            logging.error("Error decoding JSON response from ImgFlip API")
            return {"success": False, "error_message": "Invalid response from ImgFlip API"}
        except Exception as e:
            logging.error(f"Unexpected error getting templates: {str(e)}")
            return {"success": False, "error_message": f"Unexpected error: {str(e)}"}

async def search_meme_templates(query: str, include_nsfw: int = 0) -> Dict[str, Any]:
    """Search for meme templates using the Imgflip Premium API"""
    url = "https://api.imgflip.com/search_memes"
    
    username = os.getenv("IMGFLIP_USERNAME")
    password = os.getenv("IMGFLIP_PASSWORD")
    
    if not username or not password:
        return {
            "success": False, 
            "error_message": "IMGFLIP_USERNAME and IMGFLIP_PASSWORD environment variables are required for premium features"
        }
    
    # Prepare the payload using FormData format
    form_data = aiohttp.FormData()
    form_data.add_field("username", username)
    form_data.add_field("password", password)
    form_data.add_field("query", query)
    form_data.add_field("include_nsfw", str(include_nsfw))
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=form_data) as response:
                data = await response.json()
                
                if not data.get("success"):
                    error_message = data.get("error_message", "Unknown API error")
                    logging.error(f"ImgFlip Search API error: {error_message}")
                    return {"success": False, "error_message": error_message}
                
                return data
    except aiohttp.ClientError as e:
        logging.error(f"Error connecting to ImgFlip API: {str(e)}")
        return {"success": False, "error_message": f"Connection error: {str(e)}"}
    except json.JSONDecodeError:
        logging.error("Error decoding JSON response from ImgFlip API")
        return {"success": False, "error_message": "Invalid response from ImgFlip API"}
    except Exception as e:
        logging.error(f"Unexpected error searching meme templates: {str(e)}")
        return {"success": False, "error_message": f"Unexpected error: {str(e)}"}

async def get_meme_by_id(template_id: str) -> Dict[str, Any]:
    """Get a specific meme template by ID using the Imgflip Premium API"""
    url = "https://api.imgflip.com/get_meme"
    
    username = os.getenv("IMGFLIP_USERNAME")
    password = os.getenv("IMGFLIP_PASSWORD")
    
    if not username or not password:
        return {
            "success": False, 
            "error_message": "IMGFLIP_USERNAME and IMGFLIP_PASSWORD environment variables are required for premium features"
        }
    
    # Prepare the payload using FormData format
    form_data = aiohttp.FormData()
    form_data.add_field("username", username)
    form_data.add_field("password", password)
    form_data.add_field("template_id", template_id)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=form_data) as response:
                if response.status != 200:
                    return {
                        "success": False,
                        "error_message": f"HTTP error: {response.status} - {response.reason}"
                    }
                
                data = await response.json()
                
                if not data.get("success"):
                    error_message = data.get("error_message", "Unknown API error")
                    logging.error(f"ImgFlip Get Meme API error: {error_message}")
                    return {"success": False, "error_message": error_message}
                
                return data
    except aiohttp.ClientError as e:
        logging.error(f"Error connecting to ImgFlip API: {str(e)}")
        return {"success": False, "error_message": f"Connection error: {str(e)}"}
    except json.JSONDecodeError:
        logging.error("Error decoding JSON response from ImgFlip API")
        return {"success": False, "error_message": "Invalid response from ImgFlip API"}
    except Exception as e:
        logging.error(f"Unexpected error getting meme template: {str(e)}")
        return {"success": False, "error_message": f"Unexpected error: {str(e)}"}

async def create_meme_advanced(
    template_id: str, 
    boxes: List[Dict[str, Any]], 
    font: str = "impact", 
    max_font_size: str = "50"
) -> Dict[str, Any]:
    """
    Create a meme using the Imgflip API with advanced options
    
    Args:
        template_id: The ID of the meme template to use
        boxes: List of box objects, each containing text and optional positioning info
        font: Font family to use (default: "impact")
        max_font_size: Maximum font size in pixels (default: "50")
        
    Returns:
        dict: API response with success status and data or error message
    """
    url = "https://api.imgflip.com/caption_image"
    
    username = os.getenv("IMGFLIP_USERNAME")
    password = os.getenv("IMGFLIP_PASSWORD")
    
    if not username or not password:
        return {
            "success": False, 
            "error_message": "IMGFLIP_USERNAME and IMGFLIP_PASSWORD environment variables are required"
        }
    
    # Prepare the payload using FormData format
    form_data = aiohttp.FormData()
    form_data.add_field("template_id", template_id)
    form_data.add_field("username", username)
    form_data.add_field("password", password)
    form_data.add_field("font", font)
    form_data.add_field("max_font_size", max_font_size)
    
    # If there are exactly 2 boxes and they only have text (no positioning),
    # we can use the simpler text0/text1 format for better compatibility
    if len(boxes) == 2 and all(set(box.keys()) == {"text"} for box in boxes):
        form_data.add_field("text0", boxes[0]["text"])
        form_data.add_field("text1", boxes[1]["text"])
    else:
        # Otherwise use the boxes parameter
        for i, box in enumerate(boxes):
            form_data.add_field(f"text{i}", box["text"])
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=form_data) as response:
                # Check HTTP status code first
                if response.status != 200:
                    return {
                        "success": False,
                        "error_message": f"HTTP error: {response.status} - {response.reason}"
                    }
                
                # Parse JSON response
                try:
                    data = await response.json()
                except json.JSONDecodeError:
                    return {
                        "success": False,
                        "error_message": "Invalid JSON response from ImgFlip API"
                    }
                
                # Check if the API returned a success response
                if not data.get("success"):
                    error_message = data.get("error_message", "Unknown API error")
                    logging.error(f"ImgFlip API error: {error_message}")
                    return {"success": False, "error_message": error_message}
                
                # Handle potential missing data in success response
                if "data" not in data or "url" not in data.get("data", {}):
                    return {
                        "success": False,
                        "error_message": "API returned success but no meme URL was provided"
                    }
                
                return data
    except aiohttp.ClientError as e:
        logging.error(f"Error connecting to ImgFlip API: {str(e)}")
        return {"success": False, "error_message": f"Connection error: {str(e)}"}
    except Exception as e:
        logging.error(f"Unexpected error creating meme: {str(e)}")
        return {"success": False, "error_message": f"Unexpected error: {str(e)}"}