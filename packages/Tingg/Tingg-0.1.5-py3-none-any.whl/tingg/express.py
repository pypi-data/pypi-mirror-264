import requests
from .constants import SUPPORTED_ENVIRONMENTS, API_BASE_URL, AUTH_BASE_URL, API_ENDPOINTS, PAYLOAD_FIELDS_ERROR_CODES


class Express:
    @staticmethod
    def validation_error_codes():
        return [error_code for error_list in PAYLOAD_FIELDS_ERROR_CODES.values() for error_code in error_list if
                error_code is not None]

    def __init__(self, environment="sandbox"):
        if environment in SUPPORTED_ENVIRONMENTS:
            self.environment = environment
        else:
            raise ValueError("Invalid environment. Expected one of: {}".format(", ".join(SUPPORTED_ENVIRONMENTS)))

    def create(self, api_key, client_id, client_secret, payload):
        """
        Creates a checkout request.

        :param api_key: Your API KEY.
        :type api_key: str

        :param client_id: Your Client ID.
        :type client_id: str

        :param client_secret: Your Client Secret.
        :type client_secret: str

        :param payload: The payload containing the checkout details.
        :type payload: dict

        :return: The created checkout URLs
        :rtype: dict

        :raises requests.exceptions.RequestException: If the request fails for any reason.
        :raises Exception: If authentication, validation, or serialization fails.

        The function creates a checkout request by first obtaining an access token using the provided client ID and client
        secret. Then, it sends a POST request to create the checkout URL using the obtained token and provided payload.
        The function handles various error cases including authentication failure, validation errors, and serialization
        errors. In case of success, it returns the created long URL and short URL in a dictionary.

        """

        if not isinstance(api_key, str) or not (isinstance(api_key, str) and api_key.strip()):
            raise TypeError("Invalid api_key. Expected a none zero length string.")

        if not isinstance(client_id, str) or not (isinstance(client_id, str) and client_id.strip()):
            raise TypeError("Invalid client_id. Expected a none zero length string.")

        if not isinstance(client_secret, str) or not (isinstance(client_secret, str) and client_secret.strip()):
            raise TypeError("Invalid client_secret. Expected a none zero length string.")

        if not isinstance(payload, dict) or not bool(payload):
            raise TypeError("Invalid payload. Expected a none empty dictionary.")

        # Request a token
        auth_url = AUTH_BASE_URL[self.environment] + API_ENDPOINTS['auth']
        auth_headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'apikey': api_key}
        auth_payload = {'client_id':  client_id, 'client_secret':  client_secret, 'grant_type':  'client_credentials'}

        resp = requests.post(auth_url, json=auth_payload, headers=auth_headers)

        if resp.status_code == 200:
            # Request a checkout URL
            token = resp.json().get("access_token")
            url = API_BASE_URL[self.environment] + API_ENDPOINTS["create-express-request"]
            headers = {"Authorization": "Bearer {}".format(token), "Content-Type": "application/json"}

            resp = requests.post(url, json=payload, headers=headers)

            # Handle authentication error
            if resp.status_code == 401 and int(resp.json().get("statusCode")) == 132:
                """
                {
                    "data": null,
                    "success": false,
                    "statusCode": 132,
                    "message": "Full authentication is required to access this resource"
                }
                """

                print("Error code: {}".format(resp.json()["statusCode"]))
                print("Error message: {}".format(resp.json()["message"]))

                raise Exception("Authentication failed. Invalid or expired token. Try again later.")

            # Handle validation errors
            if (
                    resp.status_code == 200 and
                    not isinstance(resp.json().get("status"), dict) and
                    int(resp.json().get("status")) in self.validation_error_codes()
            ):
                """
                {
                    "status": 1018,
                    "message": "The checkout request did not have a msisdn."
                }
                """

                print("Error code: {}".format(resp.json()["status"]))
                print("Error message: {}".format(resp.json()["message"]))

                raise Exception("Validation failed. {}".format(resp.json()['message']))

            # Handle serialization error
            if resp.status_code == 400 and int(resp.json().get("status")) == 400:
                """
                { 
                    "status": 400, 
                    "message": "JSON parse error: Cannot deserialize value of type ..."
                }
                """

                print("Error code: {}".format(resp.json()["status"]))
                print("Error message: {}".format(resp.json()["message"]))

                raise Exception("Serialization failed. Invalid or malformed JSON payload.")

            # Handle happy path
            if (
                    resp.status_code == 200 and
                    isinstance(resp.json().get("status"), dict) and
                    int(resp.json().get("status").get("status_code")) == 200
            ):
                """
                {
                    "status": {
                        "status_code": 200,
                        "status_description": "success"
                    },
                    "results": {
                        "long_url": "...",
                        "short_url": "..."
                    }
                }
                """

                long_url = resp.json()["results"]["long_url"]
                short_url = resp.json()["results"]["short_url"]

                return {"long_url": long_url, "short_url": short_url}
            else:
                raise Exception("Something went wrong. Please try again later.")
        else:
            raise Exception("Authentication failed. Check your credentials, and try again.")
