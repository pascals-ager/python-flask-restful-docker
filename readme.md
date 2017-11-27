Readme - vimcar coding challenge
###################################

The application exposes three apis @ endpoint /api:

1. /signup -Allowed methods - HTTP POST

In - Request header:

        {
            'email': 'test@example.com',
            'password': 'password'
        }

On request, the user is created after basic checks to check pre-existence, and a confirmation link is sent out


Out - Response json :

	{
		"confirmation_url": "http://0.0.0.0:8000/api/confirm/InNoaXZhbnkucG93YW5pQGdtYWlsLmNvbSI.DPzEnw.cZmP6GlLLz64oTGiOQHGlVivW34"
	}

Ideally, the activation link is sent via email; for testing purposes it is sent in the response message. On click of the activation link confirms the above user.


2. /confirm/{token} - Allowed methods - HTTP GET

In - The confirmation url from step 1

The token parameter is decoded and the right user (test@example.com, in this case) is confirmed.

Out - Response json:
	{
		'confirmation_message': 'User test@example.com is confirmed'
	}

3. /sign - Allowed methods - HTTP GET

In - A request header with username and password of an already registered and confirmed user.

        {
            'email': 'test@example.com',
            'password': 'password'
        }

Out - A jwt token is returned which is valid for the next 30 mins. The token shall be used as a bearer to access protected service apis.
      Response json:	
	
	{
		token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJhZHZpdGgubmFnYXBwYUBnbWFpbC5jb20iLCJleHAiOjE1MTE3MjMzOTZ9.G0uOOJCaG8tTSCaFQ4YMUrutX2cZ29bdTzqdLd2WTZY"
	}

4. /service - Allowed methods - HTTP GET with a valid bearer token

In - A request with a authorization header comprising a vlaid bearer token
	{
		'Authorization': "Bearer 			eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJzaGl2YW55LnBvd2FuaUBnbWFpbC5jb20iLCJleHAiOjE1MTE3MjM2MDN9.jlAfrEAq5XrdgJNFcK7rYbzARZEd9gV5iFScsfzCDM8"
	}

Out - The service can be accessed only if the token is valid
	Response message:
	'User test@example is accessing the protected service using a bearer token'

The use of a jwt token for request authentication is preferred here as a best practice for api first approach to back-end design. Jwt's provide a light-weight authorization mechanism versus passing the username/password in the request headers, which increases the vulnerabality of the username/password. Whereas a jwt token can be emphemeral and can be revoked or sandboxed within time boundaries.

###############################################################
Testing the application - unittests
###############################################################

1. Navigate to root, and run docker build
	docker-compose build
2. Bring up the docker containers 
	docker-compose up
3. SSH into the docker application container
	sudo docker exec -i -t restfulflask_vimcar_1 /bin/bash
4. From the home directory, run the unittests
	python -m unittest

 Only the happy path end to end functions of the challenge are covered as part of the scope of this test



###############################################################
Application components
###############################################################
Key libraries used:
	1. Flask
	2. Flask-Sqlalchemy
	3. Flask-restful
	4. python jwt tokens

Databse: Postgres database

Server: Gunicorn

Containers: 
	1. A docker Webcontainer running the flask and gunicorn app at port 8000
	2. A container running the postgresdb with a mounted volume at posrt 5432






