"""Top-level package for scim_client."""

__author__ = """Mitratech Development Team"""
__email__ = "devs@mitratech.com"
__version__ = "0.1.0"

from .scim_client import SCIMClient
from .response import SCIMResponse
from .resources import User, UserSearch, UserMeta, UserEmail, UserName
