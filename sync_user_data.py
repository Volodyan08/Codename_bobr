import os

import requests
from dotenv import load_dotenv

from import_user_data import insert_users_to_db

load_dotenv()

url = "https://api.nimble.com/api/v1/contacts"
bearer_token = os.getenv("BEARER_TOKEN")

headers = {
    "Authorization": f"Bearer {bearer_token}"
}


def get_users_from_request():
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()

            persons_data = [record for record in data.get("resources") if record.get("record_type") == "person"]
            users = [
                {
                    "first_name": person["fields"]["first name"][0]["value"],
                    "last_name": person["fields"]["last name"][0]["value"],
                    "email": person["fields"]["email"][0]["value"]
                }
                for person in persons_data
                if "email" in person["fields"]
                   and "first name" in person["fields"]
                   and "last name" in person["fields"]
            ]

            return users
        else:
            print(f"Request failed with status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    users = get_users_from_request()
    insert_users_to_db(users)
