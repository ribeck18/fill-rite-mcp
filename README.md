# Fill-Rite MCP

This project is an MCP to allow agents to interact with a user's Fill-Rite.

## Access Tokens

Fill-Rite access tokens go stale in 30 minutes, and refresh tokens go stale in 7 days. You must run the `refresh_tokens()` function at least once per week (before the 7 days are up!) otherwise you will need to add new tokens to your `tokens.json` file.

Tokens are checked for staleness at every tool call, and refreshed if needed, so as long as the MCP is used once per week you will be fine.

You could also set up a cron job to refresh your token every 3-4 days, or you could set a scheduled prompt on your AI agent that makes any tool call in this MCP at least once per week.

## Setup

I have only tested this on macOS, and these setup steps assume you use macOS. In the future I plan to write an install script that will make setup simple.

### Claude Code

1. Navigate to the directory you want to run the MCP in and clone the repo:

```
   git clone https://github.com/ribeck18/fill-rite-mcp.git
```

2. Register the MCP with Claude Code:

```
   claude mcp add fillrite -- uv run --directory {path_to_repo} main.py
```

3. In the directory you just cloned, make a new file called `tokens.json`. Paste the following into it, replacing the placeholders with your API tokens from Fill-Rite:

```json
   {
       "access_token": {
           "token": "{your_access_token}",
           "expires_at": ""
       },
       "refresh_token": {
           "token": "{your_refresh_token}"
       }
   }
```

   Make sure your access token starts with "Bearer ". Leave `expires_at` blank for now.

4. In the same directory, make a file called `.env`. Paste the following into it:

```
   BASE_URL=https://fmsapi.fillrite.com/rest/v1.0/
```

Your MCP should now function properly in Claude Code.

### Claude Desktop

1. Navigate to the directory you want to run the MCP in and clone the repo:

```
   git clone https://github.com/ribeck18/fill-rite-mcp.git
```

2. In the directory you just cloned, make a new file called `tokens.json`. Paste the following into it, replacing the placeholders with your API tokens from Fill-Rite:

```json
   {
       "access_token": {
           "token": "{your_access_token}",
           "expires_at": ""
       },
       "refresh_token": {
           "token": "{your_refresh_token}"
       }
   }
```

   Make sure your access token starts with "Bearer ". Leave `expires_at` blank for now.

3. In the same directory, make a file called `.env`. Paste the following into it:

```
   BASE_URL=https://fmsapi.fillrite.com/rest/v1.0/
```

4. Navigate to your claude desktop config file. If it does not exist, create it.

```
    ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

5. Add the following to that file.

```
    {
        "mcpServers": {
            "Fill-Rite": {
                "command": "{path_to_uv}",
                "args": [
                    "run",
                    "--directory",
                    "{path_to_cloned_repo}",
                    "main.py"
                ]
            }
        }
    }
```

Your path to uv can be found with `which uv`.

6. Restart your Claude Desktop app. After restart the MCP should function.
