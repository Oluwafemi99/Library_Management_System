from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Books
from datetime import date


LibraryUser = get_user_model()


class LibraryUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = LibraryUser
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'Date_of_Membership', 'Active_Status', 'books_checked_out']

    def create(self, validated_data):
        # Extract the password from validated_data
        password = validated_data.pop('password')

        # Create the user with the remaining data
        user = LibraryUser.objects.create(**validated_data)
        user.set_password(password)  # Set the password securely
        user.save()

        return user


class BooksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Books
        fields = ['id', 'Title', 'Author', 'ISBN', 'Published_Date', 'Number_of_Copies_Available']

    def validate(self, data):
        Published_Date = data.get('Published_Date')
        if Published_Date.year > date.today().year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return data
