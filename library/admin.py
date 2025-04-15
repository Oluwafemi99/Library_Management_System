from django.contrib import admin
from .models import LibraryUser, Books, Transaction


class LibraryUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'Date_of_Membership', 'Active_Status', 'checked_out_books')

    def checked_out_books(self, obj):
        # Display the titles of books checked out by the user
        return ", ".join([book.Title for book in obj.books_checked_out.all()])
    checked_out_books.short_description = 'Books Checked Out'


admin.site.register(LibraryUser, LibraryUserAdmin)
admin.site.register(Books)
admin.site.register(Transaction)
