from parameterized import parameterized  # type: ignore

from room.serializers import RoomSerializer
from room.tests.test_room_base import RoomTestBase


class RoomSerializerTest(RoomTestBase):
    def setUp(self) -> None:
        self.room_data = {
            'id': 1,
            'name': 'room_name',
            'description': 'description',
            'notes': 'notes',
            'responsible': 1
        }
        self.room = self.make_room()
        self.serializer = RoomSerializer(instance=self.room)
        return super().setUp()

    def test_serializer_room_contain_expected_fields(self):
        self.assertEqual(
            list(self.serializer.data.keys()),
            list(self.room_data.keys())
        )

    @parameterized.expand([
        'id',
        'name',
        'description',
        'notes',
        'responsible',
    ])
    def test_serializer_room_field_content(self, keys):
        data = self.serializer.data
        self.assertEqual(data[keys], self.room_data[keys])

    def test_serializer_room_create_is_valid(self):
        valid_data = {
            'name': 'New Room',
            'description': 'Description',
            'notes': 'Nothing',
            'responsible': 1
        }
        serializer = RoomSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
