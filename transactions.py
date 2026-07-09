import json
from fillrite import mcp, api_get, api_patch, path_from_url


def clean_transaction_response(data: dict):
    """Cleans the transactions so that the ai is not given personal or unwanted info."""
    result = {}
    product = data.get("product", {})
    if isinstance(product, list):
        product = product[0] if product else {}

    result["id"] = data.get("id")
    result["label"] = data.get("label")
    result["transaction_type"] = data.get("transaction_type")
    result["tank_id"] = data.get("tank_id")
    result["start_date"] = data.get("start_date")
    result["end_date"] = data.get("end_date")
    result["product_type"] = product.get("product_category")
    result["product_name"] = product.get("product_name")
    result["volume"] = data.get("volume")
    result["unit"] = data.get("unit")
    result["percent"] = data.get("percent")
    result["price"] = data.get("price")
    result["driver_id"] = data.get("driver_id")
    result["user_id"] = data.get("user_id")
    result["vehicle_id"] = data.get("vehicle_id")
    result["driver_type"] = data.get("driver_type")
    result["transaction_time_utc"] = data.get("transaction_time_utc")
    result["created_utc"] = data.get("created_utc")
    result["updated_at"] = data.get("updated_at")
    result["utc_offset"] = data.get("utc_offset")
    result["status"] = data.get("status")
    result["pump_name"] = data.get("pump_name")

    return result


def get_latest_transactions():
    pass


@mcp.tool()
def get_all_transactions():
    """Gets all transactions. This will be an insane amount of transactions and will probably blow the context"""
    response = api_get("transaction", "application/x-www-form-urlencoded")
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

    transactions = []
    clean_transactions = []
    for transaction in results:
        if isinstance(transaction, list):
            for item in transaction:
                transactions.append(clean_transaction_response(item))
        else:
            transactions.append(clean_transaction_response(transaction))

    for transaction in transactions:
        t = {}
        t["id"] = transaction.get("id")
        t["vehicle_id"] = transaction.get("vehicle_id")
        t["driver_id"] = transaction.get("driver_id")
        t["transaction_time_utc"] = transaction.get("transaction_time_utc")
        t["status"] = transaction.get("status")
        clean_transactions.append(t)

    return json.dumps(clean_transactions, indent=2)


def get_transactions(amount: int):
    """Gets a set amount of transactions"""
    pass


@mcp.tool()
def get_transaction_detail(id: int):
    """Gets the full details of a single transaction."""
    response = api_get(f"transaction/{id}", "application/x-www-form-urlencoded")
    if not response["success"]:
        return response["result"]

    response = response["result"]["data"][0]

    return json.dumps(
        clean_transaction_response(response),
        indent=2,
    )
