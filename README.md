Web Service Boilerplate
===

Boilerplate template for web service for Python

## Virtual Environment

```bash
python -m venv venv
source ./venv/vin/activate
```

## Installation

```bash
pip install -r requirement.txt
```

## Start Web Service

The web service is hosted by `Flask` (https://flask.palletsprojects.com) on port `5000`.

```bash
python main.py
```

## Test APIs

Use `curl` to test the `predict` api.

```bash
 curl -F "file=@image.png" -X POST http://localhost:5000/api/predict
```

p.s. assume the file name is `image.png`.
