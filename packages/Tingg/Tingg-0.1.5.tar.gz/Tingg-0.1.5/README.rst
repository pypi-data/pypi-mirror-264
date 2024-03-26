Tingg Checkout SDK
===================

.. image:: https://cdn.cellulant.africa/images/brand-assets/tingg-by-cellulant-themed.svg
    :target: https://tingg.africa
    :alt: Tingg by Cellulant
    :height: 64px

Overview
--------

This Tingg Checkout SDK helps you streamline your integration to the Tingg Checkout API to facilitate secure processing of payments. It includes functionality for payload validation and encryption of payment data.

Prerequisites
-------------

You need a `Tingg account <https://app.sandbox.tingg.africa/cas/login>`_ to use this package. If you don't have one you can contact our account managers through `tingg-checkout@cellulant.io` and have your business registered & activated.

Visit our `official documentation <https://docs.tingg.africa/docs/checkout-v3-getting-started>`_ to find out more on how you can get started using Tingg.

Once you're signed in, you will need to retrieve your `API Keys <https://docs.tingg.africa/docs/checkout-v3-integration-dashboard#get-your-api-keys>`_, that is the client ID, the client secret, and the API Key.

Installation
------------

We'll create a sample project with `Flask <https://flask.palletsprojects.com/en/3.0.x/>` using a .venv directory.

Give the project any name you like

.. code-block:: bash

    mkdir <project-name>

.. code-block:: bash

    cd <project-name>

.. code-block:: bash

    python3 -m venv .venv

.. code-block:: bash

    . .venv/bin/activate

.. code-block:: bash

    pip install Tingg Flask requests python-dotenv pycryptodome

Usage
-----

.. code-block:: python

    import os
    from tingg import Express
    from dotenv import load_dotenv
    from flask import Flask, request, jsonify

    load_dotenv()
    app = Flask(__name__)

    # Recommended
    @app.route('/express', methods=['POST'])
    def express_checkout():
        # Get these values from your .env file or CLI args
        env = os.getenv("ENV")
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")

        # Get the JSON payload from the request
        payload = request.json

        # A sample for value for request.json
        # {
        #     merchant_transaction_id: "mtr-dg9823euy3a",
        #     account_number: "acc-14n345j5599",
        #     msisdn: "254700000000",
        #     service_code: "JOHNDOEONLINE",
        #     country_code: "KEN",
        #     currency_code: "KES",
        #     customer_last_name: "John",
        #     customer_first_name: "Doe",
        #     customer_email: "tingg@cellulant.io",
        #     request_amount: "100",
        #     due_date: "2023-11-18 16:15:30",
        #     language_code: "en",
        #     request_description: "Dummy merchant transaction",
        #     fail_redirect_url: "https://webhook.site/88390df9-a496-432f-abe5-0cf3380fda54",
        #     success_redirect_url: "https://webhook.site/88390df9-a496-432f-abe5-0cf3380fda54",
        #     callback_url: "https://webhook.site/88390df9-a496-432f-abe5-0cf3380fda54",
        # }

        express = Express(env)
        result = express.create(client_id, client_secret, payload)

        # A sample response for the testing environment
        """
        {
            "long_url": "https://online.uat.tingg.africa/testing/express/checkout?access_key=...&encrypted_payload=...",
            "short_url": "https://online.uat.tingg.africa/testing/express/checkout/..."
        }
        """

        return jsonify(result)

Features
--------

- Payload Validation: Ensures that the provided payment payload adheres to specified criteria.
- Encryption: Uses AES encryption to secure payment data during processing.

For more detailed usage instructions and examples, refer to the `documentation <https://docs.tingg.africa>`_.

Feedback
--------

Feel free to reach us through our `discussion forum <https://docs.tingg.africa/discuss>`_.
