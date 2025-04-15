from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Books(models.Model):
    Title = models.CharField(max_length=100)
    Author = models.CharField(max_length=100)
    ISBN = models.IntegerField(unique=True)
    Published_Date = models.DateField()
    Number_of_Copies_Available = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.Title}, is written by {self.Author}'


class LibraryUser(AbstractUser):
    Date_of_Membership = models.DateField(auto_now_add=True)
    Active_Status = models.BooleanField(default=True)
    books_checked_out = models.ManyToManyField('Books', blank=True, related_name='checked_out_by')

    def __str__(self):
        return f"{self.username}"


class Transaction(models.Model):
    user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    checkout_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.book}'
