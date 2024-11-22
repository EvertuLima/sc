from django.core.exceptions import ValidationError  # type: ignore
from parameterized import parameterized  # type: ignore

from .test_room_base import RoomTestBase


class RoomComponentTest(RoomTestBase):
    def setUp(self) -> None:
        self.component = self.make_component()
        return super().setUp()

    @parameterized.expand([
        ('inventory_number', 65),
        ('description', 254),
        ('brand', 65),
        ('model', 65),
        ('condition', 65),
        ('notes', 65),
    ])
    def test_component_fields_max_length(self, field, max_length):
        setattr(self.component, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.component.full_clean()

    def test_component_string_representation(self):
        self.assertEqual(
            str(self.component),
            self.component.description
        )

    def test_relationship_between_component_model_and_room_model(self):
        new_local = self.make_room(name='New Room', responsible_data={
            'username': 'New Responsible'
        })
        self.component.location = new_local
        self.assertEqual(self.component.location.name, new_local.name)
