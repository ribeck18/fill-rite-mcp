from fillrite import api_get


def get_all_vehicles() -> str:
    return api_get("vehicle", "application/x-www-form-urlencoded")["result"]


def get_all_vehicles_filtered():
    pass


def get_vehicle_detail(vehicle_id: int):
    return api_get(f"vehicle/{vehicle_id}", "application/x-www-form-urlencoded")[
        "result"
    ]
