#\app\config.py
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_EXPIRATION_MINUTES = os.getenv('JWT_EXPIRATION_MINUTES')
SPACES_ENDPOINT = os.getenv('SPACES_ENDPOINT')
SPACES_ACCESS_KEY = os.getenv('SPACES_ACCESS_KEY')
SPACES_SECRET_KEY = os.getenv('SPACES_SECRET_KEY')
BUCKET_NAME = os.getenv('BUCKET_NAME')
SPACES_REGION = os.getenv('blr1')
DATABASE_URL = "mysql+pymysql://doadmin:AVNS_R-GQJAHUk5xZSriLERr@dbaas-db-2031020-do-user-17464047-0.i.db.ondigitalocean.com:25060/test"

if JWT_SECRET_KEY is None:
    raise ValueError("JWT_SECRET_KEY is not set")
if JWT_EXPIRATION_MINUTES is None:
    raise ValueError("JWT_EXPIRATION_MINUTES is not set")
if SPACES_ENDPOINT is None:
    raise ValueError("SPACES_ENDPOINT is not set")
if BUCKET_NAME is None:
    raise ValueError("BUCKET_NAME is not set")


JWT_EXPIRATION_MINUTES = int(JWT_EXPIRATION_MINUTES)
