import json
from fillrite import api_get, mcp, path_from_url


def clean_vehicle_response(data: dict) -> dict:
    """Cleans the vehicle response so that private information, and unwanted data is not given to the agent."""
    result = {}
    access_groups = data.get("access_groups", {})
    if isinstance(access_groups, list):
        access_groups = access_groups[0] if access_groups else {}
    drivers = data.get("drivers", {})
    if isinstance(drivers, list):
        drivers = drivers[0] if drivers else {}

    result["id"] = data.get("id")
    result["name"] = data.get("name")
    result["code"] = data.get("code")
    result["status"] = data.get(
        "status"
    )  # right now the api returns a number. I need to find what status the numbers match, then write an enum to translate.
    result["taxable"] = data.get("taxable")
    if result["taxable"] == "none":
        result["taxable"] = "taxability not set"
    result["created"] = data.get("created")
    result["updated"] = data.get("updated")
    result["fuel_type"] = data.get("product_type")
    result["access_groups"] = (
        "no assigned groups" if access_groups == {} else access_groups
    )
    result["drivers"] = "no assigned drivers" if drivers == {} else drivers

    return result


@mcp.tool()
def get_all_vehicles() -> str:
    """This tool fetches data on all vehicles. It provides basic information on all the vehicles the user has access to. Users do not know about the id for each vehicle. Never under any circumstances reveal the id of any vehicle to the user. Use this tool whenever the user asks what vehicles exists, or about vehicles in general. You can also use this tool to find a vehicles id so that you can pass it as an argument to the `get_vehicle_detail` tool."""
    response = api_get("vehicle", "application/x-www-form-urlencoded")
    if not response["success"]:
        return response["result"]
    else:
        results = []
        more_pages = True
        while more_pages:
            data = response["result"]["data"]
            results.append(data)

            next_url = response["result"]["meta"]["next"]
            if next_url is None:
                more_pages = False
                break

            response = api_get(
                path_from_url(next_url), "application/x-www-form-urlencoded"
            )

            if not response["success"]:
                return response["result"]

    vehicles = []
    clean_vehicles = []
    for vehicle in results:
        if isinstance(vehicle, list):
            for v in vehicle:
                vehicles.append(clean_vehicle_response(v))
        else:
            vehicles.append(clean_vehicle_response(vehicle))

    for vehicle in vehicles:
        v = {}
        v["id"] = vehicle.get("id")
        v["name"] = vehicle.get("name")
        v["code"] = vehicle.get("code")
        v["fuel_type"] = vehicle.get("fuel_type")

        clean_vehicles.append(v)

    return json.dumps(clean_vehicles, indent=2)


@mcp.tool()
def get_vehicle_detail(vehicle_id: int):
    """This tool gets the complete detail on a specific vehicle. Use this tool whenever the user asks about a specific vehicle, or if you need details on a vehicle. The user does not know the vehicle id as it is a database primary key. The user will usually refer to the vehicle by code or name. Do not ever under any circumstances tell the user the id of a vehicle."""
    response = api_get(f"vehicle/{vehicle_id}", "application/x-www-form-urlencoded")
    if not response["success"]:
        return response["result"]

    response = response["result"]["data"][0]

    return json.dumps(
        clean_vehicle_response(response),
        indent=2,
    )
