# rsa

[![license](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/AleksaC/rsa/blob/master/LICENSE)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/AleksaC/rsa/blob/master/.pre-commit-config.yaml)

The most overengineered educational implementation of RSA algorithm.

## About
This project was done in collaboration with [Nikola Ivanović](https://github.com/Buddypas),
[Petar Ćetković](https://github.com/PetarCetkovic) and [Petar Vujović](https://github.com/petarvujovic98)
for a cryptography course at our university.

This repo includes:
- a python library implementing rsa algorithm (key generation,
encryption and decryption) along with some utilities (i.e. rabin-miller
primality test)
- cli exposing the main functionality of the library
- flask server exposing the main functionality of the library through a REST API
- Simple website that uses the api to perform the aforementioned actions through
a nice interface

While working on this project we tried to follow best practices:
- All the relevant code is documented
- The entire project (except for the frontend) is covered with tests
- The entire project is formatted and linted according to a set of predefined rules
- The entire core library is type-annotated and type-checked using mypy
- Testing, linting and type-checking are ran in CI with ability to fix and push
back incorrectly styled code

## Getting started
### Library
To learn more about the core library of this project check out its
[README](algorithm/README.md).

### Web app
#### With Docker
The easiest way to spin up both backend and frontend is using docker compose.
To run development version run the following command:
```shell script
docker-compose up
```
Backend API will be exposed through port 5000 and frontend will be available
at port 3000.

To run a production version use:
```shell script
docker-compose up -f docker-compose.yml
```

#### Without Docker
To run the frontend in development mode outside of docker use (provided that you
have already installed all the dependencies using `npm install`):
```shell script
npm start
```
Running:
```shell script
npm run build
```
produces the production bundle in the `frontend/dist` directory. You can move it
to `/usr/share/nginx/html` and add the provided `nginx.conf` to `/etc/nginx/conf.d/`
or `/etc/nginx/sintes-enabled/` depending on your existing nginx configuration.

To run the backend in development mode, simply run the `backend/app.py` file:
```shell script
python app.py
```
To run the API in production you can use the following command (assuming you are
using a unix machine):
```shell script
gunicorn \
    --workers=$((2 * $(getconf _NPROCESSORS_ONLN) + 1)) \
    --bind 0.0.0.0:5000 \
    app:app
```
Note that you need to install the `backend/requirements.txt` before running the
API in either mode.

## Running tests
The recommended way to run tests is using `tox`, by simply running:
```shell script
tox
```
It will run all tests with coverage and doctest against multiple versions of
python interpreter (you need to have at least one of them installed on your
machine). You can also run test only for specific interpreter:
```shell script
tox -e py38
```
You can also run tests by running `./runtests.sh` which is used by tox to run
tests, but before running it you need to have `requirements-test.txt` installed.

## Contact
- [Personal website](https://aleksac.me)
- <a target="_blank" href="http://twitter.com/aleksa_c_"><img alt='Twitter followers' src="https://img.shields.io/twitter/follow/aleksa_c_.svg?style=social"></a>
- aleksacukovic1@gmail.com
