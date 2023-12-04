import requests
from . settings import END_POINT, HEADERS, PAYLOAD
from typing import Dict, Any


def insert_data(data: Dict[str, Any]) -> Any:
    """
    Insert data into the MongoDB collection.
    :param data: Dictionary containing the data to be inserted.
    :return: Response from the database.
    """
    url = f"{END_POINT}/action/insertOne"
    payload = PAYLOAD.copy()
    payload['document'] = data
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()


def find_data(query: Dict[str, Any]) -> Any:
    """
    Query data from the MongoDB collection.
    :param query: Dictionary representing the query to be executed.
    :return: Response from the database.
    """
    url = f"{END_POINT}/action/find"
    payload = PAYLOAD.copy()
    payload['filter'] = query
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()


def update_data(filter: Dict[str, Any], update: Dict[str, Any]) -> Any:
    """
    Update data in the MongoDB collection.
    :param filter: Dictionary representing the query to match documents.
    :param update: Dictionary representing the update to be applied.
    :return: Response from the database.
    """
    url = f"{END_POINT}/action/updateOne"
    payload = PAYLOAD.copy()
    payload['filter'] = filter
    payload['update'] = update
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()


def delete_data(filter: Dict[str, Any]) -> Any:
    """
    Delete data from the MongoDB collection.
    :param filter: Dictionary representing the query to match documents.
    :return: Response from the database.
    """
    url = f"{END_POINT}/action/deleteOne"
    payload = PAYLOAD.copy()
    payload['filter'] = filter
    response = requests.post(url, json=payload, headers=HEADERS)
    return response.json()
