import os
from dotenv import load_dotenv

load_dotenv()

oauth2_github_client_id = "b09d90f4e8f24e634d28"
oauth2_github_client_secret = "c11d378fc9647edbde7a28fde568e77e1998b8a6"

minio_settings = {
    'endpoint': os.environ.get('MINIO_ENDPOINT') or 'minioo:9000',
    'access_key': 'root',
    'secret_key': 'qwerty123',
    'secure': False,
}

db_name = 'storage_db'
postgres_settings = {
    'host': os.environ.get('POSTGRES_HOST') or 'pg', 
    'port': 5432, 
    'user': 'postgres', 
    'password': 'mysecretpassword'
}
