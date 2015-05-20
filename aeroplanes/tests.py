from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.utils import timezone
from .models import Aeroplane

# Create your tests here.
class NextMaintIntervalTest(TestCase):

    def test_next_hour_based_check(self):
        """
        Next maintainence item has two results: time and hours based.
        Let's work on the hours-based one first.
        Given the current TTAF, last check type and last check hours, what's next?
        """

        # Arrange
        last_check_type = Aeroplane.CHECK_TYPE_50_HOURS_2
        flown_hours = 35
        last_check_ttaf = 2623.45

        # Act
        next_check = Aeroplane.calc_next_flying_hours_check(last_check_type, last_check_ttaf, flown_hours)

        # Assert
        self.assertEqual(next_check.check_type, Aeroplane.CHECK_TYPE_150_HOURS)
        self.assertEqual(next_check.check_in_flying_hours, 15)
        self.assertEqual(next_check.check_at_total_flying_hours, 2673.45)

    def test_next_calendar_based_check(self):
        # Arrange
        last_annual_check_at = timezone.datetime(2014, 7, 29)
        last_check_at = timezone.datetime(2015, 4, 8)

        # Act
        next_calendar_check = Aeroplane.calc_next_calendar_check(last_check_at, last_annual_check_at)

        # Assert
        self.assertEqual(next_calendar_check.check_before, timezone.datetime(2015, 7, 29))
        self.assertEqual(next_calendar_check.check_type, Aeroplane.CHECK_TYPE_ANNUAL)

    def test_next_check_pair_gbxex(self):
        # Arrange

        # Act
        check_pair = Aeroplane.calc_next_check_pair(
            timezone.datetime(2015, 4, 8),
            timezone.datetime(2014, 7, 29),
            Aeroplane.CHECK_TYPE_50_HOURS_2,
            2623.45,
            44
        )

        # Assert
        self.assertEqual(check_pair.flying_hours_check.check_type, Aeroplane.CHECK_TYPE_150_HOURS)
        self.assertEqual(check_pair.flying_hours_check.check_in_flying_hours, 6)
        self.assertEqual(check_pair.flying_hours_check.check_at_total_flying_hours, 2673.45)

        self.assertEqual(check_pair.calendar_check.check_before, timezone.datetime(2015, 7, 29))
        self.assertEqual(check_pair.calendar_check.check_type, Aeroplane.CHECK_TYPE_ANNUAL)

    def test_next_check_pair_2(self):
        # Arrange

        # Act
        check_pair = Aeroplane.calc_next_check_pair(
            timezone.datetime(1972, 10, 15),  # last check
            timezone.datetime(1972, 1, 1),  # last annual
            Aeroplane.CHECK_TYPE_150_HOURS,  # last check
            762,  # ttaf at last check
            27  # hours flown since
        )

        # Assert
        self.assertEqual(check_pair.flying_hours_check.check_type, Aeroplane.CHECK_TYPE_50_HOURS_1)
        self.assertEqual(check_pair.flying_hours_check.check_in_flying_hours, 23)
        self.assertEqual(check_pair.flying_hours_check.check_at_total_flying_hours, 812)

        self.assertEqual(check_pair.calendar_check.check_before, timezone.datetime(1973, 1, 1))
        self.assertEqual(check_pair.calendar_check.check_type, Aeroplane.CHECK_TYPE_ANNUAL)

    def test_next_check_pair_no_flying(self):
        # Arrange

        # Act
        check_pair = Aeroplane.calc_next_check_pair(
            timezone.datetime(2010, 1, 1),  # last check
            timezone.datetime(2010, 1, 1),  # last annual
            Aeroplane.CHECK_TYPE_ANNUAL,  # last check
            1000,  # ttaf at last check
            1  # hours flown since
        )

        # Assert
        self.assertEqual(check_pair.flying_hours_check.check_type, Aeroplane.CHECK_TYPE_50_HOURS_1)
        self.assertEqual(check_pair.flying_hours_check.check_in_flying_hours, 49)
        self.assertEqual(check_pair.flying_hours_check.check_at_total_flying_hours, 1050)

        self.assertEqual(check_pair.calendar_check.check_before, timezone.datetime(2010, 7, 1))
        self.assertEqual(check_pair.calendar_check.check_type, Aeroplane.CHECK_TYPE_50_HOURS_1)

    def test_next_check_pair_one_early_50h(self):
        # Arrange

        # Act
        check_pair = Aeroplane.calc_next_check_pair(
            timezone.datetime(2010, 2, 1),  # last check
            timezone.datetime(2010, 1, 1),  # last annual
            Aeroplane.CHECK_TYPE_50_HOURS_1,  # last check
            1000,  # ttaf at last check
            1  # hours flown since
        )

        # Assert
        self.assertEqual(check_pair.flying_hours_check.check_type, Aeroplane.CHECK_TYPE_50_HOURS_2)
        self.assertEqual(check_pair.flying_hours_check.check_in_flying_hours, 49)
        self.assertEqual(check_pair.flying_hours_check.check_at_total_flying_hours, 1050)

        self.assertEqual(check_pair.calendar_check.check_before, timezone.datetime(2010, 8, 1))
        self.assertEqual(check_pair.calendar_check.check_type, Aeroplane.CHECK_TYPE_50_HOURS_1)

    def test_next_check_pair_one_late_50h_then_nothing(self):
        # Arrange

        # Act
        check_pair = Aeroplane.calc_next_check_pair(
            timezone.datetime(2010, 7, 1),  # last check
            timezone.datetime(2010, 1, 1),  # last annual
            Aeroplane.CHECK_TYPE_50_HOURS_1,  # last check
            1000,  # ttaf at last check
            1  # hours flown since
        )

        # Assert
        self.assertEqual(check_pair.flying_hours_check.check_type, Aeroplane.CHECK_TYPE_50_HOURS_2)
        self.assertEqual(check_pair.flying_hours_check.check_in_flying_hours, 49)
        self.assertEqual(check_pair.flying_hours_check.check_at_total_flying_hours, 1050)

        self.assertEqual(check_pair.calendar_check.check_before, timezone.datetime(2011, 1, 1))
        self.assertEqual(check_pair.calendar_check.check_type, Aeroplane.CHECK_TYPE_ANNUAL)
