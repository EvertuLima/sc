from django.contrib.auth.models import User  # type: ignore
from django.contrib.auth.password_validation import validate_password  # type: ignore
from rest_framework import serializers  # type: ignore
from rest_framework.pagination import PageNumberPagination  # type: ignore
from rest_framework.validators import UniqueValidator  # type: ignore

from room.models import Component, Room


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "password",
            "password_confirm",
            "email",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "username": {"validators": [UniqueValidator(queryset=User.objects.all())]},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password": "As senhas não correspondem."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para operações de leitura e atualização de usuários.
    Não inclui campos sensíveis como senha.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    full_name = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "is_active",
            "is_staff",
            "date_joined",
            "last_login",
        )
        extra_kwargs = {
            "username": {
                "validators": [UniqueValidator(queryset=User.objects.all())],
                "read_only": True,  # Previne alteração do username após criação
            },
            "is_staff": {
                "read_only": True
            },  # Apenas admin pode alterar via admin interface
        }

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def update(self, instance, validated_data):
        """
        Sobrescreve o método update para garantir que campos sensíveis
        não sejam alterados inadvertidamente
        """
        # Remove campos que não devem ser atualizados via API
        validated_data.pop("is_staff", None)
        validated_data.pop("is_active", None)

        # Atualiza os campos permitidos
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        instance.save()
        return instance


class RoomSerializer(serializers.ModelSerializer):
    responsible_details = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "description",
            "notes",
            "responsible",
            "responsible_details",
        ]

    def get_responsible_details(self, obj):
        if obj.responsible:
            return {
                "id": obj.responsible.id,
                "first_name": obj.responsible.first_name,
                "last_name": obj.responsible.last_name,
                "email": obj.responsible.email,
            }
        return None


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = [
            "id",
            "inventory_number",
            "description",
            "brand",
            "model",
            "condition",
            "notes",
            "location",
            "location_name",
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            email=validated_data["email"],
            password=validated_data[
                "password"
            ],  # Faz o hashing da senha automaticamente
        )
        return user
