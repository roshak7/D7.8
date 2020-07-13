from django.contrib import admin

from .models import Book, Author, Publisher, Friend, UserProfile
from .forms import AuthorAdminForm, FriendAdminForm


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    filter_horizontal = ('friend_reader',)

    @staticmethod
    def author_full_name(obj):
        return obj.author.full_name

    list_display = ('title', 'author_full_name', 'year_release')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    form = AuthorAdminForm


@admin.register(Publisher)
class AdminPublisher(admin.ModelAdmin):
    # prevent default publisher from deleting
    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.id == 1:
            return False
        else:
            return True


@admin.register(Friend)
class AdminFriend(admin.ModelAdmin):
    form = FriendAdminForm
    filter_horizontal = ('books',)


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    pass
