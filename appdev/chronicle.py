from datetime import datetime
from fastparquet import write
from pandas import DataFrame
from boto3 import client

BUCKET = 'appdev-register'
PATH = '/tmp'

class ChronicleSession:
  def __init__(self, access_key, secret_key, app, cache_size=10):
    self.s3 = client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    self.app = app
    self.cache_size = cache_size
    self.log_map = dict()

  def log(self, event_name, event):
    if event_name not in self.log_map:
      self.log_map[event_name] = [event]
      return

    logs = self.log_map[event_name]
    logs.append(event)
    self.log_map[event_name] = logs
    if len(logs) >= self.cache_size:
      self.write_logs(event_name)

  def write_logs(self, event_name):
    organized = dict()
    for event in self.log_map[event_name]:
      for key in event.keys():
        if key not in organized.keys():
          organized[key] = [event[key]]
        else:
          organized[key].append(event[key])
    df = DataFrame(organized)
    file_name = str(datetime.now()) + '.parquet'
    write(PATH + '/' + file_name, df)
    self.s3.upload_file(PATH + '/' + file_name, BUCKET, self.app + '/' + event_name + '/' + file_name)
