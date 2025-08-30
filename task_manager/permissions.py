from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of this object to modify it."

    def has_object_permission(self, request, view, obj):
        # чтение всем
        if request.method in SAFE_METHODS:
            return True

        # взять владельца напрямую
        owner = getattr(obj, "owner", None)

        # если это вложенный объект, у которого owner на связанной модели
        if owner is None and hasattr(obj, "task"):
            owner = getattr(obj.task, "owner", None)

        return owner == request.user
