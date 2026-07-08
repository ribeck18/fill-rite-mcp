import json
from fillrite import api_get, api_patch, mcp


@mcp.tool()
def get_all_tanks() -> str:
    return api_get("tank", "application/x-www-form-urlencoded")["result"]


@mcp.tool()
def get_single_tank_detail(tank_id: int):
    return api_get(f"tank/{tank_id}", "application/json")["result"]


@mcp.tool()
def update_tank_inventory(tank_id: int, new_inventory: int) -> str:
    tank_current = api_get(f"tank/{tank_id}", "application/json")
    if not tank_current["success"]:
        return tank_current["result"]

    tank_capacity = tank_current["result"]["tank_capacity"]
    if new_inventory > tank_capacity:
        return f"New inventory of {new_inventory} is greater than the tanks capacity. Tank capacity is {tank_capacity}. This update has been rejected."
    if new_inventory < 0:
        return f"New inventory of {new_inventory} is less than 0 and is invalid. This update has been rejected."

    payload = {"current_inventory": new_inventory}

    updated = api_patch(f"tank/adjust-inventory/{tank_id}", payload)
    if not updated["success"]:
        return updated["result"]
    return f"Inventory for tank {tank_id} has been updated to {new_inventory} {json.dumps(updated['result'], indent=4)}"


def set_tank_details():
    pass


def adjust_price():
    pass
