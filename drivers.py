from fillrite import api_get


def get_all_drivers():
    return api_get("driver", "application/x-www-urlencoded")["result"]


def get_driver_detail(driver_id: int):
    return api_get(f"driver/{driver_id}", "application/x-www-urlencoded")["result"]
