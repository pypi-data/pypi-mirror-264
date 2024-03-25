"""
This file contains the context processors for views
More info: https://flask.palletsprojects.com/en/3.0.x/templating/#context-processors
"""

import datetime
import humanize

def utility_processor():
    """
    This function returns a dictionary of utility functions that
    can be used in templates
    """
    def format_time(time):
        # format time as HH:MM:SS
        return time.replace('-', ':')

    def format_date(date):
        # read date as YYYY-MM-DD
        date = datetime.datetime.strptime(date, '%Y-%m-%d')

        # format date as natural language
        return humanize.naturaldate(date)

    def format_duration(duration):
        if duration is None:
            return "N/A"

        # format duration as n seconds, n minutes, n hours, n days, etc.
        return humanize.precisedelta(datetime.timedelta(seconds=duration))

    return dict(
            format_time=format_time,
            format_duration=format_duration,
            format_date=format_date
        )
