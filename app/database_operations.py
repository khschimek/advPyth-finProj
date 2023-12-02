import requests
from .settings import END_POINT, HEADERS, PAYLOAD

def insert_data(data):
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

def find_data(query):
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

def update_data(filter, update):
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

def delete_data(filter):
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