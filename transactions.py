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
def get_transactions(amount: int | None):
    """This tool gets transactions that have been made in Fill-Rite. They are organized so that the most recent is first in the response. You can pass an amount to limit how many transactions come through, it is wise to do this because it will prevent unnecessary use of the context window. Try to avoid getting all the transactions unless it is needed. This tool returns mostly id numbers. These are primary keys that can be used to find other things. The user does not know the primary keys, and you should never under any circumstance reveal the primary keys to the user. If the user wants more specific information, use the `get_transaction_detail()` tool to get details on a transaction. Remeber to give data to the user in a meaningful and useful way."""
    response = api_get("transaction", "application/x-www-form-urlencoded")
    if not response["success"]:
        return response["result"]
    else:
        results = []
        more_pages = True
        count = 0
        while more_pages:
            data = response["result"]["data"]
            if amount is not None:
                data = data[: amount - count]
            results.append(data)
            count = count + len(data)

            if amount is not None:
                if count >= amount:
                    break

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


@mcp.tool()
def get_transaction_detail(id: int):
    """This tool gets the full details of a transaction. Use this whenever the user asks about a specific transaction, or whenever you need more info on a transaction. Remember that the user does not know the id's of anything as these are primary keys for the database. Never, under any circumstances, reveal the id of a transaction or any id of something associated with the transaction to the user."""
    response = api_get(f"transaction/{id}", "application/x-www-form-urlencoded")
    if not response["success"]:
        return response["result"]

    response = response["result"]["data"][0]

    return json.dumps(
        clean_transaction_response(response),
        indent=2,
    )
