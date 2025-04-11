from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Books
from datetime import date


LibraryUser = get_user_model()


class LibraryUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        models = LibraryUser
        fields = '__all__'

    def create(self, validated_data):
        # Create the user with the provided data
        user = get_user_model().objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password'),
        )
        return user


class BooksSerializer(serializers.ModelSerializer):

    class Meta:
        models = Books
        feilds = '__all__'

    def validate(self, data):
        Published_Date = data.get('Published_Date')
        if Published_Date > date.today().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return Published_Date
