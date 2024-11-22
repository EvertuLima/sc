from django.urls import reverse  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.test import APITestCase  # type: ignore

from room.tests.test_room_base import RoomTestBase


class RoomViewRoomTest(APITestCase, RoomTestBase):
    def test_view_room_method_get_list(self):
        wanted_number_of_rooms = 3
        self.make_several_rooms(qtd=wanted_number_of_rooms)

        response = self.client.get(reverse('rooms:room-api-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        qtd_of_loaded_rooms = len(response.data)
        self.assertEqual(
            qtd_of_loaded_rooms,
            wanted_number_of_rooms
        )

    def test_view_room_method_get_detail_by_fields(self):
        room_raw_data = {
            'id': 1, 'name': 'New Room - 0', 'description': 'description',
            'notes': 'notes', 'responsible': 1
        }
        wanted_number_of_rooms = 1
        self.make_several_rooms(qtd=wanted_number_of_rooms)

        response = self.client.get(reverse('rooms:room-api-detail', args=(1,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, room_raw_data)

    def test_view_room_method_post(self):
        self.make_responsible()
        room_raw_data = {
            'name': 'New Room - 0', 'description': 'description',
            'notes': 'notes', 'responsible': 1
        }

        response = self.client.post(
            reverse('rooms:room-api-list'),
            data=room_raw_data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_room_method_patch(self):
        self.make_room()
        wanted_new_name = 'New Name For Room'

        response = self.client.patch(
            reverse('rooms:room-api-detail', args=(1,)),
            data={'name': wanted_new_name}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get('name'),
            wanted_new_name
        )

    def test_view_room_method_delete(self):
        self.make_room()

        response = self.client.delete(
            reverse('rooms:room-api-detail', args=(1, ))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
