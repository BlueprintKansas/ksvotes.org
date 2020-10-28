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

  def vr_through_today(self, start_date):
    today = datetime.date.today()
    sql = """
      select cast(vr_completed_at at time zone 'utc' at time zone 'america/chicago' as date), count(id)
      from registrants
      where vr_completed_at is not null and vr_completed_at at time zone 'utc' at time zone 'america/chicago' between '{start_date}' and '{today}'
      group by cast(vr_completed_at at time zone 'utc' at time zone 'america/chicago' as date)
      order by 1
    """
    vr_stats = db.session.connection().execute(sql.format(start_date=start_date, today=today))

    return vr_stats.fetchall()

  def ab_through_today(self, start_date):
    today = datetime.date.today()
    sql = """
      select cast(ab_completed_at at time zone 'utc' at time zone 'america/chicago' as date), count(id)
      from registrants
      where ab_completed_at is not null and ab_completed_at at time zone 'utc' at time zone 'america/chicago' between '{start_date}' and '{today}'
      group by cast(ab_completed_at at time zone 'utc' at time zone 'america/chicago' as date)
      order by 1
    """
    ab_stats = db.session.connection().execute(sql.format(start_date=start_date, today=today))

    return ab_stats.fetchall()
