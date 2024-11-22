from django.test import TestCase  # type: ignore

from room.models import Component, Room, User


class RoomTestBase(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    component_raw_data = {
        'id': 1,
        'inventory_number': 'register',
        'description': 'description - 0',
        'brand': 'brand',
        'model': 'model',
        'condition': 'condition',
        'notes': 'notes',
        'location': 1
    }

    def make_responsible(
        self,
        first_name='user',
        last_name='name',
        username='username',
        email='username@email.com',
        password='12345678',
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )

    def make_room(
        self,
        name='room_name',
        description='description',
        notes='notes',
        responsible_data=None,
    ):
        if responsible_data is None:
            responsible_data = {}

        return Room.objects.create(  # pylint: disable=no-member
            name=name,
            description=description,
            notes=notes,
            responsible=self.make_responsible(**responsible_data),
        )

    def make_component(
        self,
        inventory_number='register',
        description='description',
        brand='brand',
        model='model',
        condition='condition',
        notes='notes',
        location_data=None,
    ):
        if location_data is None:
            location_data = {}

        return Component.objects.create(  # pylint: disable=no-member
            inventory_number=inventory_number,
            description=description,
            brand=brand,
            model=model,
            condition=condition,
            notes=notes,
            location=self.make_room(**location_data),
        )

    def make_several_rooms(self, qtd=10):
        rooms = []
        for i in range(qtd):
            room = self.make_room(
                name=f'New Room - {i}',
                responsible_data={
                    'username': f'New Responsible - {i}'
                }
            )
            rooms.append(room)
        return rooms

    def make_several_components(self, qtd=10):
        components = []
        for i in range(qtd):
            component = self.make_component(
                description=f'description - {i}',
                location_data={
                    'name': f'New Room - {i}',
                    'responsible_data': {
                        'username': f'New Responsible - {i}'
                    }
                }
            )
            components.append(component)
        return components

    def make_several_components_for_a_room(self, qtd=10):
        room = self.make_room()
        components = []

        for i in range(qtd):
            component = self.make_component(
                description=f'description - {i}',
                location_data={
                    'name': f'New Room - {i+1}',
                    'responsible_data': {
                        'username': f'New Responsible - {i+1}'
                    }
                }
            )
            component.location = room
            component.save()
            components.append(component)

        return components
