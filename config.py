import datetime
import enum
import json
import os

from dotenv import load_dotenv
import requests
from pathlib import Path

from errors import FillriteAuthError, FillriteError, FillriteResponseError


load_dotenv()
TOKEN_FILE = Path(__file__).parent / "tokens.json"


class TokenType(enum.Enum):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"


def get_env_var(env_var: str) -> str:
    """Gets a variable from the .env file"""
    var = os.environ.get(env_var)
    if var is None:
        raise ValueError(f"No value was found for {env_var}")

    return var


def get_token_data(token_type: TokenType):
    if not TOKEN_FILE.exists():
        raise ValueError("Token file does not exist.")

    data = json.loads(TOKEN_FILE.read_bytes())

    return data[token_type.value]


def _load_token_data():
    if not TOKEN_FILE.exists():
        return {}
    return json.loads(TOKEN_FILE.read_bytes())


def _update_expire(seconds: int):
    """Gets the new expire date for a token."""
    now = datetime.datetime.now(datetime.timezone.utc)
    expires_at = now + datetime.timedelta(seconds=seconds)

    return expires_at.isoformat()


def token_near_expire() -> bool:
    time_margin = 1200
    expire_date = datetime.datetime.fromisoformat(
        get_token_data(TokenType.ACCESS_TOKEN)["expires_at"]
    )
    now = datetime.datetime.now(datetime.timezone.utc)

    return expire_date - datetime.timedelta(seconds=time_margin) <= now


def refresh_tokens() -> str:
    """The refresh token must be refreshed every 7 days. If it is not then the token will expire and this mcp will not run. The access token must be refreshed every 30 minutes."""
    refresh_token = get_token_data(TokenType.REFRESH_TOKEN)["token"]
    url = f"https://fmsapi.fillrite.com/rest/refresh-token/{refresh_token}"
    headers = {
        "Authorization": get_token_data(TokenType.ACCESS_TOKEN)["token"],
        "Content-Type": "application/x-www-urlencoded",
    }
    payload = {}

    try:
        resp = requests.request("GET", url, headers=headers, data=payload)
    except requests.RequestException as err:
        raise FillriteError(f"Network error contacting Fill-Rite: {err}")

    if resp.status_code != 200:
        if resp.status_code in (401, 403):
            raise FillriteAuthError(
                f"Refresh rejected [{resp.status_code}] - refresh token may have expired."
            )
        raise FillriteResponseError(
            f"Unexpected status [{resp.status_code}]: {resp.text}"
        )

    try:
        response = resp.json()
    except ValueError:
        raise FillriteResponseError(f"Response was not valid JSON: {resp.text}")

    if "access_token" not in response:
        raise FillriteResponseError("Response missing new access_token")
    elif "refresh_token" not in response:
        raise FillriteResponseError("Response missing new refresh_token")

    data = _load_token_data()
    data["access_token"]["token"] = response["access_token"]
    data["access_token"]["expires_at"] = _update_expire(response["expires_in"])
    data["refresh_token"]["token"] = response["refresh_token"]

    tmp = TOKEN_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=4))
    os.replace(tmp, TOKEN_FILE)

    return "Token refresh completed."


base_url = get_env_var("BASE_URL")


def auth_token() -> str:
    """Reads the CURRENT token from tokens.json"""
    if token_near_expire():
        refresh_tokens()
    return get_token_data(TokenType.ACCESS_TOKEN)["token"]
