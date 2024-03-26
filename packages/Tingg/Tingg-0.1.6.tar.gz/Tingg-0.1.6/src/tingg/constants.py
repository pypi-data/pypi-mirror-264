SUPPORTED_ENVIRONMENTS = ["testing", "sandbox", "production"]

VALID_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

SUPPORTED_LANGUAGES = {
    "ar": "Arabic",
    "fr": "French",
    "en": "English",
    "pt": "Portuguese",
}

INSTANT_PAYMENT_NOTIFICATION_ACTIONS = {
    "accept": {
        "status_code": 183,
        "status_description": "Payment has been accepted",
    },
    "reject": {
        "status_code": 180,
        "status_description": "Payment has been rejected",
    },
    "acknowledge": {
        "status_code": 188,
        "status_description": "Payment has been acknowledged",
    },
}

SUPPORTED_COUNTRIES = {
    "MW": {
        "name": "Malawi",
        "country_code": "MWI",
        "currency_code": "MWK",
        "calling_code": "265",
        "test_msisdn": "+2651800000",
    },
    "KE": {
        "name": "Kenya",
        "country_code": "KEN",
        "currency_code": "KES",
        "calling_code": "254",
        "test_msisdn": "+254700000000",
    },
    "GH": {
        "name": "Ghana",
        "country_code": "GHA",
        "currency_code": "GHS",
        "calling_code": "233",
        "test_msisdn": "+233240000000",
    },
    "ZM": {
        "name": "Zambia",
        "country_code": "ZMB",
        "currency_code": "ZMW",
        "calling_code": "260",
        "test_msisdn": "+260970000000",
    },
    "UG": {
        "name": "Uganda",
        "country_code": "UGA",
        "currency_code": "UGX",
        "calling_code": "256",
        "test_msisdn": "+256770000000",
    },
    "BW": {
        "name": "Botswana",
        "country_code": "BWA",
        "currency_code": "BWP",
        "calling_code": "267",
        "test_msisdn": "+2670000000",
    },
    "AG": {
        "name": "Angola",
        "country_code": "AGO",
        "currency_code": "AOA",
        "calling_code": "244",
        "test_msisdn": "+244921000000",
    },
    "TZ": {
        "name": "Tanzania",
        "country_code": "TZA",
        "currency_code": "TZS",
        "calling_code": "255",
        "test_msisdn": "+255780000000",
    },
    "NG": {
        "name": "Nigeria",
        "country_code": "NGA",
        "currency_code": "NGN",
        "calling_code": "234",
        "test_msisdn": "+234800000000000",
    },
    "ZA": {
        "name": "South Africa",
        "country_code": "ZAF",
        "currency_code": "ZAR",
        "calling_code": "276",
        "test_msisdn": "+27646000000",
    },
    "CI": {
        "name": "Côte d'Ivoire",
        "country_code": "CIV",
        "currency_code": "XOF",
        "calling_code": "225",
        "test_msisdn": "+22555000000",
    },
}

SUPPORTED_LANGUAGE_CODES = list(SUPPORTED_LANGUAGES.keys())

SUPPORTED_COUNTRY_CODES = list(
    set([SUPPORTED_COUNTRIES[key]["country_code"] for key in SUPPORTED_COUNTRIES])
)

SUPPORTED_CURRENCY_CODES = list(
    set([SUPPORTED_COUNTRIES[key]["currency_code"] for key in SUPPORTED_COUNTRIES])
)

REQUIRED_PAYLOAD_FIELDS = {
    # transaction details
    "msisdn": "The msisdn provided is not valid",
    "due_date": "The due_date should be in the format " + VALID_DATE_FORMAT,
    "account_number": "The account_number provides should be a string or number",
    "request_amount": "The request_amount should be a valid integer or float",
    "merchant_transaction_id": "The merchant_transaction_id should a valid string or number",
    # checkout configurations
    "service_code": "The service_code be a valid string",
    "country_code": "The country_code should be one of {}".format(
        ", ".join(SUPPORTED_COUNTRY_CODES)
    ),
    "currency_code": "The currency_code should be one of {}".format(
        ", ".join(SUPPORTED_CURRENCY_CODES)
    ),
    # webhooks configurations
    "callback_url": "The callback_url should be a valid URL",
    "fail_redirect_url": "The fail_redirect_url should be a valid URL",
    "success_redirect_url": "The success_redirect_url should be a valid URL",
}

OPTIONAL_PAYLOAD_FIELDS = {
    # transaction details
    "customer_email": "The customer_email provided is not valid",
    "customer_last_name": "The customer_last_name should be a valid string",
    "customer_first_name": "The customer_first_name should be a valid string",
    "request_description": "The request_description should be a valid string",
    "invoice_number": "The invoice_number should be a valid string or number",
    # checkout configurations
    "prefill_msisdn": "The prefill_msisdn should be true or false",
    "payment_option_code": "The payment_option_code should a valid string",
    "language_code": "The language_code should be one of {}".format(
        ", ".join(SUPPORTED_LANGUAGE_CODES)
    ),
    "charge_beneficiaries": "The charge_beneficiaries should be an array of objects with amount & charge_beneficiary_code",
    # webhooks configurations
    "pending_redirect_url": "The pending_redirect_url should be a valid URL",
}

# ERROR CODES MAPPING {<field> : [0 => "missing error code", 1 => "invalid error code"]}
PAYLOAD_FIELDS_ERROR_CODES = {
    "msisdn": [1018, 1019],


    "due_date": [None, 1029], # Should be mandatory
    "account_number": [1028, None],
    "request_amount": [None, 1026],
    "merchant_transaction_id": [1014, None],

    "service_code": [1017, 1003],
    "country_code": [1007, 1003],
    "currency_code": [1008, 1003],


    "callback_url": [1012, 1012],
    "fail_redirect_url": [1013, 1013],
    "success_redirect_url": [1015, 1015],


    "customer_email": [None, 1030],
    "customer_first_name": [7, 7],
    "customer_last_name": [7,7],
    "request_description": [400],
    "invoice_number": [],

    "prefill_msisdn": [],
    "payment_option_code": [],
    "language_code": [],
    "charge_beneficiaries": [],

    "pending_redirect_url": []
}

EXPRESS_URL = {
    "production": "https://checkout.tingg.africa/express/checkout",
    "testing": "https://online.uat.tingg.africa/testing/express/checkout",
    "sandbox": "https://online.sandbox.tingg.africa/approval/express/checkout",
}

API_ENDPOINTS = {
    "auth": "/oauth/token/request",
    "create-express-request": "/request-service/checkout-request/express-request"
}

AUTH_BASE_URL = {
    "testing": "https://api-test.tingg.africa/v1",
    "sandbox": "https://api-approval.tingg.africa/v1",
    "production": "https://api.tingg.africa/v1",
}

API_BASE_URL = {
    "production": "https://api.tingg.africa/v1",
    "testing": "https://online.uat.tingg.africa/testing",
    "sandbox": "https://api-approval.tingg.africa/v1",
}