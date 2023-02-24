# cats/permissions.py

from rest_framework import permissions

#  В приложении cat опишите и примените пермишен, который не даст пользователю
#  удалить или отредактировать чужие публикации.
#  Запрашивать список всех публикаций или отдельную публикацию может любой
#  пользователь.
#  Создавать новую публикацию может только аутентифицированный пользователь.


class OwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


#    def has_permission(self, request, view):
#        return (
#                request.method in permissions.SAFE_METHODS
#                or request.user.is_authenticated
#            )
#
#    def has_object_permission(self, request, view, obj):
#        return obj.owner == request.user
#
#
# class ReadOnly(permissions.BasePermission):
#
#    def has_permission(self, request, view):
#        return request.method in permissions.SAFE_METHODS
