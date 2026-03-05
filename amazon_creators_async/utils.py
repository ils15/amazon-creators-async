"""
Utilities and constants for the Amazon Creators API.
"""

from enum import Enum

class Region(str, Enum):
    NORTH_AMERICA = "NA"
    EUROPE = "EU"
    FAR_EAST = "FE"

def get_api_endpoint(region: Region) -> str:
    """Returns the endpoint for the respective region."""
    return "https://creatorsapi.amazon/catalog/v1"

def get_version_for_region(region: Region) -> str:
    """Returns the authorization version for a given Region."""
    if region == Region.NORTH_AMERICA:
        return "2.1"
    elif region == Region.EUROPE:
        return "2.2"
    elif region == Region.FAR_EAST:
        return "2.3"
    raise ValueError(f"Unknown region: {region}")

def get_auth_endpoint(version: str) -> str:
    """Returns the correct OAuth2 token endpoint based on version."""
    if version == "2.1":
        return "https://creatorsapi.auth.us-east-1.amazoncognito.com/oauth2/token"
    elif version == "2.2":
        return "https://creatorsapi.auth.eu-south-2.amazoncognito.com/oauth2/token"
    elif version == "2.3":
        return "https://creatorsapi.auth.us-west-2.amazoncognito.com/oauth2/token"
    elif version == "3.1":
        return "https://api.amazon.com/auth/o2/token"
    elif version == "3.2":
        return "https://api.amazon.co.uk/auth/o2/token"
    elif version == "3.3":
        return "https://api.amazon.co.jp/auth/o2/token"
    raise ValueError(f"Unsupported version: {version}")

def get_scope(version: str) -> str:
    """Returns the correct OAuth2 scope based on version."""
    if version.startswith("3."):
        return "creatorsapi::default" # LWA scope
    return "creatorsapi/default" # Cognito scope

def validate_marketplace(marketplace: str):
    """Simple check for typical marketplace domains."""
    if not marketplace.startswith("www.amazon."):
        raise ValueError("Marketplace must be a valid Amazon domain (e.g. 'www.amazon.com', 'www.amazon.com.br')")
