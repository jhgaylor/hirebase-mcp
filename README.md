# HireBase MCP Server

A Model Context Protocol (MCP) server providing tools to interact with the HireBase Job API.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- MCP Tools for searching jobs (`search_jobs`) and retrieving job details (`get_job`) from the HireBase API.
- MCP Prompt (`create_candidate_profile`) to assist in generating job search strategies.

## Setup

1. Install `uv` if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create a new virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS

# Install dependencies
uv pip install -e .
```

## Running the Server

Start the server with:
```bash
python -m mcp_server
```

## Available MCP Interactions

This server exposes the following MCP interactions:

### Tools

*   `search_jobs`: Search for jobs using the HireBase API based on various criteria (keywords, title, location, salary, etc.).
    *   *Parameters*: `query`, `and_keywords`, `or_keywords`, `not_keywords`, `title`, `category`, `country`, `city`, `location_type`, `company`, `salary_from`, `salary_to`, `salary_currency`, `years_from`, `years_to`, `visa`, `limit`.
*   `get_job`: Retrieve detailed information about a specific job using its HireBase ID.
    *   *Parameters*: `job_id`.

### Prompts

*   `create_candidate_profile`: Generates a structured prompt based on candidate details (name, LinkedIn, website, resume text) to help guide job searching.
    *   *Parameters*: `name`, `linkedin_url`, `personal_website`, `resume_text`.

## Development

This project uses:
- `uv` for dependency management and virtual environments
- `ruff` for linting and formatting
- `hatch` as the build backend

### Common Tasks

```bash
# Update dependencies
uv pip compile pyproject.toml -o requirements.txt

# Run linting
ruff check .

# Format code
ruff format .
```

## Client Setup (Examples: Claude Desktop, Cursor)

To use this server with an MCP client like Claude Desktop or Cursor, you need to configure the client to run the server process and optionally provide the HireBase API key.

1.  **Ensure `uv` is installed:** See [Setup](#setup).
2.  **Obtain a HireBase API Key (optional):** Request a key from [HireBase](https://hirebase.org/) You can set this as an environment variable (`HIREBASE_API_KEY`).
3.  **Configure your client:**

    *   **Using `uvx` (Recommended for simplicity):**
        *   **Claude Desktop:** Edit your `claude_desktop_config.json`:
            ```json
            {
              "mcpServers": {
                "hirebase": { // Choose a name for the server
                  "command": "uvx",
                  "args": [
                    // Assuming your package is named 'hirebase-mcp'
                    // If you haven't published it, you might need to point to the local path
                    // e.g., "--path", "." if running from the project root
                    "hirebase-mcp" 
                  ],
                  "env": {
                    "HIREBASE_API_KEY": "your-hirebase-api-key-here" 
                  }
                }
                // ... other servers
              }
            }
            ```
        *   **Cursor:** Go to Settings > MCP > Add Server:
            *   **Mac/Linux Command:** `uvx hirebase-mcp` (Adjust package name if needed)
            *   **Windows Command:** `cmd`
            *   **Windows Args:** `/c`, `uvx`, `hirebase-mcp` (Adjust package name if needed)
            *   Set the `HIREBASE_API_KEY` environment variable in the appropriate section.

    *   **Running from source via Python (Alternative):**
        *   This requires the environment to be set up as per the [Setup](#setup) section.
        *   **Claude Desktop:** Edit your `claude_desktop_config.json`:
            ```json
            {
              "mcpServers": {
                "hirebase": { 
                  "command": "python", 
                  "args": [
                    "-m", "mcp_server" // Assumes running from the project root
                  ],
                  "env": {
                    "HIREBASE_API_KEY": "your-hirebase-api-key-here" 
                  }
                }
                // ... other servers
              }
            }
            ```

*Replace `"your-hirebase-api-key-here"` with your actual HireBase API key.*
*Adjust the package name (`hirebase-mcp`) or paths if necessary based on your project setup.*

## Environment Variables

-   `HIREBASE_API_KEY` (**required**): Your API key for accessing the HireBase API. The server needs this to make authenticated requests for job data.

## Testing

This project uses `pytest` for testing the core tool logic. Tests mock external API calls using `unittest.mock`.

1. Install test dependencies:
```bash
# Ensure you are in your activated virtual environment (.venv)
uv pip install -e '.[test]'
```

2. Run tests:
```bash
# Example command
pytest
```

## Contributing

Contributions are welcome.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 