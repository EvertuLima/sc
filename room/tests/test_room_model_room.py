from django.core.exceptions import ValidationError  # type: ignore
from parameterized import parameterized  # type: ignore

from room.tests.test_room_base import RoomTestBase


class RoomModelTest(RoomTestBase):
    def setUp(self) -> None:
        self.room = self.make_room(name='Room Testing')
        return super().setUp()

    @parameterized.expand([
        ('name', 65),
        ('description', 254),
        ('notes', 65),
    ])
    def test_room_fields_max_length(self, field, max_length):
        setattr(self.room, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.room.full_clean()

    def test_room_string_representation(self):
        self.assertEqual(
            str(self.room),
            self.room.name
        )

    def test_relationship_between_room_model_and_user_model(self):
        responsible = self.make_responsible(username='Responsible')
        self.room.responsible = responsible
        self.assertEqual(responsible.username, self.room.responsible.username)
