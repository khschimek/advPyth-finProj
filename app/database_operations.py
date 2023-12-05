import requests
from . settings import END_POINT, HEADERS, PAYLOAD
from typing import Dict, Any, Optional
from bson import ObjectId


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


def find_data(query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Query data from the MongoDB collection.
    :param query: Dictionary representing the query to be executed.
    :return: User data if it exists, None otherwise.
    """
    if '_id' in query and isinstance(query['_id'], ObjectId):
        query['_id'] = str(query['_id'])

    url = f"{END_POINT}/action/find"
    payload = PAYLOAD.copy()
    payload['filter'] = query
    response = requests.post(url, json=payload, headers=HEADERS)
    data = response.json()

    if 'documents' in data and isinstance(data['documents'], list):
        if len(data['documents']) > 0:

            user_data = data['documents'][0]
            if isinstance(user_data, dict):
                if '_id' in user_data:
                    if isinstance(user_data['_id'], ObjectId):
                        user_data['_id'] = str(user_data['_id'])
                    return user_data

    return None
