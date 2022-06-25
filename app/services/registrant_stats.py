from app.models import Registrant
from app import db
import datetime
from sqlalchemy import func

class RegistrantStats():
  def vr_total_processed(self):
    r = db.session.query(func.count(Registrant.id)).filter(Registrant.vr_completed_at.isnot(None)).first()
    return r[0]

  def ab_total_processed(self):
    r = db.session.query(func.count(Registrant.id)).filter(Registrant.ab_completed_at.isnot(None)).first()
    return r[0]

  def vr_through_today(self, start_date, end_date=None):
    today = datetime.date.today() + datetime.timedelta(days=1)
    if not end_date:
        end_date = today
    sql = """
      select cast(vr_completed_at at time zone 'utc' at time zone 'america/chicago' as date) as vr_date, count(id)
      from registrants
      where vr_completed_at is not null and vr_completed_at at time zone 'utc' at time zone 'america/chicago' between '{start_date}' and '{end_date}'
      group by vr_date
      order by 1
    """
    vr_stats = db.session.connection().execute(sql.format(start_date=start_date, end_date=end_date))

    return vr_stats.fetchall()

  def ab_through_today(self, start_date, end_date=None):
    today = datetime.date.today() + datetime.timedelta(days=1)
    if not end_date:
        end_date = today
    sql = """
      select cast(ab_completed_at at time zone 'utc' at time zone 'america/chicago' as date) as ab_date, count(id)
      from registrants
      where ab_completed_at is not null and ab_completed_at at time zone 'utc' at time zone 'america/chicago' between '{start_date}' and '{end_date}'
      group by ab_date
      order by 1
    """
    ab_stats = db.session.connection().execute(sql.format(start_date=start_date, end_date=end_date))

    return ab_stats.fetchall()
