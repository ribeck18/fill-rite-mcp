import json
import requests
from urllib.parse import urlparse
from mcp.server.fastmcp import FastMCP

from config import auth_token, base_url  # https://fmsapi.fillrite.com/rest/v1.0/

mcp = FastMCP("Fill-Rite")


# Helper functions


def path_from_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path
    prefix = "/rest/v1.0/"

    if path.startswith(prefix):
        path = path[len(prefix) :]
    else:
        path = path.lstrip("/")

    if parsed.query:
        return f"{path}?{parsed.query}"

    return path


def api_get(path: str, content_type: str, payload: dict | None = None) -> dict:
    """makes a get request to the fuelrite api."""
    url = base_url + path
    headers = {
        "Authorization": auth_token(),
        "Content-Type": content_type,
    }
    response = None
    if payload is None:
        data = {}
    else:
        data = payload

    return_dict = {
        "success": False,
        "result": "",
    }
    try:
        response = requests.request("GET", url, headers=headers, data=data, timeout=15)
        response.raise_for_status()
        return_dict["success"] = True
        return_dict["result"] = response.json()

    except requests.RequestException as err:
        return_dict["result"] = f"Error fetching {path}: {err}"

    except json.JSONDecodeError:
        if response is not None:
            return_dict["result"] = (
                f"Fillrite returned a non-JSON response for {path}: {response.text[:500]}"
            )
        else:
            return_dict["result"] = f"Error fetching {path}: no response."

    return return_dict


def api_patch(path: str, payload: dict) -> dict:
    """Makes a patch request to the fuelrite api"""
    url = base_url + path
    headers = {"Authorization": auth_token()}
    response = None

    return_dict = {
        "success": False,
        "result": "",
    }

    try:
        response = requests.request(
            "PATCH", url, headers=headers, json=payload, timeout=15
        )
        response.raise_for_status()
        return_dict["success"] = True
        return_dict["result"] = response.json()

    except requests.RequestException as err:
        return_dict["result"] = f"Error fetching {path}: {err}"
    except json.JSONDecodeError:
        if response is not None:
            return_dict["result"] = (
                f"Fillrite returned a non-JSON response for {path}: {response.text[:500]}"
            )
        else:
            return_dict["result"] = f"Error updating {path}: no response."

    return return_dict
