import uuid
from datetime import datetime

def generate_event_id():

    return str(uuid.uuid4())

def utc_now():

    return datetime.utcnow().isoformat()

def safe_divide(a, b):

    if b == 0:
        return 0

    return a / b