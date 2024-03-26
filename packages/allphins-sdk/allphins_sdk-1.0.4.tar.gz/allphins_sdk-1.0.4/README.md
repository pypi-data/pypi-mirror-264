# allphins-sdk
Allphins SKD repository

## How to contribute

1) Install pre-commit hook
```bash
> pre-commit install
```

2) Convention followed

- [PEP8](https://www.python.org/dev/peps/pep-0008/) -> 120 characters per line

- [Google Python Style Docstring]

## Requirements
* [Poetry](https://python-poetry.org/docs/#installation)
* [Docker](https://docs.docker.com/get-docker/)
* [Docker-compose](https://docs.docker.com/compose/install/)

## How to set up poetry environment
To set up your development environment using poetry you have to install all the dependencies using:

```
poetry install --with dev
```

You can also run the documentation on a local environment:

```
poetry run mkdocs serve
```
The documentation will be running on your localhost port 8000

Finally, you can run the unit test using the following command:  

```
poetry run coverage run --source=./allphins tests && poetry run coverage report --fail-under=80
```

## Mock allphins-api
You can mock the allphins-api by using the following command:
```
docker-compose up -d
```
All calls to localhost:8080 will be redirected to the mock server.
You can update the mock server by updating the files in the stubs/allphins-api folder.

This is required before runing local tests.