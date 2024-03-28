import unittest

from looqbox.objects.response_parameters.temporal_granularity import TemporalGranularity


class TestTemporalGranularity(unittest.TestCase):

    def test_DAYS_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'DAYS'))

    def test_DAY_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'DAY'))

    def test_HOURS_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'HOURS'))

    def test_HOUR_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'HOUR'))

    def test_WEEKS_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'WEEKS'))

    def test_WEEK_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'WEEK'))

    def test_MINUTES_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'MINUTES'))

    def test_MINUTE_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'MINUTE'))

    def test_SECONDS_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'SECONDS'))

    def test_SECOND_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'SECOND'))

    def test_MONTHS_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'MONTHS'))

    def test_MONTH_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'MONTH'))

    def test_YEARS_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'YEARS'))

    def test_YEAR_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'YEAR'))

    def test_DECADES_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'DECADES'))

    def test_DECADE_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'DECADE'))

    def test_CENTURIES_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'CENTURIES'))

    def test_CENTURY_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'CENTURY'))

    def test_MILLENNIA_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'MILLENNIA'))

    def test_MILLENNIUM_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'MILLENNIUM'))

    def test_BIMESTER_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'BIMESTER'))

    def test_TRIMESTER_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'TRIMESTER'))

    def test_QUARTER_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'QUARTER'))

    def test_SEMESTER_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'SEMESTER'))

    def test_YEAR_DAY_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'YEAR_DAY'))

    def test_MONTH_DAY_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'MONTH_DAY'))

    def test_MONTH_YEAR_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'MONTH_YEAR'))

    def test_WEEK_DAY_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'WEEK_DAY'))

    def test_WEEK_YEAR_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'WEEK_YEAR'))

    def test_WEEK_MONTH_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'WEEK_MONTH'))

    def test_DAY_HOURS_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'DAY_HOURS'))

    def test_DAY_MINUTES_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'DAY_MINUTES'))

    def test_HOUR_MINUTES_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'HOUR_MINUTES'))

    def test_HOUR_SECONDS_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'HOUR_SECONDS'))

    def test_DAY_SECONDS_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'DAY_SECONDS'))

    def test_MINUTE_SECONDS_exists(self):
        self.assertTrue(hasattr(TemporalGranularity, 'MINUTE_SECONDS'))


if __name__ == '__main__':
    unittest.main()
