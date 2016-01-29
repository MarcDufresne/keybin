# Keybin API Server

This app serves as a Generic Data Store API. All you need is a MongoDB instance.

Usage is simple, you register an account, generate a token and use that to push arbitrary data as key/value pairs.
All data stored with this API will be tied to the account you registered and you will need a token to access it later.

Tokens automatically expire after a set amount of time has passed. That duration is configured within the `store.cfg` 
file and will be show to users when they generate a token.

## Configuration

    [APP]
    # Host on which to listen for connections
    host=127.0.0.1
    # Port on which to run the server
    port=5000
    # If Flask debug should be enabled
    debug=true
    
    [STORE]
    # Your MongoDB instance's IP
    host=mongodb://<IP:PORT>/
    # Database name
    database=store
    # Collection names
    store_collection=store
    users_collection=users
    token_collection=tokens
    # Token expiration in seconds
    token_expiration=300

## API Documentation

### POST `/register`

Used to register an account on the API

#### Body

    {
        username: <string>,
        password: <string>
    }

#### Response

    {
        "result": "ok"
    }
    
### DELETE `/unregister`

Used to delete an account and token as well as all stored data for that account

#### Body

    {
        username: <string>,
        password: <string>
    }

#### Response

    {
        "result": "ok"
    }
    
### POST `/token`

Used to generate a token to use with the store API, invalidates all previous tokens. 
`client_id` allows you to generate tokens for different devices without invalidating the previous ones.

#### Body

    {
        username: <string>,
        password: <string>,
        client_id: <string> (optional, defaults to 'default')
    }

#### Response

    {
        "token": {
            "expire_seconds": <integer>,
            "token": <uuid>
        }
    }

### GET `/user/<token>/keys`

Returns all the keys associated with the account identified by the token

#### Response

    {
        "keys": [<string>,...]
    }

### GET `/user/<token>/store/<key>`

Returns the data associated with the specified key

#### Response

    {
        "value": <string>
    }
    
### POST `/user/<token>/store/<key>`

Adds some data in the store, if the key already exists the data is overwritten. A key can only contains 
characters `a-z`, `A-Z`, `0-9`, `_`, `.` and `,`.  

#### Body

    {
        "value": <string>
    }
    
#### Response

    {
        "result": "ok"
    }
    
## Library

[Python Keybin Client](https://github.com/MarcDufresne/keybin-client)
