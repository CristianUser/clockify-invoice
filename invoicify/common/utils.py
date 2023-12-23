
from dateutil.relativedelta import relativedelta
from datetime import datetime, time


def add_n_months_to_date(date, n):
    return date + relativedelta(months=n)


def parse_date(date_string):
    return datetime.strptime(date_string, "%d-%m-%Y")


def parse_end_date(date_string):
    return datetime.combine(parse_date(date_string), time.max)


def format_date(date):
    return date.strftime("%d/%m/%Y")


def seconds_to_hours(seconds):
    return seconds / 3600
