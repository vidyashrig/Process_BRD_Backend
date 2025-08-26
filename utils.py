from datetime import datetime
from constants import LOCAL_TIMEZONE

def get_local_now():
    # Use aware datetime now in the local timezone
    return datetime.now(LOCAL_TIMEZONE)
