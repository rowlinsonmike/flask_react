## project setup

`npm run setup`

installs all project packages

`npm run bootstrap`

executes `bootstrap.py` which does the following
- creates user dynamodb table

## run dev mode

`npm run dev`

executes parallel environments of flask and cra

## run a deployment

`npm run build`

builds a disto of cra

`npm run deploy`

starts application using gunicorn

## File breakdown

- /Dockerfile = spin up container of the application
- /bootstrap.py = create/destroy project resources prior to execution
- /gunicorn.conf.py = configuration file gunicorn leverages by default when setting configs in production, ie `npm run deploy`
- /.env = required environment variables to be leveraged by flask app
- /client/ = CRA
- /api/ = flask server

## .env Variables

```
FLASK_APP=api
FLASK_ENV=development
FLASK_RUN_PORT=8080
JWT_SECRET_KEY=$2b$12$kKUyJR2WN4OzpiTErmDwju
DYNAMO_USER_TABLE=USERAUTH
AWS_REGION=us-east-1
CORS_HEADERS=Content-Type
JWT_TOKEN_LOCATION=cookies
JWT_COOKIE_SECURE=False
JWT_COOKIE_CSRF_PROTECT=True
```


## Cleanup

`npm run teardown`

executes `bootstrap.py` which does the following
- destroys user dynamodb table