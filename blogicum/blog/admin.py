from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from django.utils.safestring import mark_safe

from .models import Category, Comment, Location, Post


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_display = (
        'title',
        'description',
        'is_published',
    )
    list_editable = ('is_published',)
    search_fields = ('title', 'description')
    list_filter = ('is_published',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published'
    )
    list_editable = ('is_published',)
    search_fields = ('name',)
    list_filter = ('is_published',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'is_published',
        'author',
        'location',
        'pub_date',
        'image_of_post'
    )
    list_editable = ('is_published', 'pub_date')
    search_fields = ('title', 'text')
    list_filter = (
        'is_published',
        'category',
        'author',
        'location'
    )

    @admin.display(description='Фото')
    def image_of_post(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src={obj.image.url} width="80" height="60">'
            )


admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'posts_count',
        'comments_count',
        'is_staff'
    )

    @admin.display(description='Количествово постов у пользователя: ')
    def posts_count(self, obj):
        return obj.posts.count()

    @admin.display(description='Количество комментариев у пользователя: ')
    def comments_count(self, obj):
        return obj.comments.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'text',
        'post',
    )
    search_fields = ('text',)
    list_filter = ('author', 'post')
