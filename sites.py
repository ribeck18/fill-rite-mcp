import json
from fillrite import api_get, mcp


@mcp.tool()
def get_all_sites():
    return json.dumps(
        api_get("site", "application/x-www-form-urlencoded")["result"],
        indent=2,
    )


@mcp.tool()
def get_site_details(site_id: int):
    return json.dumps(
        api_get(f"site/{site_id}", "application/x-www-form-urlencoded")["result"],
        indent=2,
    )
