from django.test import TestCase
from .models import ResidentActivity
from homes.factories import HomeFactory
from residents.factories import ResidentFactory, ResidencyFactory
from datetime import datetime
from django.urls import reverse
from activities.model import Activity


class ResidentActivityTestCase(TestCase):
    def setUp(self):
        # Create test data using factories
        self.home1 = HomeFactory(name="Home 1")
        self.resident1 = ResidentFactory(first_name="Alice")
        self.resident2 = ResidentFactory(first_name="Bob")
        self.residency1 = ResidencyFactory(
            home=self.home1,
            resident=self.resident1,
            move_out=None,
        )
        self.residency2 = ResidencyFactory(
            home=self.home1,
            resident=self.resident2,
            move_out=None,
        )

    def test_initial_resident_activity(self):
        """Initially no resident activity."""
        initial_resident_activity = ResidentActivity.objects.filter(
            home=self.home1,
        ).count()
        self.assertEqual(initial_resident_activity, 0)

    def test_add_activity_adds_resident_activity(self):
        """When activity is added, resident activity is added."""
        self.data = {
            "residents": self.resident1,
            "activity_type": "outdoor",
            "date": datetime.now(),
            "duration_minutes": 30,
            "caregiver_role": "staff",
        }
        response = self.client.post(
            reverse("activity-form-view"),
            self.data,
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.code, 200)
        self.assertEqual(Activity.objects.all.count(), 1)
        self.assertEqual(ResidentActivity.objects.all.count(), 1)

    def test_add_invalid_activity_rollback(self):
        """When invalid activity is added, rollback entire transaction."""
        # Resident0 does not exist
        self.data = {
            "residents": self.resident0,
            "activity_type": "outdoor",
            "date": datetime.now(),
            "duration_minutes": 30,
            "caregiver_role": "staff",
        }
        response = self.client.post(
            reverse("activity-form-view"),
            self.data,
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.code, 400)
        self.assertEqual(Activity.objects.all.count(), 0)
        self.assertEqual(ResidentActivity.objects.all.count(), 0)

    def test_add_invalid_resident_activity_rollback(self):
        """When invalid resident_activity is added, rollback entire
        transaction."""
        # Resident3 does not have residency so can't be added to resident_activity
        # table and activity insertion should be rolled back
        self.resident3 = ResidentFactory(first_name="Henry")
        self.data = {
            "residents": self.resident3,
            "activity_type": "outdoor",
            "date": datetime.now(),
            "duration_minutes": 30,
            "caregiver_role": "staff",
        }
        response = self.client.post(
            reverse("activity-form-view"),
            self.data,
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.code, 400)
        self.assertEqual(Activity.objects.all.count(), 0)
        self.assertEqual(ResidentActivity.objects.all.count(), 0)
