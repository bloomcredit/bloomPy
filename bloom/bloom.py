import re
import os
from pathlib import Path
from requests import request, HTTPError, Timeout
from dotenv import load_dotenv

load_dotenv()
BLOOM_FOLDER = Path(__file__).parent.resolve()


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


# -----------------------------------------------------------------------------
#                           fetch_auth_token
# -----------------------------------------------------------------------------

def fetch_auth_token(audience=None, client_id=None, client_secret=None, grant_type=None):
    """
    Retrieve a token from the Bloom Credit Authentication URL.
    https://developers.bloomcredit.io/docs/onboarding-to-first-credit-report#getting-an-access-token
    """

    audience = audience or os.getenv('BLOOM_AUDIENCE')

    if audience == 'dev-api':
        url = os.getenv('BLOOM_SANDBOX_AUTH_URL')
    else:
        url = os.getenv('BLOOM_PRODUCTION_AUTH_URL')

    payload = {
        'audience': audience,
        'client_id': client_id or os.getenv('BLOOM_CLIENT_ID'),
        'client_secret': client_secret or os.getenv('BLOOM_CLIENT_SECRET'),
        'grant_type': grant_type or os.getenv('BLOOM_TOKEN_GRANT')
    }

    try:
        response = request(
            "POST",
            url,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Partner': "2e114527-50e1-4857-bc14-7f20fe49b38f"
            },
            data=payload,
            timeout=10
        )

        response.raise_for_status()
        return response.json()['access_token']

    except KeyError:
        print('No token was included in the response from the server.')
        print(response.json())
    except Timeout:
        print('Server took too long to respond.')
    except HTTPError as e:
        print(f"{e.response.status_code}: {e.response.reason}")
    except Exception as e:
        print(e)
    return None


# -----------------------------------------------------------------------------
#                           register_consumer
# -----------------------------------------------------------------------------

def register_consumer(audience, consumer_info, auth_token):
    """ Consumers are representations of persons within the Bloom API.
    To order a credit report for a consumer, you first need to submit their information to Bloom.
    https://developers.bloomcredit.io/docs/onboarding-to-first-credit-report#creating-a-consumer
    """

    if audience == 'dev-api':
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
        return response.json()['data']['id']
    except KeyError:
        print('No consumer id returned from Bloom Credit.')
        print(response.json())
    except Timeout:
        print('Server took too long to respond.')
    except HTTPError as e:
        print(f"{e.response.status_code}: {e.response.reason}")
        print(f"{e.response.json()['errors'][0]['detail']}")
    except Exception as e:
        print(e)
    return None


# -----------------------------------------------------------------------------
#                           order_credit_data
# -----------------------------------------------------------------------------
def order_credit_data(audience, consumer_id, portfolio_id, sku, auth_token):
    """ Once your consumer is created, you can order a credit report via the
    Bloom API. This order will be made for Bloom to fetch the credit report
    for your order.

    https://developers.bloomcredit.io/docs/onboarding-to-first-credit-report#ordering-a-credit-report
    """

    if audience == 'dev-api':
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
        return response.json()['data']['id']
    except KeyError:
        print('No order id returned from Bloom Credit.')
        print(response.json())
    except Timeout:
        print('Server took too long to respond.')
    except HTTPError as e:
        print(f"{e.response.status_code}: {e.response.reason}")
        print(f"{e.response.json()['status_message']}")
    except Exception as e:
        print(e)
    return None


# -----------------------------------------------------------------------------
#                           get_credit_data
# -----------------------------------------------------------------------------

def get_credit_data(audience, order_id, auth_token):

    if audience == 'dev-api':
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
        return response.json()
    except Timeout:
        print('Server took too long to respond.')
    except HTTPError as e:
        print(f"{e.response.status_code}: {e.response.reason}")
    except Exception as e:
        print(e)
    return None
