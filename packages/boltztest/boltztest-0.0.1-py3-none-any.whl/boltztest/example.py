import requests


def get_boltzbit_landing_page():
    resp = requests.get("https://boltzflow.com")
    resp.raise_for_status()
    return resp.text
