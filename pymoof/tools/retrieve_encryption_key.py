import base64
import getpass

import requests


def query():
    API_URL = "https://my.vanmoof.com/api/v8"
    API_KEY = "fcb38d47-f14b-30cf-843b-26283f6a5819"

    username = input("Username: ")
    password = getpass.getpass()

    headers = {
        "Api-Key": API_KEY,
        "Authorization": "Basic "
        + base64.b64encode((username + ":" + password).encode()).decode("ascii"),
    }

    result = requests.post(API_URL + "/authenticate", headers=headers)
    result = result.json()

    if "error" in result:
        raise Exception("error", result)

    token = result["token"]

    headers = {
        "Api-Key": API_KEY,
        "Authorization": "Bearer " + token,
    }

    result = requests.get(
        API_URL + "/getCustomerData",
        headers=headers,
        params={"includeBikeDetails": ""},
    )
    result = result.json()

    # Only get the first bike's encryption key
    return result["data"]["bikeDetails"][0]["key"]["encryptionKey"]


if __name__ == "__main__":
    print(query())
