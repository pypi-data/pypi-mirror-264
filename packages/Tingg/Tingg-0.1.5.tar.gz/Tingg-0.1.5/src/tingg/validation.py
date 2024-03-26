from cmath import isnan
from datetime import datetime
import re
from .constants import VALID_DATE_FORMAT, SUPPORTED_LANGUAGE_CODES, SUPPORTED_COUNTRY_CODES, SUPPORTED_CURRENCY_CODES, REQUIRED_PAYLOAD_FIELDS

def none_empty_string(value):
    return (isinstance(value, str) and value.strip() != "") or (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and not isnan(value)
    )


def is_valid_date(date_string, date_format):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False


def is_valid_amount(value) -> bool:
    try:
        value = str(value)
        return bool(re.match(r"^\d+(\.\d+)?$", value))
    except ValueError:
        return False


def is_valid_msisdn(value) -> bool:
    try:
        value = str(value)
        return bool(re.match(r"^\+?1?\d{9,15}$", value))
    except ValueError:
        return False


def is_valid_country_code(country_code) -> bool:
    return country_code in SUPPORTED_COUNTRY_CODES


def is_valid_currency_code(currency_code) -> bool:
    return currency_code in SUPPORTED_CURRENCY_CODES


def is_valid_language_code(language_code) -> bool:
    return language_code in SUPPORTED_LANGUAGE_CODES


def is_valid_email(value):
    return bool(
        re.match(
            r'^(([^<>()[\].,;:\s@"]+(\.[^<>()[\].,;:\s@"]+)*)|(".+"))@(([^<>()[\].,;:\s@"]+\.)+[^<>()[\].,;:\s@"]{2,})$',
            value,
        )
    )


def validate_payload(payload):
    # error bag
    error = {}

    if not isinstance(payload, dict):
        return {"error": {"payload": "Payload should be a dictionary"}}

    # Check if all required fields are provided
    for field in REQUIRED_PAYLOAD_FIELDS:
        if payload.get(field) is None:
            message = f"The {field} is required"
            error.setdefault("error", {}).setdefault(field, []).append(message)

    if error.get("error"):
        return {"error": error["error"], "data": None}

    if "request_amount" in payload and not is_valid_amount(payload["request_amount"]):
        error.setdefault("error", {})[
            "request_amount"
        ] = "Invalid request_amount format"

    if "msisdn" in payload and not is_valid_msisdn(payload["msisdn"]):
        error.setdefault("error", {})["msisdn"] = "Invalid msisdn format"

    if "due_date" in payload and not is_valid_date(
        payload["due_date"], VALID_DATE_FORMAT
    ):
        error.setdefault("error", {})["due_date"] = "Invalid due_date format"

    if "country_code" in payload and not is_valid_country_code(payload["country_code"]):
        error.setdefault("error", {})[
            "country_code"
        ] = f"Invalid country_code, should be one of {', '.join(SUPPORTED_COUNTRY_CODES)}"

    if "currency_code" in payload and not is_valid_currency_code(
        payload["currency_code"]
    ):
        error.setdefault("error", {})[
            "currency_code"
        ] = f"Invalid currency_code, should be one of {', '.join(SUPPORTED_CURRENCY_CODES)}"

    if "language_code" in payload and not is_valid_language_code(
        payload["language_code"]
    ):
        error.setdefault("error", {})[
            "language_code"
        ] = f"Invalid language_code, should be one of {', '.join(SUPPORTED_LANGUAGE_CODES)}"

    if "customer_email" in payload and not is_valid_email(payload["customer_email"]):
        error.setdefault("error", {})["msisdn"] = "Invalid customer_email format"

    if "customer_first_name" in payload and not none_empty_string(
        payload["customer_first_name"]
    ):
        error.setdefault("error", {})[
            "customer_first_name"
        ] = "Invalid customer_first_name format"

    if "customer_last_name" in payload and not none_empty_string(
        payload["customer_last_name"]
    ):
        error.setdefault("error", {})["customer_last_name"] = "Invalid last_name format"

    if "account_number" in payload and not none_empty_string(payload["account_number"]):
        error.setdefault("error", {})["account_number"] = "Invalid account_number"

    if "request_description" in payload and not none_empty_string(
        payload["request_description"]
    ):
        error.setdefault("error", {})[
            "request_description"
        ] = "Invalid request_description"

    if "merchant_transaction_id" in payload and not none_empty_string(
        payload["merchant_transaction_id"]
    ):
        error.setdefault("error", {})[
            "merchant_transaction_id"
        ] = "Invalid merchant_transaction_id"

    if "service_code" in payload and not none_empty_string(payload["service_code"]):
        error.setdefault("error", {})["service_code"] = "Invalid service_code"

    if "payment_option_code" in payload and not none_empty_string(
        payload["payment_option_code"]
    ):
        error.setdefault("error", {})[
            "payment_option_code"
        ] = "Invalid payment_option_code"

    if "callback_url" in payload and not none_empty_string(payload["callback_url"]):
        error.setdefault("error", {})["callback_url"] = "Invalid callback_url"

    if "success_redirect_url" in payload and not none_empty_string(
        payload["success_redirect_url"]
    ):
        error.setdefault("error", {})[
            "success_redirect_url"
        ] = "Invalid success_redirect_url"

    if "fail_redirect_url" in payload and not none_empty_string(
        payload["fail_redirect_url"]
    ):
        error.setdefault("error", {})["fail_redirect_url"] = "Invalid fail_redirect_url"

    if "pending_redirect_url" in payload and not none_empty_string(
        payload["pending_redirect_url"]
    ):
        error.setdefault("error", {})[
            "pending_redirect_url"
        ] = "Invalid pending_redirect_url"

    if "prefill_msisdn" in payload and not isinstance(payload["prefill_msisdn"], bool):
        error.setdefault("error", {})["prefill_msisdn"] = "Invalid prefill_msisdn"

    return {"error": error.get("error"), "data": payload}