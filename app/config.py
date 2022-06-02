import os
from dotenv import load_dotenv

load_dotenv()

oauth2_github_client_id = "b09d90f4e8f24e634d28"
oauth2_github_client_secret = "c11d378fc9647edbde7a28fde568e77e1998b8a6"

q1 = 'minioo:9000'
if os.environ.get('MINIO_ENDPOINT') is not None:
    q1 = os.environ.get('MINIO_ENDPOINT')

q2 = 'pg'
if os.environ.get('POSTGRES_HOST') is not None:
    q2 = os.environ.get('POSTGRES_HOST')

minio_settings = {
    'endpoint': q1,
    'access_key': 'root',
    'secret_key': 'qwerty123',
    'secure': False,
}

db_name = 'storage_db'
postgres_settings = {
    'host': q2, 
    'port': 5432, 
    'user': 'postgres', 
    'password': 'mysecretpassword'
}
