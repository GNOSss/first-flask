from flask import url_for, Flask
import os
from datetime import date, datetime




def make_date(dt, fmt):
    if not isinstance(dt, date):
        return datetime.strptime(dt, fmt)
    else:
        return dt
