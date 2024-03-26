import time
import requests
import structlog

from colorama import Fore
from .login_type import Client
from .auth_type import OktaFactorType, OktaFactors, OktaPrimaryResponse, OktaProviders, OktaStatus

BASE_URL = "https://contentsquare.okta.com/"
logger = structlog.get_logger()

def primary_authentication(client: Client) -> OktaPrimaryResponse:
    """This function does the initial connection with the Okta client"""

    path = "api/v1/authn"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(url = BASE_URL + path, json = client, headers = headers)
    
    okta_response = {"stateToken": "", "status": "", "factors": []}

    # Now we need to parse quickly the response
    if response.json():
        resp = response.json()
        if resp.get("stateToken", None):
            okta_response['stateToken'] = resp["stateToken"]

        else:
            logger.error("Error: State Token not found")
            logger.error("Authentication failed")
            exit(0)

        if resp.get("status", None):
            okta_response['status'] = OktaStatus(resp["status"])

        else:
            logger.error("Error: Status is empty")
            logger.error("Authentication failed")
            exit(0)

        if resp.get("_embedded", None) and resp["_embedded"].get("factors", None):
            for factor in resp["_embedded"]["factors"]:
                _factor = {"provider": "", "factorType": "", "link": ""}

                # Now inside the factors, we need to parse three things: The provider, the factor type, and the link
                if factor.get("factorType", None):
                    _factor["factorType"] = OktaFactorType(factor["factorType"])

                else:
                    logger.error("Error: No Factor Type found")
                    logger.error("Authentication failed")
                    exit(0)

                if factor.get("provider"):
                    _factor["provider"] = OktaProviders(factor["provider"])

                else:
                    logger.error("Error: No provider was found")
                    logger.error("Authentication failed")
                    exit(0)

                if factor.get("_links", None) and factor["_links"].get("verify", None) and factor["_links"]["verify"].get("href", None):
                    _factor["link"] = factor["_links"]["verify"]["href"]

                else:
                    logger.error("Error: The link is missing")
                    logger.error("Authentication failed")
                    exit(0)

                okta_response["factors"].append(OktaFactors(provider = _factor["provider"], factorType = _factor["factorType"], link = _factor["link"]))

    else:
        logger.error("Error: No Response")
        logger.error("Authentication failed")
        exit(0)

    # Finally, we have to parse the datatype
    resp = OktaPrimaryResponse(factors = okta_response["factors"], stateToken = okta_response["stateToken"], status = okta_response["status"])

    return resp

def mfa_totp_authentication(link: str, stateToken: str):
    """This function is the function that is responsible for the TOTP MFA"""

    # First thing that we nee dto do is to take input from the user to input is the MFA code
    mfa = str(input(Fore.CYAN + "MFA: " + Fore.RESET))

    # Now that we have the MFA, we can send the mfa with the state code
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "stateToken": stateToken,
        "passCode": mfa
    }

    response = requests.post(url = link, json = payload, headers = headers)

    resp = response.json()
    # Now we need to extract the access token

    if resp.get("sessionToken", None):
        logger.info("Challenge MFA Ok")
        logger.info("Session login successful")
        return resp["sessionToken"]
    
    else:
        logger.error("Error: Session Token not found")
        logger.error("Authentication failed")
        exit(0)

def mfa_push_authentication(link: str, stateToken: str):
    """This function is the function that is responsible for the MFA push notification"""

    # First thing that we should do is to send the push notification
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "stateToken": stateToken
    }

    response = requests.post(url = link, json = payload, headers = headers)
    logger.info("Push notification sent")

    resp = response.json()

    # Now here we should parse the most important thing which is the status code
    if resp.get("status", None):
        if OktaStatus(resp["status"]) is not OktaStatus.SUCCESS:
            while True:
                time.sleep(1)

                response = requests.post(url = link, json = payload, headers = headers)

                resp = response.json()

                if resp.get("status", None) and resp.get("factorResult", None):
                    if OktaStatus(resp["status"]) is OktaStatus.SUCCESS and resp['factorResult'] != "REJECTED":
                        break
                    if resp['factorResult'] == "REJECTED":
                        logger.error("Error: Rejected push notification")
                        logger.error("Authentication failed")
                        exit(0)
        
        if resp.get("sessionToken", None):
            logger.info("Challenge MFA Ok")
            logger.info("Session login successful")
            return resp["sessionToken"]
        
        else:
            logger.error("Error: Session Token not found")
            logger.error("Authentication failed")
            exit(0)
    
    else:
        logger.error("Error: status not found")
        logger.error("Authentication failed")
        exit(0)
