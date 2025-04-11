from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Books, LibraryUser
from .serializers import BooksSerializer, LibraryUserSerializer
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
class UserCreateView(generics.CreateAPIView):
    queryset = LibraryUser.objects.all()
    serializer_class = LibraryUserSerializer
    permission_classes = [permissions.AllowAny]


class UserDetailsView(generics.RetrieveAPIView):
    serializer_class = LibraryUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Restrict the queryset to the authenticated user's libraryuser object
        return LibraryUser.objects.filter(pk=self.request.pk)


class UserListView(generics.ListAPIView):
    serializer_class = LibraryUserSerializer
    queryset = LibraryUser.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = LibraryUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LibraryUser.objects.filter(pk=self.request.user.pk)

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class UserDeleteView(generics.DestroyAPIView):
    serializer_class = LibraryUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return LibraryUser.objects.filter(pk=self.request.user.pk)


class BookCreateView(generics.CreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = (permissions.IsAdminUser)


class BookListView(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookUpdateView(generics.UpdateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDeleteView(generics.DestroyAPIView):
    serializer_class = BooksSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Books.objects.all()
