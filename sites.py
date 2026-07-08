from fillrite import api_get, mcp


@mcp.tool()
def get_all_sites():
    return api_get("site", "application/x-www-form-urlencoded")["result"]


@mcp.tool()
def get_site_details(site_id: int):
    return api_get(f"site/{site_id}", "application/x-www-form-urlencoded")["result"]
