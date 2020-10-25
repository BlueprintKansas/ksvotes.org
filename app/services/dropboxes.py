from app.services.ksvotes_redis import KSVotesRedis
from airtable import Airtable
import os
import json
from flask import current_app

class Dropboxes():
  def __init__(self, county):
    self.dropboxes = None

    # disabled w/o this env var set
    if not os.getenv('AIRTABLE_DROPBOX_TABLE'):
      return

    self.county = county

    # look first in redis cache
    self.dropboxes = self.get_cached_dropboxes()

    # otherwise fetch and cache
    if not self.dropboxes:
      self.dropboxes = self.fetch_dropboxes()

  def cache_key(self):
    return "dropboxes1-{}".format(self.county)

  def get_cached_dropboxes(self):
    redis = KSVotesRedis()
    boxes = redis.get(self.cache_key())
    if boxes:
      return json.loads(boxes)
    else:
      return None

  def fetch_dropboxes(self):
    redis = KSVotesRedis()
    airtable = Airtable(os.getenv('AIRTABLE_EV_BASE_ID'), os.getenv('AIRTABLE_DROPBOX_TABLE'), os.getenv('AIRTABLE_EV_KEY'))
    response = airtable.get_all(formula="AND( COUNTY = '{}' )".format(self.county.upper()))

    # some counties do not have actual locations
    if 'LOCATION' not in response[0]['fields']:
      return

    boxes = []
    for db in response:
      evl = { 'location': db['fields']['LOCATION'], 'hours': db['fields']['HOURS'] }
      boxes.append(evl)

    redis.set(self.cache_key(), json.dumps(boxes).encode(), os.getenv('EVL_TTL', '3600'))
    return boxes
