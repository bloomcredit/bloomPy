"""Interface for Bloom Credit Report Retrieval."""

import json
from bloom import bloom

# -----------------------------------------------------------------------------
#                           fetch_auth_token
# -----------------------------------------------------------------------------

# To use the .env file, do not pass credentials. Eg:
# auth_token = bloom.fetch_auth_token()

# Override the .env file credentials.
auth_token = bloom.fetch_auth_token(
    audience=None,
    client_id=None,
    client_secret=None,
    grant_type=None
)

# -----------------------------------------------------------------------------
#                           fetch_portfolios
# -----------------------------------------------------------------------------
# TODO: Clarify multiple portfolios process.  Determine which to use.

portfolio_id = bloom.get_portfolios(
    audience='dev-api',
    auth_token=auth_token
)

# -----------------------------------------------------------------------------
#                           register_consumer
# -----------------------------------------------------------------------------

consumer_info = {
    "ssn": "123456789",
    "city": "Scranton",
    "line1": "1725 Slough Avenue",
    "state_code": "PA",
    "zipcode": "18503",
    "date_of_birth": "1964-03-15",
    "first_name": "Michael",
    "last_name": "Scott",
    "address_primary": True
}

consumer_id = bloom.register_consumer(
    audience='dev-api',
    consumer_info=consumer_info,
    auth_token=auth_token
)

# -----------------------------------------------------------------------------
#                           order_credit_data
# -----------------------------------------------------------------------------
credit_order = bloom.order_credit_data(
    audience='dev-api',
    consumer_id=consumer_id,
    portfolio_id=portfolio_id,
    sku="equifax-gold-soft-fico-internet",
    auth_token=auth_token
)

# -----------------------------------------------------------------------------
#                           get_credit_data
# -----------------------------------------------------------------------------

credit_data = bloom.get_credit_data(
    audience='dev-api',
    order_id=credit_order,
    auth_token=auth_token
)

print(json.dumps(credit_data, indent=4))
