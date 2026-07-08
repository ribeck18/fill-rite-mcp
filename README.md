# Fill-Rite MCP 

This project is an MCP to allow agents to interact with a users Fill-Rite.

## Tokens
Fill-Rite access tokens go stale in 30 minutes, and refresh tokens go stale in 7 days. You must run the `refresh_tokens()` function at least once per week (before the 7 days are up!) otherwise you will need to add new tokens to your tokens.json file.

Tokens are checked for staleness at every tool call, and refreshed if needed, so as long as the mcp is used once per week you will be fine.

You could also set up a cron job to refresh your token ever 3-4 days, or you could set a scheduled prompt on your AI Agent that makes any tool call in this MCP at least once per week.


