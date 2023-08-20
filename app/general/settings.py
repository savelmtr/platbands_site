import os


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '')   # Специально для JWT
SECRET = os.getenv('SECRET', '')   # Для общих задач
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'SimpleBackend')
BASE_EMAIL = os.getenv('BASE_EMAIL', '')
BASE_URL = os.getenv('BASE_URL', '')
URL_FOR_RESET_PASS = os.getenv('URL_FOR_RESET_PASS', '')
PASSWORD_RESET_TOKEN_MAX_DAYS = 2
