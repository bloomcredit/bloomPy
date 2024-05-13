# bloomPy
Use the Bloom Credit API with Python.


# .env


```
BLOOM_CLIENT_ID=<client_id>
BLOOM_CLIENT_SECRET=<client_secret>
BLOOM_AUDIENCE=<audience>

# Token/Authorization
BLOOM_TOKEN_GRANT=client_credentials
BLOOM_SANDBOX_AUTH_URL=https://auth.bloom.dev/oauth/token
BLOOM_PRODUCTION_AUTH_URL=https://auth.bloomcredit.io

# Environment parameters
# https://developers.bloomcredit.io/docs/environments-1#per-environment-parameters
# Use the full enpoint URL to account for version changes.

BLOOM_SANDBOX_ORG_URL=https://sandbox.bloom.dev/v2/core/organization
BLOOM_PRODUCTION_ORG_URL=https://api.bloomcredit.io/v2/core/organization

BLOOM_SANDBOX_CONSUMER_URL=https://sandbox.bloom.dev/v2/core/consumers
BLOOM_PRODUCTION_CONSUMER_URL=https://api.bloomcredit.io/v2/core/consumers

BLOOM_SANDBOX_ORDER_URL=https://sandbox.bloom.dev/v2/data-access/orders
BLOOM_PRODUCTION_CONSUMER_URL=https://api.bloomcredit.io/v2/data-access/orders

BLOOM_SANDBOX_ORDERS_URL=https://sandbox.bloom.dev/v2/data-access/orders/<order_id>/full-report
BLOOM_PRODUCTION_ORDERS_URL=https://api.bloomcredit.io/v2/data-access/orders/<order_id>/full-report=https://bloom.dev/v2/data-access/orders/<order_id>/full-report

```