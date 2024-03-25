from enum import Enum
from typing import TypedDict

class OktaStatus(Enum):
    """The different Okta Classes"""

    MFA_REQUIRED = "MFA_REQUIRED"
    SUCCESS  = "SUCCESS"
    WAITING = "WAITING"
    MFA_CHALLENGE = "MFA_CHALLENGE"

class OktaFactorType(Enum):
    """The different Okta Factor Types"""

    TOTP = "token:software:totp"
    PUSH = "push"
    YUBICO = "token:hardware"

class OktaProviders(Enum):
    """The supported providers from Okta"""

    GOOGLE = "GOOGLE"
    OKTA = "OKTA"
    YUBIKO = "YUBIKO"

class OktaFactors(TypedDict):
    """the datatype that contain the necessary information that we want from Okta respone"""

    provider: OktaProviders
    factorType: OktaFactorType
    link: str

class OktaPrimaryResponse(TypedDict):
    """The datatype which represents the initial response from Okta"""

    stateToken: str
    status: OktaStatus
    factors: list[OktaFactors]
