# -*- coding: utf-8 -*-

from calendar import monthrange
from datetime import datetime, timedelta
from unittest import TestCase

from core_datetime.utils import FrequencyType
from core_datetime.utils import get_time_windows
from core_datetime.utils import utc_datetime_to_epoch


class TimeUtilsTestCases(TestCase):
    """ Test cases for utils related to datetime """

    def test_get_list_time_windows_hour(self):
        start = (datetime.utcnow() - timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
        res = get_time_windows(start)
        self.assertEqual(list(res)[0], (start, datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")))

        now = datetime.utcnow()
        start = (datetime.utcnow() - timedelta(hours=5)).strftime("%Y-%m-%dT%H:%M:%S")
        res = get_time_windows(start, frequency=FrequencyType.HOUR)

        self.assertEqual(list(res), [
            (
                (now - timedelta(hours=5)).strftime("%Y-%m-%dT%H:00:00"),
                (now - timedelta(hours=5)).strftime("%Y-%m-%dT%H:59:59")
            ),
            (
                (now - timedelta(hours=4)).strftime("%Y-%m-%dT%H:00:00"),
                (now - timedelta(hours=4)).strftime("%Y-%m-%dT%H:59:59")
            ),
            (
                (now - timedelta(hours=3)).strftime("%Y-%m-%dT%H:00:00"),
                (now - timedelta(hours=3)).strftime("%Y-%m-%dT%H:59:59")
            ),
            (
                (now - timedelta(hours=2)).strftime("%Y-%m-%dT%H:00:00"),
                (now - timedelta(hours=2)).strftime("%Y-%m-%dT%H:59:59")
            ),
            (
                (now - timedelta(hours=1)).strftime("%Y-%m-%dT%H:00:00"),
                (now - timedelta(hours=1)).strftime("%Y-%m-%dT%H:59:59")
            )
        ])

    def test_get_list_time_windows_day(self):
        now = datetime.utcnow()
        start = (datetime.utcnow() - timedelta(days=3)).strftime("%Y-%m-%dT00:00:00")
        res = get_time_windows(start, frequency=FrequencyType.DAY)

        self.assertEqual(list(res), [
            (
                (now - timedelta(days=3)).strftime("%Y-%m-%dT00:00:00"),
                (now - timedelta(days=3)).strftime("%Y-%m-%dT23:59:59")
            ),
            (
                (now - timedelta(days=2)).strftime("%Y-%m-%dT00:00:00"),
                (now - timedelta(days=2)).strftime("%Y-%m-%dT23:59:59")
            ),
            (
                (now - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00"),
                (now - timedelta(days=1)).strftime("%Y-%m-%dT23:59:59")
            )
        ])

    def test_get_list_time_windows_month(self):
        current_month = datetime.utcnow().replace(day=1)
        previous_month_one = (current_month - timedelta(days=3)).replace(day=1)
        previous_month_two = (previous_month_one - timedelta(days=3)).replace(day=1)
        start_date = (previous_month_two - timedelta(days=3)).replace(day=1)

        res = get_time_windows(
            start_date.replace(day=1).strftime("%Y-%m-%d"),
            frequency=FrequencyType.MONTH)

        self.assertEqual(list(res), [
            (
                start_date.strftime("%Y-%m-%dT00:00:00"),
                start_date \
                    .replace(day=monthrange(start_date.year, start_date.month)[1]) \
                    .strftime("%Y-%m-%dT23:59:59")
            ),
            (
                previous_month_two.strftime("%Y-%m-%dT00:00:00"),
                previous_month_two \
                    .replace(day=monthrange(previous_month_two.year, previous_month_two.month)[1]) \
                    .strftime("%Y-%m-%dT23:59:59")
            ),
            (
                previous_month_one.strftime("%Y-%m-%dT00:00:00"),
                previous_month_one \
                    .replace(day=monthrange(previous_month_one.year, previous_month_one.month)[1]) \
                    .strftime("%Y-%m-%dT23:59:59")
            )
        ])

    def test_get_list_time_windows_month_with_end(self):
        res = get_time_windows(
            start="2022-03-01T00:00:00",
            end="2022-06-10T00:00:00",
            frequency=FrequencyType.MONTH)

        self.assertEqual(list(res), [
            ("2022-03-01T00:00:00", "2022-03-31T23:59:59"),
            ("2022-04-01T00:00:00", "2022-04-30T23:59:59"),
            ("2022-05-01T00:00:00", "2022-05-31T23:59:59")
        ])

    def test_utc_time_to_epoch(self):
        res = utc_datetime_to_epoch(datetime(year=1970, month=1, day=1))
        self.assertEqual(res, 0)
