from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer  # type: ignore
from django.contrib.auth.models import User  # type: ignore
from rest_framework import permissions  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.decorators import action  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.views import APIView  # type: ignore
from rest_framework.viewsets import ModelViewSet  # type: ignore

from room.models import Component, Room
from room.serializers import (
    ComponentSerializer,
    CustomPagination,
    RoomSerializer,
    UserCreateSerializer,
    UserRegisterSerializer,
    UserSerializer,
)


class user_API_ViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [permissions.AllowAny]
        elif self.action in ["update", "partial_update", "retrieve"]:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == "me":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_success_headers(self, data):
        # Construa o cabeçalho Location com a URL completa do novo usuário criado
        try:
            return {"Location": f"{self.request.build_absolute_uri()}{data['id']}/"}
        except (TypeError, KeyError):
            return {}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "user": UserSerializer(user).data,
                "message": "Usuário criado com sucesso!",
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(
        detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request):
        """Retorna os dados do usuário autenticado."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class room_API_ViewSet(ModelViewSet):
    queryset = Room.objects.all()  # pylint: disable=no-member
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    # pagination_class = CustomPagination
    channel_layer = get_channel_layer()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        async_to_sync(self.channel_layer.group_send)(
            "rooms_group",
            {
                "type": "send_rooms_updated",
            },
        )
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        async_to_sync(self.channel_layer.group_send)(
            "rooms_group",
            {
                "type": "send_rooms_updated",
            },
        )
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)

        async_to_sync(self.channel_layer.group_send)(
            "rooms_group",
            {
                "type": "send_rooms_updated",
            },
        )
        return response


class component_API_ViewSet(ModelViewSet):
    queryset = Component.objects.all()  # pylint: disable=no-member
    serializer_class = ComponentSerializer
    permission_classes = [permissions.IsAuthenticated]
    channel_layer = get_channel_layer()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        async_to_sync(self.channel_layer.group_send)(
            "components_group",
            {
                "type": "send_components_updated",
            },
        )

        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)

        async_to_sync(self.channel_layer.group_send)(
            "components_group",
            {
                "type": "send_components_updated",
            },
        )

        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)

        async_to_sync(self.channel_layer.group_send)(
            "components_group",
            {
                "type": "send_components_updated",
            },
        )

        return response


class UserView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
