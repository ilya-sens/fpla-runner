import json

import requests

base_url = "http://localhost:8084/crud/name/"
headers = {'Content-type': 'application/json', 'Accept': 'text/json'}


def get_all(table_name):
    return requests.get(base_url + table_name).json()


def create(table_name, json_data):
    return requests.post(base_url + table_name, data=json_data, headers=headers)


def update(table_name, json_data):
    return requests.put(base_url + table_name + "/" + json_data["ID"], data=json_data, headers=headers)


def delete(table_name, row_id):
    return requests.delete(base_url + table_name + row_id)


