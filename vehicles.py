import json
from fillrite import api_get, mcp


# @mcp.tool()
def get_all_vehicles() -> str:
    return json.dumps(
        api_get("vehicle", "application/x-www-form-urlencoded")["result"], indent=2
    )


# @mcp.tool()
def get_all_vehicles_filtered():
    pass


# @mcp.tool()
def get_vehicle_detail(vehicle_id: int):
    return json.dumps(
        api_get(f"vehicle/{vehicle_id}", "application/x-www-form-urlencoded")["result"],
        indent=2,
    )
