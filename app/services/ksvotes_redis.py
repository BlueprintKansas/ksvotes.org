from flask_redis import FlaskRedis
from flask import current_app
from redis import WatchError

class KSVotesRedis():
  def __init__(self):
    self.redis_client = FlaskRedis(current_app)

  def get_or_set(self, key, setter):
    with self.redis_client.pipeline() as pipe:
      try:
        pipe.watch(key)
        # after WATCHing, the pipeline is put into immediate execution
        # mode until we tell it to start buffering commands again.
        # this allows us to get the current value of our sequence
        if pipe.exists(key):
          return pipe.get(key)
        # now we can put the pipeline back into buffered mode with MULTI
        pipe.multi()
        pipe.set(key, setter())
        pipe.get(key)
        # and finally, execute the pipeline (the set and get commands)
        return pipe.execute()[-1]
        # if a WatchError wasn't raised during execution, everything
        # we just did happened atomically.
      except WatchError:
        # another client must have changed key between
        # the time we started WATCHing it and the pipeline's execution.
        # Let's just get the value they changed it to.
        return pipe.get(key)
