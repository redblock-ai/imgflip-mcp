"""
MCP Server for Meme Creation Platform.

This server provides tools for creating memes using the Imgflip API
through the Model Control Protocol (MCP).
"""

import os
import sys
import json
import asyncio
import logging
import mcp.server.stdio
import mcp.types as types
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server

from src import api

# Initialize the MCP server
server = Server("imgflip-mcp")

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """
    List available prompts.
    Each prompt can have optional arguments to customize its behavior.
    """
    return [
        types.Prompt(
            name="imgflip_create_meme",
            description="Create a meme using Imgflip with a specified template and text",
            arguments=[
                types.PromptArgument(
                    name="template_name",
                    description="The name of the meme template to use",
                    required=True,
                ),
                types.PromptArgument(
                    name="text_boxes",
                    description="The text to display in each box (comma-separated)",
                    required=True,
                ),
            ],
        ),
        types.Prompt(
            name="imgflip_create_from_description",
            description="Create a meme from a description of the meme concept",
            arguments=[
                types.PromptArgument(
                    name="description",
                    description="A description of the meme concept or idea",
                    required=True,
                ),
            ],
        )
    ]


@server.get_prompt()
async def handle_get_prompt(
    name: str, arguments: dict[str, str] | None
) -> types.GetPromptResult:
    """
    Generate a prompt by combining arguments with server state.
    """
    if name == "imgflip_create_meme":
        template_name = (arguments or {}).get("template_name", "")
        text_boxes = (arguments or {}).get("text_boxes", "")
        
        return types.GetPromptResult(
            description=f"Create a meme with the {template_name} template",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Create a meme using the '{template_name}' template with the following text boxes:\n{text_boxes}",
                    ),
                ),
            ],
        )
    elif name == "imgflip_create_from_description":
        description = (arguments or {}).get("description", "")
        
        return types.GetPromptResult(
            description=f"Create a meme based on the concept: {description}",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"I want to create a meme that captures this idea or concept: {description}\n\nPlease analyze this concept and determine appropriate meme templates that would work well for it. Then select the best one and generate suitable captions.",
                    ),
                ),
            ],
        )
    else:
        raise ValueError(f"Unknown prompt: {name}")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List all available tools provided by this MCP server."""
    return [
        types.Tool(
            name="imgflip_search_memes",
            description="Search for meme templates using keywords",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query for meme templates"},
                    "include_nsfw": {"type": "boolean", "description": "Include NSFW memes in results", "default": False}
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="imgflip_get_template_info",
            description="Get information about a meme template including the number of text boxes required",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_id": {"type": "string", "description": "ID of the meme template to get info for"}
                },
                "required": ["template_id"],
            },
        ),
        types.Tool(
            name="imgflip_create_meme",
            description="Create a meme using the Imgflip API with custom text for any number of boxes",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_id": {
                        "type": "string", 
                        "description": "ID of the meme template from get_memes"
                    },
                    "text_boxes": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "Array of text strings, one for each text box in the template"
                    },
                    "font": {
                        "type": "string", 
                        "enum": ["impact", "arial"],
                        "description": "Font family to use (defaults to impact)",
                        "default": "impact"
                    },
                    "max_font_size": {
                        "type": "string",
                        "description": "Maximum font size in pixels (defaults to 50px)",
                        "default": "50"
                    }
                },
                "required": ["template_id", "text_boxes"],
            },
        ),
        types.Tool(
            name="imgflip_generate_search_terms",
            description="Generate optimal search terms for a meme concept",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {"type": "string", "description": "Description of the meme concept or idea"}
                },
                "required": ["description"],
            },
        ),
        types.Tool(
            name="imgflip_create_from_concept",
            description="Create a meme from a concept by searching templates and generating captions",
            inputSchema={
                "type": "object",
                "properties": {
                    "concept": {"type": "string", "description": "The meme concept or idea"},
                    "include_nsfw": {"type": "boolean", "description": "Include NSFW memes in results", "default": False}
                },
                "required": ["concept"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(
    name: str, arguments: dict
) -> list[types.TextContent | types.EmbeddedResource]:
    """Handle tool calls from the LLM"""
    
    if name == "imgflip_search_memes":
        query = arguments["query"]
        include_nsfw = 1 if arguments.get("include_nsfw", False) else 0
        
        result = await api.search_meme_templates(query, include_nsfw)
        
        # If search fails, fallback to popular memes
        if not result.get("success"):
            fallback_result = await api.get_meme_templates()
            if fallback_result.get("success"):
                fallback_result["message"] = "Search failed, showing popular templates instead"
                return [types.TextContent(type="text", text=json.dumps(fallback_result, indent=2))]
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "imgflip_get_template_info":
        template_id = arguments["template_id"]
        
        result = await api.get_meme_by_id(template_id)
        
        if result.get("success"):
            # Extract just the template info
            template_info = result.get("data", {}).get("meme", {})
            
            # Add helpful text about box count
            box_count = template_info.get("box_count", 0)
            box_guidance = f"This template requires {box_count} text boxes."
            
            if box_count == 2:
                box_guidance += " This is a standard meme template with top and bottom text."
            elif box_count == 1:
                box_guidance += " This template has only one text area."
            elif box_count > 2:
                box_guidance += f" You'll need to provide {box_count} different text strings for this template."
                
            return [types.TextContent(
                type="text", 
                text=f"Template Information:\n{json.dumps(template_info, indent=2)}\n\n{box_guidance}"
            )]
        else:
            return [types.TextContent(
                type="text", 
                text=f"Error getting template info: {result.get('error_message', 'Unknown error')}"
            )]
    
    elif name == "imgflip_create_meme":
        template_id = arguments["template_id"]
        text_boxes = arguments["text_boxes"]
        font = arguments.get("font", "impact")
        max_font_size = arguments.get("max_font_size", "50")
        
        # Get template info to check box count
        template_info = await api.get_meme_by_id(template_id)
        if template_info.get("success"):
            required_box_count = template_info.get("data", {}).get("meme", {}).get("box_count", 2)
            provided_box_count = len(text_boxes)
            
            # If too few boxes provided, warn but proceed (empty boxes will be used)
            if provided_box_count < required_box_count:
                logging.warning(f"Template requires {required_box_count} text boxes, but only {provided_box_count} provided. Empty boxes will be used for remaining positions.")
                
                # Pad the text_boxes array with empty strings
                text_boxes = text_boxes + [""] * (required_box_count - provided_box_count)
                
            # If too many boxes provided, truncate and warn
            elif provided_box_count > required_box_count:
                logging.warning(f"Template only supports {required_box_count} text boxes, but {provided_box_count} provided. Extra boxes will be ignored.")
                text_boxes = text_boxes[:required_box_count]
        
        # Create boxes array for API call
        boxes = [{"text": text} for text in text_boxes]
        
        result = await api.create_meme_advanced(template_id, boxes, font, max_font_size)
        
        # If the API call was successful and we have a URL
        if result.get("success") and result.get("data", {}).get("url"):
            meme_url = result["data"]["url"]
            page_url = result["data"]["page_url"]
            
            # Build a response with template info if available
            response_text = "Meme created successfully!\n\n"
            
            if template_info.get("success"):
                template_name = template_info.get("data", {}).get("meme", {}).get("name", "Unknown template")
                response_text += f"Template: {template_name}\n"
            
            response_text += "\nText boxes:\n"
            for i, text in enumerate(text_boxes):
                response_text += f"{i+1}. {text}\n"
                
            response_text += f"\nDirect image URL: {meme_url}\nPage URL: {page_url}\n\n"
            response_text += "To view the meme, please open the URL in your browser or display it using HTML with an img tag."
            
            return [types.TextContent(type="text", text=response_text)]
        else:
            # Return error information
            error_message = result.get("error_message", "Unknown error")
            return [types.TextContent(type="text", text=f"Error creating meme: {error_message}")]
    
    elif name == "imgflip_generate_search_terms":
        description = arguments["description"]
        
        search_prompt = f"""
Concept: {description}
I need to search for meme templates on Imgflip that would work well for this concept.
IMPORTANT: The Imgflip search API is very basic and only searches for exact matches in template names.
It does NOT understand complex queries, concepts, or smart search.
Please provide 1-3 extremely simple search terms that are likely to be part of actual meme template names.
These should be:
- Single words when possible (like "confused", "drake", "cat", "distracted")
- Common meme character names (like "doge", "batman", "pikachu")
- Well-known meme format names (like "drake", "change my mind", "distracted")
DO NOT provide:
- Phrases or complete sentences
- Complex descriptions
- Conceptual terms that wouldn't appear in a template name
Examples:
- For "when your code finally works but you don't know why" → "success", "confused", "math"
- For "me explaining something complex to my parents" → "explain", "pointing", "confused"
Respond with ONLY the search terms, separated by commas, no additional text or explanation.
"""
        return [types.TextContent(type="text", text=search_prompt)]
    
    elif name == "imgflip_create_from_concept":
        concept = arguments["concept"]
        include_nsfw = arguments.get("include_nsfw", False)
        
        # First use the search query generation prompt
        search_prompt = f"""
Concept: {concept}
I need to search for meme templates on Imgflip that would work well for this concept.
IMPORTANT: The Imgflip search API is very basic and only searches for exact matches in template names.
It does NOT understand complex queries, concepts, or smart search.
Please provide 1-3 extremely simple search terms that are likely to be part of actual meme template names.
These should be:
- Single words when possible (like "confused", "drake", "cat", "distracted")
- Common meme character names (like "doge", "batman", "pikachu")
- Well-known meme format names (like "drake", "change my mind", "distracted")
DO NOT provide:
- Phrases or complete sentences
- Complex descriptions
- Conceptual terms that wouldn't appear in a template name
Examples:
- For "when your code finally works but you don't know why" → "success", "confused", "math"
- For "me explaining something complex to my parents" → "explain", "pointing", "confused"
Respond with ONLY the search terms, separated by commas, no additional text or explanation.
"""
        # This is a placeholder for the LLM to generate search terms
        # In a real implementation, this would call the LLM and get the response
        return [types.TextContent(type="text", text=search_prompt)]
            
    raise ValueError(f"Tool not found: {name}")


async def main():
    """Main entry point for the MCP server"""
    # Check for required environment variables
    username = os.getenv("IMGFLIP_USERNAME")
    password = os.getenv("IMGFLIP_PASSWORD")
    
    if not username or not password:
        logging.warning("IMGFLIP_USERNAME and IMGFLIP_PASSWORD environment variables are required")
        logging.warning("Without them, you won't be able to create memes")
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="imgflip-mcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def cli():
    """CLI entry point for imgflip-mcp"""
    logging.basicConfig(level=logging.INFO)
    # Check for environment variables
    username = os.getenv("IMGFLIP_USERNAME")
    password = os.getenv("IMGFLIP_PASSWORD")
    
    if not username or not password:
        print(
            "Warning: IMGFLIP_USERNAME and IMGFLIP_PASSWORD environment variables are required",
            file=sys.stderr,
        )
        print(
            "Without them, you won't be able to create memes",
            file=sys.stderr,
        )
    
    # Display welcome message
    logging.info("Starting Imgflip MCP Server")
    logging.info("This server provides tools for meme generation using the Imgflip API")
    logging.info("")
    logging.info("Available tools:")
    logging.info(" • imgflip_search_memes - Search for meme templates using keywords")
    logging.info(" • imgflip_get_template_info - Get info about template including required box count")
    logging.info(" • imgflip_create_meme - Create a meme with custom text")
    logging.info(" • imgflip_generate_search_terms - Generate optimal search terms for a meme concept")
    logging.info(" • imgflip_create_from_concept - Create a meme from a concept description")
    logging.info("")
    logging.info("API Requirements:")
    logging.info("Set your IMGFLIP_USERNAME and IMGFLIP_PASSWORD as environment variables")
    asyncio.run(main())


if __name__ == "__main__":
    cli()