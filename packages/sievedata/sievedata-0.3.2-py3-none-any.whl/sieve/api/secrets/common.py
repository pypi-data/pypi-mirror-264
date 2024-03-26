import requests
from sieve.api.utils import get_api_key, sieve_request
from sieve.api.constants import API_URL, API_BASE
import json


def get(name=None, API_KEY=None, limit=10000, offset=0):
    """
    Get a secret by name
    """
    return sieve_request(
        "GET",
        f"secrets/{name}",
        params={"limit": limit, "offset": offset},
        api_key=API_KEY,
    )


def list(limit=10000, offset=0, API_KEY=None):
    """
    List all secrets
    """

    rjson = sieve_request(
        "GET",
        "secrets",
        params={"limit": limit, "offset": offset},
        api_key=API_KEY,
    )

    return rjson["data"], rjson["next_offset"]


def create(name=None, value=None, API_KEY=None):
    """
    Create a secret
    """

    data = {"value": value}
    sdata = json.dumps(data)
    return sieve_request(
        "POST",
        f"secrets/{name}",
        data=sdata,
        api_key=API_KEY,
    )


def delete(name=None, API_KEY=None):
    """
    Delete a secret
    """

    return sieve_request(
        "DELETE",
        f"secrets/{name}",
        api_key=API_KEY,
    )


def update(name=None, value=None, API_KEY=None):
    """
    Update a secret
    """

    return sieve_request(
        "PUT",
        f"secrets/{name}",
        data=sdata,
        api_key=API_KEY,
    )
