# MCP: Meme Creation Platform

![MCP Banner](https://i.imgflip.com/9p7wqm.jpg)

A Meme Creation Protocol server for Claude and other AI assistants. Released on April 1st, 2025 because... memes.

## What is MCP?

MCP provides AI models with the ability to create and share memes using the Imgflip API. 
It implements the Model Control Protocol (MCP) to allow seamless integration with Claude and other AI assistants.

## Features

- 🔍 Search for meme templates using keywords
- 🧠 Get template information including box count
- 🎨 Create memes with custom text
- 💡 Generate search terms for meme concepts
- 🚀 Create memes from concept descriptions

## Setup

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/imgflip-mcp.git

# Install dependencies
pip install -r requirements.txt
```

### Imgflip API Credentials

```bash
# Set your Imgflip credentials
export IMGFLIP_USERNAME="your_username"
export IMGFLIP_PASSWORD="your_password"
```

### Running the Server

```bash
python -m src.server
```

## Configuring Claude Desktop

To connect Claude Desktop to your MCP server:

1. Open Claude Desktop
2. Click on the settings icon (⚙️) in the top right
3. Select "Extensions"
4. Click "Add Extension"
5. Add the following configuration:

```json
{
  "name": "imgflip-mcp",
  "description": "Meme Creation Platform using Imgflip API",
  "logo": "https://imgflip.com/favicon.ico",
  "contactInfo": "your@email.com",
  "server": {
    "type": "subprocess",
    "command": "python",
    "args": ["-m", "src.server"]
  }
}
```

6. Click "Save"
7. Restart Claude Desktop

## Using MCP with Claude

Once configured, you can ask Claude to create memes:

```
Create a meme using the "Drake" template with "Writing code" and "Making memes" as text.
```

or

```
Make a meme about debugging code for hours only to find a simple typo.
```

## Available Tools

| Tool | Description |
|------|-------------|
| `imgflip_search_memes` | Search for meme templates |
| `imgflip_get_template_info` | Get template details |
| `imgflip_create_meme` | Create a meme with custom text |
| `imgflip_generate_search_terms` | Generate search terms for concepts |
| `imgflip_create_from_concept` | Create a meme from a concept |

## License

MIT License

## Acknowledgements

- [Imgflip API](https://imgflip.com/api)
- [Model Control Protocol](https://github.com/anthropics/model-control-protocol)

---

Built with ❤️ and 😂  
Released on April 1st, 2025
