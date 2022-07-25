from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .models import (
    Category,
    Title,
    Genre,
    Review,
    Comment,
    User,
)

EMPTY_VALUE = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Отображение категорий в административной панели.
    """

    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Отображение жанров в административной панели.
    """

    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_display_links = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """
    Отображение произведений в административной панели.
    """

    list_display = (
        'pk',
        'name',
        'year',
        'category',
        'get_genre_names',
    )
    search_fields = (
        'name',
        'year',
        'category__name',
    )
    list_filter = (
        'name',
        'year',
        'category__name',
    )
    list_editable = ('category',)
    list_display_links = ('name',)
    empty_value_display = EMPTY_VALUE

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super().get_queryset(request)
        return qs.select_related('category').prefetch_related('genre')

    def get_genre_names(self, obj: Title) -> str:
        """
        Метод отображения имен жанров в модели произведения.
        :param obj: Модель произведения.
        :return: Имена жанров в формате строки.
        """

        return ', '.join(obj.genre.all().values_list('name', flat=True))

    get_genre_names.short_description = 'Жанры'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Отображение отзывов в административной панели.
    """

    list_display = (
        'pk',
        'author',
        'title',
        'score',
        'pub_date',
    )
    search_fields = (
        'author__username',
        'title__name',
        'score',
        'pub_date',
    )
    list_filter = (
        'author__username',
        'title__name',
        'score',
    )

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super().get_queryset(request)
        return qs.select_related('author', 'title')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Отображение комментариев в административной панели.
    """

    list_display = (
        'pk',
        'author',
        'review',
        'pub_date',
    )
    search_fields = (
        'author__username',
        'pub_date',
    )
    list_filter = ('author__username',)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        qs = super().get_queryset(request)
        return qs.select_related('author', 'review')


@admin.register(User)
class UserAppAdmin(UserAdmin):
    """
    Модель пользователя в админке
    """

    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_superuser',
        'date_joined',
    )
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'username',
                    'email',
                    'password',
                )
            },
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_superuser',
                    'is_staff',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            _('Important dates'),
            {
                'fields': (
                    'last_login',
                    'date_joined',
                )
            },
        ),
        (
            _('Дополнительная информация'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'role',
                    'bio',
                )
            },
        ),
    )
    readonly_fields = (
        'last_login',
        'date_joined',
    )
    ordering = ('-date_joined',)
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'role',
                    'password1',
                    'password2',
                    'is_superuser',
                ),
            },
        ),
    )
    list_filter = (
        'id',
        'username',
        'role',
    )
    list_editable = (
        'role',
        'is_superuser',
    )
    list_display_links = ('username',)
