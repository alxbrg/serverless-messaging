# Serverless messaging

A bare-bones messaging API implemented using Lambda functions written in Python, DynamoDB, SNS and SES.
The [Serverless framework](https://serverless.com) is used to provision the Lambdas and the DynamoDB table.

## API Usage

All requests must have a valid API key value set in the `x-api-key` header.

_Note_: for demonstration purposes, a single key is configured to be generated.

### Send and store a message

`POST` `/messages`

__Request body__:

| Property        | Type     | Required | Description                |
|-----------------|----------|----------|----------------------------|
| `body`          | `string` | `true`   | The content of the message |
| `recipient`     | `string` | `true`   | The name of the recipient  |
| `email_address` | `string` | `false`  | A valid email address      |
| `phone_number`  | `string` | `false`  | A valid phone number       |

_Note_: At least one of the `email_address` and `phone_number` properties must be provided.

### Retrieve messages by recipient

`GET` `/messages`

__Query string__:

| Parameter       | Type     | Required | Description                |
|-----------------|----------|----------|----------------------------|
| `recipient`     | `string` | `true`   | The name of the recipient  |

## Running the project locally

### Prerequisites

- Have `python3`, `pip` and `virtualenv` installed
- Have `node` and `npm` installed, as the project relies on the Serverless to spin the lambdas locally
- Have `docker` installed, to run a local DynamoDB container
- Create a `.env` file at the root of the project (refer to the [example.env file](/example.env) for
its content)
- _Caveat_: the associated AWS account must be out of the SES sandbox to send emails to unverified
email addresses

### Install dependencies

```bash
# install npm dependencies
npm install

# create and activate a virtual env and install Python dependencies
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

### Start the API

```bash
npm start
```

This will start a `DynamoDB` container on port `8000` and launch a local API Gateway on port `3000`.

_Note_: if no `DB_CONNECTION_STRING` is provided, AWS DynamoDB will be used, removing the need for a
local DynamoDB instance. In this case, the API can be run with `npx dotenv sls offline`.

### Run the tests

```bash
python -m pytest --disable-pytest-warnings tests/ -v

# or for convenience:
npm test
```

## Deploying

### Prerequisites

- Have `python3`, `pip`, `virtualenv`, `node` and `npm` installed (`docker` as well for non-linux
OSs –– see [serverless-python-requirements](https://www.npmjs.com/package/serverless-python-requirements#cross-compiling))
- AWS credentials must be configured
- `DB_TABLE_MESSAGES` and `SOURCE_EMAIL_ADDRESS` parameters must be set in the SSM parameter store

### Deploy

```bash
npm run deploy
```

### CI/CD

The project uses CircleCI for its CI/CD. Tests will run for all pull requests and the lambdas are
automatically deployed when the `master` branch is updated.

## TODO

- Handle security (configure: VPC, subnets, security groups)
- Sanitize inputs
- Add unit and integration tests
- Format the API Gateway Error model to be consistent with the internal [ApiError class](/messaging/helpers/errors.py)
- Optimize the lambdas (package them separately, exclude unwanted packages and files)
- Document the code more
