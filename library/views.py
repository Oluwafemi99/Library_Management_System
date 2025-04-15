from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Books, LibraryUser, Transaction
from .serializers import BooksSerializer, LibraryUserSerializer
from rest_framework.response import Response
from rest_framework import status
from datetime import date


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
    permission_classes = [permissions.IsAdminUser]


class BookListView(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookDeleteView(generics.DestroyAPIView):
    serializer_class = BooksSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Books.objects.all()


class BookCheckOutView(generics.UpdateAPIView):
    queryset = Books.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BooksSerializer

    def update(self, request, *args, **kwargs):
        book = self.get_object()
        user = request.user

    # Check if there are available copies
        if book.Number_of_Copies_Available <= 0:
            return Response({"error": "No copies of this book are available for checkout."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the user has already checked out this book
        if Transaction.objects.filter(user=user, book=book, return_date__isnull=True).exists():
            return Response({"error": "You have already checked out this book."}, status=status.HTTP_400_BAD_REQUEST)

    # Reduce the number of available copies
        book.Number_of_Copies_Available -= 1
        book.save()

    # Log the checkout transaction
        Transaction.objects.create(user=user, book=book)
        return Response({"message": "Book checked out successfully."}, status=status.HTTP_200_OK)


class BookReturnView(generics.UpdateAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        book = self.get_object()
        user = request.user

    # Check if the user has checked out this book
        transaction = Transaction.objects.filter(user=user, book=book, return_date__isnull=True).first()
        if not transaction:
            return Response({"error": "You have not checked out this book."}, status=status.HTTP_400_BAD_REQUEST)

    # increase the no of books
        book.Number_of_Copies_Available += 1
        book.save()

    # Log the return date
        transaction.return_date = date.today()
        transaction.save()

        return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)
