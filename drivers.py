import json
from fillrite import api_get, mcp


@mcp.tool()
def get_all_drivers():
    return json.dumps(
        api_get("driver", "application/x-www-form-urlencoded")["result"],
        indent=2,
    )


@mcp.tool()
def get_driver_detail(driver_id: int):
    return json.dumps(
        api_get(f"driver/{driver_id}", "application/x-www-form-urlencoded")["result"],
        indent=2,
    )
