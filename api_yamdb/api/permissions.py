from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    """
    Проверка прав на "владельца" объекта.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author == request.user


class IsModerator(BasePermission):
    """
    Проверка прав на Модератора.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_moderator


class IsAdmin(BasePermission):
    """
    Проверка прав на Админа.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(BasePermission):
    """
    Проверка прав на Админа с расширенным функционалам
    доступа для безопасных методов(SAFE_METHODS)
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsSuperuser(BasePermission):
    """
    Проверка прав на Суперпользователя.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.is_superuser
