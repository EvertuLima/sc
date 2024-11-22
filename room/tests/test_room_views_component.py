from django.urls import reverse  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.test import APITestCase  # type: ignore

from room.tests.test_room_base import RoomTestBase


class RoomViewComponentTest(APITestCase, RoomTestBase):
    def test_view_component_method_get_list(self):
        wanted_number_of_components = 4
        self.make_several_components(qtd=wanted_number_of_components)

        response = self.client.get(reverse('rooms:component-api-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        qtd_of_loaded_components = len(response.data)
        self.assertEqual(
            qtd_of_loaded_components,
            wanted_number_of_components
        )

    def test_view_component_method_get_detail_by_fields(self):
        wanted_number_of_components = 1
        self.make_several_components(qtd=wanted_number_of_components)

        response = self.client.get(
            reverse('rooms:component-api-detail', args=(1, ))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.component_raw_data)

    def test_view_component_method_post(self):
        self.make_room()

        response = self.client.post(
            reverse('rooms:component-api-list'),
            data=self.component_raw_data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_component_method_patch(self):
        self.make_component()
        wanted_new_descrition = 'New Description'

        response = self.client.patch(
            reverse('rooms:component-api-detail', args=(1, )),
            data={'description': wanted_new_descrition}
        )

        self.assertEqual(
            response.data.get('description'),
            wanted_new_descrition
        )

    def test_view_component_method_delete(self):
        self.make_component()

        response = self.client.delete(
            reverse('rooms:component-api-detail', args=(1, ))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_view_component_method_get_components_filter_by_location(self):
        wanted_number_of_components = 1
        self.make_several_components_for_a_room(
            qtd=wanted_number_of_components
        )

        url = reverse('rooms:component-api-list') + '?location=1'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), wanted_number_of_components)
