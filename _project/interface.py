"""Interface for Bloom Credit Report Retrieval."""
from src.bloom import bloom

# -----------------------------------------------------------------------------
#                           fetch_auth_token
# -----------------------------------------------------------------------------

# To use the .env file, do not pass credentials. Eg:
# auth_token = bloom.fetch_auth_token()

# Override the .env file credentials.
auth_token, response = bloom.fetch_auth_token(
    audience=None,
    client_id=None,
    client_secret=None,
    grant_type=None
)

# -----------------------------------------------------------------------------
#                           fetch_portfolios
# -----------------------------------------------------------------------------
# TODO: Clarify multiple portfolios process.  Determine which to use.

portfolio_id, response = bloom.get_portfolios(
    auth_token=auth_token,
    audience=None
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

consumer_id, response = bloom.register_consumer(
    audience=None,
    consumer_info=consumer_info,
    auth_token=auth_token
)

# -----------------------------------------------------------------------------
#                           order_credit_data
# -----------------------------------------------------------------------------
credit_order, response = bloom.order_credit_data(
    audience=None,
    consumer_id=consumer_id,
    portfolio_id=portfolio_id,
    sku="equifax-gold-soft-fico-internet",
    auth_token=auth_token
)

# -----------------------------------------------------------------------------
#                           get_credit_data
# -----------------------------------------------------------------------------

credit_data, response = bloom.get_credit_data(
    audience=None,
    order_id=credit_order,
    auth_token=auth_token,
    outfile="credit_data.json"
)

