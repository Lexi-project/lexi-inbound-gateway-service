import os
from dotenv import load_dotenv

load_dotenv()

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
USER_SERVICE_HOST = os.getenv('USER_SERVICE_HOST', '')
GRAPHQL_GATEWAY_HOST = os.getenv('GRAPHQL_GATEWAY_HOST', '')
USER_SERVICE_AUTHENTICATE_URL= os.getenv('USER_SERVICE_AUTHENTICATE_URL', '')