# COS Python Sample App
 
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/54720664bb154753b702214a5cc81a2e)](https://app.codacy.com/gh/namely/cos-python-sample/dashboard)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/54720664bb154753b702214a5cc81a2e)](https://app.codacy.com/gh/namely/cos-python-sample/dashboard)

Sample gRPC python application using [Chief of State](https://github.com/namely/chief-of-state).

### Overview

This sample application uses Chief of State to build a [Bank Account service](./proto/local/banking_app/api.proto) that tracks debit/credit [events](./proto/local/banking_app/events.proto) to derive the current balance.

```
code
├── banking_app             # generated gRPC service code
├── banking_app_impl        # implements the banking service
├── chief_of_state          # generated COS code
├── read_handler_impl       # implements the COS read side handler
├── shared                  # shared helpers
├── test_client             # test client for sample traffic
└── write_handler_impl      # implements the COS write side handler
```

### Quickstart

```bash
# update submodules
git submodule update --init

# download earth
brew install earthly

# updates submodules, generates protobufs
earthly +all

# starts all containers
docker-compose up -d

# create sample traffic
docker-compose exec test-client python -m test_client

# OTHER HELPFUL COMMANDS

# only generate protobufs locally
earthly +protogen

# supervise app logs
docker-compose logs -f --tail="all" api write-handler read-handler

# cos logs
docker-compose logs -f chiefofstate
```

### installing dependencies for local dev in an IDE
```bash
# configure virtual env
python -m venv .venv

# activate it
. .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```
