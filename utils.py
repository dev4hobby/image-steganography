from hashlib import md5
from datetime import datetime

def get_timestamp_as_md5():
  return md5(str(datetime.now()).encode('utf-8')).hexdigest()
