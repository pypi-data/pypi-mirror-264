# This is a proof of concept of the Belenios election protocol.

## Installation

```
$ cd poc
$ pip install -r requirements.txt
$ python setup.py install
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:


### Create a virtualenv for development

```
$ cd poc
$ make virtualenv
$ source env/bin/activate
```

### Run belenios cli application
```
$ belenios --help
```

### Run an election automaticaly
```
$ cd poc
$ python3 tests/auto_election.py
```

### Run an election automaticaly (with Pedersen)
```
$ cd poc
$ python3 tests/auto_election_pedersen.py
```

### Run pytest / coverage
```
$ cd poc
$ make test
```


### Releasing to PyPi

Before releasing to PyPi, you must configure your login credentials:

**~/.pypirc**:

```
[pypi]
username = YOUR_USERNAME
password = YOUR_PASSWORD
```

Then use the included helper function via the `Makefile`:

```
$ cd poc
$ make dist
$ make dist-upload
```

## Deployments

### Docker

Included is a basic `Dockerfile` for building and distributing `Belenios`,
and can be built with the included `make` helper:

```
$ cd poc
$ make docker
$ docker run -it belenios --help
```
