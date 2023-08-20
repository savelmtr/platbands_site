from general.settings import EMAIL_BACKEND
from lib import email_backends

email_backend: email_backends.AbstractEmailBackend = getattr(email_backends, EMAIL_BACKEND)
