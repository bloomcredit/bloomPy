import re
import os
import json
from pathlib import Path
from requests import request, HTTPError, Timeout
from dotenv import load_dotenv


BLOOM_FOLDER = Path(__file__).parent.resolve()
load_dotenv(BLOOM_FOLDER / "endpoints.env")
load_dotenv()


# -----------------------------------------------------------------------------
#                           Utilities
# -----------------------------------------------------------------------------
def tokenize_json(fn, tokens):
    with open(BLOOM_FOLDER / fn, "r", encoding="utf-8") as json_file:
        json_data = json_file.read()

    tags = re.findall(r'(<.*>)', json_data)

    for tag in tags:
        try:
            repl = tokens[tag[1:-1]] or ""
            if isinstance(repl, bool):
                repl = "true" if repl else "false"
        except KeyError:
            repl = ""
        json_data = json_data.replace(tag, repl)
    return json_data


def coalesce(*arg):
    return next((a for a in arg if a is not None), None)


# -----------------------------------------------------------------------------
#                           fetch_auth_token
# -----------------------------------------------------------------------------

def fetch_auth_token(audience=None, client_id=None, client_secret=None, grant_type=None):
    """
    Retrieve a token from the Bloom Credit Authentication URL.
    https://developers.bloomcredit.io/docs/onboarding-to-first-credit-report#getting-an-access-token
    """

    payload = {
        'audience': coalesce(audience, os.getenv('BLOOM_AUDIENCE')),
        'client_id': coalesce(client_id, os.getenv('BLOOM_CLIENT_ID')),
        'client_secret': coalesce(client_secret, os.getenv('BLOOM_CLIENT_SECRET')),
        'grant_type': coalesce(grant_type, os.getenv('BLOOM_TOKEN_GRANT'))
    }

    if payload['audience'] == 'dev-api':
        url = os.getenv('BLOOM_SANDBOX_AUTH_URL')
    else:
        url = os.getenv('BLOOM_PRODUCTION_AUTH_URL')

    try:
        response = request(
            "POST",
            url,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()['access_token'], response.json()
    except KeyError:
        # No token was included in the response from the server
        return None, response.json()
    except Timeout:
        return None, "Server Timeout"
    except HTTPError as e:
        return None, f"{e.response.status_code}: {e.response.reason}"
    except Exception as e:
        return None, e


# -----------------------------------------------------------------------------
#                            get_portfolios
# -----------------------------------------------------------------------------

def get_portfolios(auth_token, audience=None):
    """Organizations are representations of a companies. They contain
    multiple Portfolios which represent Credit Products managed by a company.
    https://developers.bloomcredit.io/docs/onboarding-to-first-credit-report#fetching-your-organizations-portfolios
    """

    if coalesce(audience, os.getenv('BLOOM_AUDIENCE')) == 'dev-api':
        url = os.getenv('BLOOM_SANDBOX_ORG_URL')
    else:
        url = os.getenv('BLOOM_PRODUCTION_ORG_URL')

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {auth_token}"
    }

    try:
        response = request(
            "GET",
            url=url,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        return response.json()['data']['attributes']['portfolios'][0]['id'], response.json()
    except KeyError:
        # No consumer id returned from Bloom Credit
        return None, response.json()
    except Timeout:
        return None, "Server Timeout"
    except HTTPError as e:
        return None, f"{e.response.status_code}: {e.response.reason}"
    except Exception as e:
        return None, e


# -----------------------------------------------------------------------------
#                           register_consumer
# -----------------------------------------------------------------------------

def register_consumer(consumer_info, auth_token, audience=None):
    """ Consumers are representations of persons within the Bloom API.
    To order a credit report for a consumer, you first need to submit their information to Bloom.
    https://developers.bloomcredit.io/docs/onboarding-to-first-credit-report#creating-a-consumer
    """

    if coalesce(audience, os.getenv('BLOOM_AUDIENCE')) == 'dev-api':
        url = os.getenv('BLOOM_SANDBOX_CONSUMER_URL')
    else:
        url = os.getenv('BLOOM_PRODUCTION_CONSUMER_URL')

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {auth_token}"
    }

    payload = tokenize_json('consumer.json', consumer_info)

    try:
        response = request(
            "POST",
            url=url,
            headers=headers,
            data=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()['data']['id'], response
    except KeyError:
        # No consumer id returned from Bloom Credit
        return None, response.json()
    except Timeout:
        return None, "Server Timeout"
    except HTTPError as e:
        return None, f"{e.response.status_code}: {e.response.reason}"
    except Exception as e:
        return None, e


# -----------------------------------------------------------------------------
#                           order_credit_data
# -----------------------------------------------------------------------------
def order_credit_data(consumer_id, portfolio_id, sku, auth_token, audience=None):
    """ Once your consumer is created, you can order a credit report via the
    Bloom API. This order will be made for Bloom to fetch the credit report
    for your order.

    https://developers.bloomcredit.io/docs/onboarding-to-first-credit-report#ordering-a-credit-report
    """

    if coalesce(audience, os.getenv('BLOOM_AUDIENCE')) == 'dev-api':
        url = os.getenv('BLOOM_SANDBOX_ORDER_URL')
    else:
        url = os.getenv('BLOOM_PRODUCTION_CONSUMER_URL')

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {auth_token}"
    }

    payload = tokenize_json('order.json', {
        'consumer_id': consumer_id,
        'portfolio_id': portfolio_id,
        'sku': sku
    })

    try:
        response = request(
            "POST",
            url=url,
            headers=headers,
            data=payload,
            timeout=10
        )
        response.raise_for_status()
        return response.json()['data']['id'], response
    except KeyError:
        # No order id returned from Bloom Credit
        return None, response.json()
    except Timeout:
        return None, "Server Timeout"
    except HTTPError as e:
        return None, f"{e.response.status_code}: {e.response.reason}"
    except Exception as e:
        return None, e


# -----------------------------------------------------------------------------
#                           get_credit_data
# -----------------------------------------------------------------------------

def get_credit_data(order_id, auth_token, audience=None, outfile=None):

    if coalesce(audience, os.getenv('BLOOM_AUDIENCE')) == 'dev-api':
        url = os.getenv('BLOOM_SANDBOX_ORDERS_URL')
    else:
        url = os.getenv('BLOOM_PRODUCTION_ORDERS_URL')

    url = url.replace('<order_id>', order_id)

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {auth_token}"
    }

    try:
        response = request(
            "GET",
            url=url,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()

        if outfile is not None:
            with open(outfile, "w", encoding="utf-8") as f:
                f.write(json.dumps(response.json(), indent=4))

        return json.dumps(response.json(), indent=4), response.json()

    except Timeout:
        return None, "Server Timeout"
    except HTTPError as e:
        return None, f"{e.response.status_code}: {e.response.reason}"
    except Exception as e:
        return None, e
