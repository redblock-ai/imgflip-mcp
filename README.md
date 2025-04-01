# MCP: Meme Creation Platform

![MCP Banner](https://i.imgflip.com/9pbq4t.jpg)

A Meme Creation Protocol server for Claude and other AI assistants. Released on April 1st, 2025 because... memes.

## What is MCP?

MCP provides AI models with the ability to create and share memes using the Imgflip API. 
It implements the Model Control Protocol (MCP) to allow seamless integration with Claude and other AI assistants.

## Features

- 🚀 Create memes from description, AI chooses its own meme
- 🎯 Create meme for a specific template from description
- 🌟 Create meme from popular memes (works for non-premium API access accounts)



### Installation

```bash
# Ensure you have uv installed (https://docs.astral.sh/uv/getting-started/installation/)
git clone https://github.com/redblock-ai/imgflip-mcp.git
cd imgflip-mcp
uv sync --dev --all-extras
uv run imgflip-mcp # Just to test. NOT needed for the rest of instructions here... it will be set by claude computer.
```

#### Imgflip API Credentials

```bash
# Create a `.env` file in the root directory of the project and add your Imgflip API credentials:
IMGFLIP_USERNAME="YOUR_IMGFLIP_USERNAME"
IMGFLIP_PASSWORD="YOUR_IMGFLIP_PASSWORD"
```

#### Integrate with Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`

On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
<summary>Get environment details to update the `claude_desktop_config` file</summary>

- To retrieve the environment details:
   1. Run the following command in your terminal:
      ```bash
      npx @modelcontextprotocol/inspector uv --directory <PATH_TO_PROJECT_DIR> run imgflip-mcp
      ```
   2. Open the MCP Inspector on localhost.
   
   3. Click on Connect.
   
   4. Copy the output environment key from the terminal.

You can install and use the MCP Inspector via npm if needed.
</details> 


<details>
  <summary>Development/Unpublished Servers Configuration</summary>

  ```bash
  "mcpServers": {
    "imgflip-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "<PATH_TO_PROJECT_DIR>",
        "run",
        "imgflip-mcp"
      ],
      "env": {
       <content from env key in mcp inspector terminal response>
      }
    }
  }
```
</details> 

<details>
  <summary>Development/Unpublished Servers Configuration if MCP server is hosted in WSL</summary>
  
  ```bash
  "mcpServers": {
    "imgflip-mcp": {
      "command": "wsl.exe",
        "args": [
            "bash",
            "-c",
            "PATH_TO_UV_BIN --directory <PATH_TO_PROJECT_DIR> run imgflip-mcp"
        ],
    }
  }
  ```

</details>

<details>
  <summary>Published Servers Configuration</summary>

  ```bash
  "mcpServers": {
    "imgflip-mcp": {
      "command": "uvx",
      "args": [
        "imgflip-mcp"
      ]
    }
  }
  ```

</details>



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


## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory <PATH_TO_PROJECT_DIR> run imgflip-mcp
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.


## License

MIT License

## Acknowledgements

- All the meme creators who have contributed to internet culture
- [Imgflip API](https://imgflip.com/api)
- [Model Control Protocol](https://github.com/modelcontextprotocol/python-sdk)

---

Built with ❤️ and 😂  
Released on April 1st, 2025