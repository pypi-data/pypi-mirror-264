from typing import TypedDict

class Client(TypedDict):
    """The client class which will contain the username and password"""

    username: str
    password: str