import os
import time
import requests
import urllib.parse
import base64

# Define module-level variables for CURRENT_TOKEN and CURRENT_EXPIRY
CURRENT_TOKEN = ""
CURRENT_EXPIRY = -1
CURRENT_SCOPE = ""


class Request:
    def __init__(self, method, url, headers, body=""):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body

    def __str__(self):
        return f"method={self.method}, url={self.url}, headers={self.headers}, body={self.body})"


class Response:
    def __init__(self, status, headers, body):
        self.status = status
        self.headers = headers
        self.body = body

    def __str__(self):
        return "Response(status={}, headers={}, body={})".format(
            self.status, self.headers, self.body
        )


class CustomHook:
    def before_request(self, request):
        global CURRENT_TOKEN, CURRENT_EXPIRY, CURRENT_SCOPE  # Declare these as global to modify the module-level variables
        if request.url.endswith("/token"):
            return

        # Get the client_id and client_secret from environment variables
        client_id = os.getenv("CLIENT_ID", "")
        client_secret = os.getenv("CLIENT_SECRET", "")

        if not client_id or not client_secret:
            print("Missing CLIENT_ID and/or CLIENT_SECRET environment variables")
            return
        else:
            # Derive the oaauth2 scope from the request method and url
            oauth2_scope = self.getOauth2Scope(request)

            # Check if CURRENT_TOKEN is missing or CURRENT_EXPIRY is in the past or the oauth2_scope is different from CURRENT_SCOPE
            if (
                not CURRENT_TOKEN
                or CURRENT_EXPIRY < time.time()
                or oauth2_scope != CURRENT_SCOPE
            ):
                # Fetch a fresh OAuth token
                try:

                    response = self.doPost(
                        "https://demo-api.ramp.com/developer/v1/token",
                        client_id,
                        client_secret,
                        oauth2_scope,
                    )
                    if response is None:
                        print("Failed to fetch OAuth token.")
                        return

                    expires_in = response.get("expires_in")
                    access_token = response.get("access_token")
                    if not expires_in or not access_token:
                        print("There is an issue with getting the OAuth token")
                        return

                    CURRENT_EXPIRY = int(time.time()) + expires_in * 1000
                    CURRENT_TOKEN = access_token
                    CURRENT_SCOPE = oauth2_scope
                except Exception as e:
                    print("An error occurred while fetching the OAuth token:", str(e))
                    return

            # Set the Bearer token in the request header
            authorization = f"Bearer {CURRENT_TOKEN}"
            request.headers["Authorization"] = authorization

    def doPost(
        self, urlEndpoint: str, clientId: str, clientSecret: str, oauth2Scope: str
    ):
        authHeader = (
            f"Basic {base64.b64encode(f'{clientId}:{clientSecret}'.encode()).decode()}"
        )

        postData = {"grant_type": "client_credentials", "scope": oauth2Scope}

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": authHeader,
        }

        try:
            resp = requests.post(
                urlEndpoint, data=self.toFormData(postData), headers=headers
            )
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            print("Error in posting the request:", str(e))
            return None

    def toFormData(self, data: dict) -> str:
        return "&".join(
            [
                f"{key}={urllib.parse.quote_plus(str(value))}"
                for key, value in data.items()
            ]
        )

    def getOauth2Scope(self, request: Request) -> str:
        resource = request.url.split("/developer/v1/")[1].split("/")[0]
        permission = "read" if request.method.lower() == "get" else "write"
        oauth2Scope = f"{resource}:{permission}"
        return oauth2Scope

    def after_response(self, request: Request, response: Response):
        print("")

    def on_error(self, error: Exception, request: Request, response: Response):
        print("")
