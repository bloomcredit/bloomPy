# bloomPy
Use the Bloom Credit API with Python.


Credentials
-------------


To start the authentication process with the Bloom API, make sure you have both a client_id and client_secret ready to be used. Using these credentials, you will be able to generate the access token used to authenticate your API calls.  You will need to contact Bloom Credit for credentials.


Installation
-------------

To install, you can use pip:

    pip install git+https://github.com/CaffeineLab/bloomPy.git

 
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



