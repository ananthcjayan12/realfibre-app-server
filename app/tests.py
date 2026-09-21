import json
from pathlib import Path

from django.contrib.auth.models import User
from django.test import SimpleTestCase, TestCase
from django.utils import timezone

from .catalog_config import (
    DEFAULT_COLOUR_BY_MODEL,
    calculate_frame_measurements,
)
from .forms import FinishForm
from .models import Customer, Door, DoorBatch, DoorModel


class CatalogueConfigTests(SimpleTestCase):
    def test_confirmed_default_colours(self):
        self.assertEqual(DEFAULT_COLOUR_BY_MODEL["lyka"], "beigegrey")
        self.assertEqual(DEFAULT_COLOUR_BY_MODEL["electra"], "olivegreen")
        self.assertEqual(DEFAULT_COLOUR_BY_MODEL["kenz"], "goldenbrown")
        self.assertEqual(DEFAULT_COLOUR_BY_MODEL["willo"], "coffeebrown")
        self.assertEqual(DEFAULT_COLOUR_BY_MODEL["stripes"], "chocolatebrown")
        self.assertEqual(DEFAULT_COLOUR_BY_MODEL["grace"], "beige")
        self.assertEqual(DEFAULT_COLOUR_BY_MODEL["olive"], "oakwood")
        self.assertNotIn("plain", DEFAULT_COLOUR_BY_MODEL)
        self.assertNotIn("recta", DEFAULT_COLOUR_BY_MODEL)

    def test_new_frame_clearances_keep_existing_height_adjustment(self):
        self.assertEqual(
            calculate_frame_measurements("Small", 100, 100, 210),
            (92.9, 92.9, 205.7),
        )
        self.assertEqual(
            calculate_frame_measurements("Normal", 100, 100, 210),
            (92.0, 92.0, 205.2),
        )
        self.assertEqual(
            calculate_frame_measurements("Medium", 100, 100, 210),
            (93.0, 93.0, 205.7),
        )
        self.assertEqual(
            calculate_frame_measurements("Heavy", 100, 100, 210),
            (89.6, 89.6, 203.7),
        )

    def test_finish_options_preserve_historical_values(self):
        values = [value for value, _label in FinishForm.FINISH_CHOICES]
        self.assertIn("std", values)
        self.assertIn("std_grains", values)
        self.assertIn("natural_wood", values)
        self.assertIn("glossy", values)

    def test_mould_capacities_match_client_confirmation(self):
        mould_path = Path(__file__).resolve().parent.parent / "mould_data.json"
        moulds = json.loads(mould_path.read_text())
        expected = {
            "plain": 8,
            "lyka": 1,
            "electra": 2,
            "kenz": 2,
            "willo": 1,
            "stripes": 1,
            "grace": 1,
            "olive": 2,
            "recta": 3,
        }
        for model, capacity in expected.items():
            self.assertEqual(moulds[model], capacity)


class DoorBatchCapacityTests(TestCase):
    def setUp(self):
        self.agent = User.objects.create_user(username="batch-agent", password="test")
        self.customer = Customer.objects.create(
            agent=self.agent,
            name="Batch Test",
            location="Test",
            phone_number="0000000000",
            delivery_date=timezone.now().date(),
            order_date=timezone.now().date(),
            form_complete=True,
        )

    def make_door(self, model_name):
        door = Door.objects.create(customer=self.customer)
        model = DoorModel.objects.create(door=door, model_name=model_name)
        door.model_selection = model
        door.save()
        return door

    def test_daily_batch_respects_new_mould_capacity(self):
        plain_doors = [self.make_door("plain") for _ in range(9)]
        lyka_doors = [self.make_door("lyka") for _ in range(2)]
        recta_doors = [self.make_door("recta") for _ in range(4)]

        batch = DoorBatch.create_batch_for_today()

        self.assertEqual(
            batch.doors.filter(model_selection__model_name="plain").count(), 8
        )
        self.assertEqual(
            batch.doors.filter(model_selection__model_name="lyka").count(), 1
        )
        self.assertEqual(
            batch.doors.filter(model_selection__model_name="recta").count(), 3
        )

        selected_ids = set(batch.doors.values_list("id", flat=True))
        self.assertEqual(len([d for d in plain_doors if d.id not in selected_ids]), 1)
        self.assertEqual(len([d for d in lyka_doors if d.id not in selected_ids]), 1)
        self.assertEqual(len([d for d in recta_doors if d.id not in selected_ids]), 1)
