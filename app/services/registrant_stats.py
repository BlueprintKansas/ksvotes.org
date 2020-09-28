from app.models import Registrant
from app import db
import datetime

class RegistrantStats():
  def vr_through_today(self, start_date):
    today = datetime.date.today()
    sql = """
      select cast(vr_completed_at as date), count(id)
      from registrants
      where vr_completed_at is not null and vr_completed_at between '{start_date}' and '{today}'
      group by cast(vr_completed_at as date)
      order by 1
    """
    vr_stats = db.session.connection().execute(sql.format(start_date=start_date, today=today))

    return vr_stats.fetchall()

  def ab_through_today(self, start_date):
    today = datetime.date.today()
    sql = """
      select cast(ab_completed_at as date), count(id)
      from registrants
      where ab_completed_at is not null and ab_completed_at between '{start_date}' and '{today}'
      group by cast(ab_completed_at as date)
      order by 1
    """
    ab_stats = db.session.connection().execute(sql.format(start_date=start_date, today=today))

    return ab_stats.fetchall()
