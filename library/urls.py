from django.urls import path
from .views import (BookCheckOutView, BookCreateView, BookDeleteView,
                    BookListView, BookReturnView, UserCreateView,
                    UserDeleteView, UserDetailsView, UserListView,
                    UserUpdateView)
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('checkout/<int:pk>/', BookCheckOutView.as_view(), name='checkout'),
    path('return/<int:pk>/', BookReturnView.as_view(), name='return'),
    path('book/create/', BookCreateView.as_view(), name='book-create'),
    path('book/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('book/list/', BookListView.as_view(), name='book-list'),
    path('user/create/', UserCreateView.as_view(), name='user-create'),
    path('user/list/', UserListView.as_view(), name='user-list'),
    path('user/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('user/<int:pk>/', UserDetailsView.as_view(), name='user-details'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('login/', obtain_auth_token, name='auth-token'),
    path('logout/', obtain_auth_token, name='logout')
]
