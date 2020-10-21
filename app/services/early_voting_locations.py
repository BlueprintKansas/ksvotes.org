from app.services.ksvotes_redis import KSVotesRedis
from airtable import Airtable
import os
import json
from flask import current_app

class EarlyVotingLocations():
  def __init__(self, county):
    self.locations = None

    # disabled w/o this env var set
    if not os.getenv('AIRTABLE_EV_TABLE'):
      return

    self.county = county

    # look first in redis cache
    self.locations = self.get_cached_locations()
    #current_app.logger.info("redis locations for {}: {}".format(self.county, self.locations))

    # otherwise fetch and cache
    if not self.locations:
      self.locations = self.fetch_locations()


  def cache_key(self):
    return "ev-{}".format(self.county)

  def get_cached_locations(self):
    redis = KSVotesRedis()
    locations = redis.get(self.cache_key())
    if locations:
      return json.loads(locations)
    else:
      return None
    
  def fetch_locations(self):
    redis = KSVotesRedis()
    airtable = Airtable(os.getenv('AIRTABLE_EV_BASE_ID'), os.getenv('AIRTABLE_EV_TABLE'), os.getenv('AIRTABLE_EV_KEY'))
    response = airtable.get_all(formula="AND( COUNTY = '{}' )".format(self.county.upper()))

    # some counties do not have actual locations
    if 'LOCATION' not in response[0]['fields']:
      return

    redis.set(self.cache_key(), json.dumps(response).encode(), os.getenv('EVL_TTL', '3600'))
    return response

