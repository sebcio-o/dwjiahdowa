from app.users.models import CustomUser
from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name"]
        read_only_fields = ["email"]
