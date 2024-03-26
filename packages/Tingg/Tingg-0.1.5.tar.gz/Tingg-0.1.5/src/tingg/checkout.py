from urllib.parse import urlencode, urlunparse, urlparse
from .encryption import Encryption
from .validation import validate_payload
from .constants import SUPPORTED_ENVIRONMENTS, EXPRESS_URL

class Checkout:
    def __init__(self, iv_key, secret_key, access_key, environment="sandbox"):
        self.iv_key = iv_key
        self.secret_key = secret_key
        self.access_key = access_key
        self.environment = environment if environment in SUPPORTED_ENVIRONMENTS else "sandbox"

    def process_payment(self, payload):
        try:
            validation_result = validate_payload(payload)
            if validation_result["error"] is not None:
                validation_result["data"] = None
                print(f"Validation Error: {validation_result}")
                return

            encryption_instance = Encryption(self.iv_key, self.secret_key)
            payload_str = str(payload)
            encrypted_payload = encryption_instance.encrypt(payload_str)

            redirect_url = str(self.build_redirect_url(encrypted_payload))
            return encrypted_payload, redirect_url

        except Exception as e:
            print(f"Error processing data: {e}")

    def build_redirect_url(self, encrypted_payload):
        base_url = EXPRESS_URL.get(self.environment, EXPRESS_URL[self.environment])
        parsed_url = urlparse(base_url)
        query_params = {
            "access_key": self.access_key,
            "encrypted_payload": encrypted_payload,
        }
        query_string = urlencode(query_params)
        new_url = urlunparse(parsed_url._replace(query=query_string))
        return new_url