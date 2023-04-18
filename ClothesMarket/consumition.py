import requests
import json


def obtain():
    response = requests.get("http://127.0.0.1:8000/branch/643d04ec928a46c2c2911fd7")
    print(json.dumps(response.json(), indent=4))


obtain()