# bloomcredit-python
Use the Bloom Credit API with Python.


Credentials
-------------


To start the authentication process with the Bloom API, make sure you have both a client_id and client_secret ready to be used. Using these credentials, you will be able to generate the access token used to authenticate your API calls.  You will need to contact Bloom Credit for credentials.


**Audience** will determine which endpoint you will submit your requests through.  Either dev-api or api.bloomcredit.io.

Installation
-------------

To install, you can use pip:

    pip install git+https://github.com/bloomcredit/bloompy

 
Environmental Variables
-------------

You can store your API keys in a .env file in the root of your project.  Either create the file using the template below, or use the provided .env.example file.  Make sure to replace the placeholders with the provided API key for the system being accessed.  

```
BLOOM_CLIENT_ID=<client_id>
BLOOM_CLIENT_SECRET=<client_secret>
BLOOM_AUDIENCE=<audience>
```

Usage
-------------

### Fetch Token
```
# Fetch Token using credentials stored in the .env file
auth_token, response = bloom.fetch_auth_token()
print(auth_token)
```

```
# Fetch Token ignoring credentials stored in the .env file
auth_token, response = bloom.fetch_auth_token(
    audience="<audience>",
    client_id="<client_id>",
    client_secret="<client_secret>",
    grant_type="client_credentials"
)
print(auth_token)
```

### Fetch Portfolios
Just a reference function for pulling the list of portfolios for the current organization.
 ```
portfolio_id, response = bloom.get_portfolios(
    auth_token=auth_token
)
```

### Register Consumer
 ```
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
    consumer_info=consumer_info,
    auth_token=auth_token
)
```

### Order Credit Data
 ```
credit_order, response = bloom.order_credit_data(
    consumer_id=consumer_id,
    portfolio_id=portfolio_id,
    sku="equifax-gold-soft-fico-internet",
    auth_token=auth_token
)
```

### Get Credit Data
If you use the outfile parameter, it will save the response from Bloom Credit into the given filepath.
 ``` 
credit_data, response = bloom.get_credit_data(
    order_id=credit_order,
    auth_token=auth_token,
    outfile="credit_data.json"
)
```
