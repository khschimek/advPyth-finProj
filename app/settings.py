"""Settings for the app.
"""
from typing import Dict, Any

END_POINT = 'https://us-west-2.aws.data.mongodb-api.com/app/'
END_POINT += 'data-qdbnx/endpoint/data/v1'
API_KEY = 'MMkqL68awB0hmRe6DfLvk48tdSS080Y2ygecsAEbbkguWiLkhPcsIXIrOVt2Z6So'
DATA_SOURCE = 'Cluster0'
DB_NAME = 'weatherapp'
COLLECTION = 'users'
HEADERS = {'Content-Type': 'application/json',
           'Access-Control-Request-Headers': '*',
           'api-key': f'{API_KEY}'}

PAYLOAD: Dict[str, Any] = {
    "collection": COLLECTION,
    "database": DB_NAME,
    "dataSource": DATA_SOURCE
}
