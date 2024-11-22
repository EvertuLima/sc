from parameterized import parameterized  # type: ignore

from room.serializers import ComponentSerializer
from room.tests.test_room_base import RoomTestBase


class ComponentSerializerTest(RoomTestBase):
    def setUp(self) -> None:
        self.component_data = {
            'id': 1,
            'inventory_number': 'register',
            'description': 'description',
            'brand': 'brand',
            'model': 'model',
            'condition': 'condition',
            'notes': 'notes',
            'location': 1
        }
        self.component = self.make_component()
        self.serializer = ComponentSerializer(instance=self.component)
        return super().setUp()

    def test_serializers_component_contain_expected_fields(self):
        self.assertEqual(
            list(self.serializer.data.keys()),
            list(self.component_data.keys())
        )

    @parameterized.expand([
        'id',
        'inventory_number',
        'description',
        'brand',
        'model',
        'condition',
        'notes',
        'location'
    ])
    def test_serializers_component_field_content(self, keys):
        data = self.serializer.data
        self.assertEqual(data[keys], self.component_data[keys])

    def test_serializer_component_create_is_valid(self):
        valid_data = {
            'id': 1,
            'inventory_number': 'register',
            'description': 'description',
            'brand': 'brand',
            'model': 'model',
            'condition': 'condition',
            'notes': 'notes',
            'location': 1
        }
        serializer = ComponentSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())