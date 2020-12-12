from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_anonymous and request.user.is_business)


class IsLogisticServices(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(
            super().has_permission(request, view) and getattr(request.user, 'is_logistic_service', False)
        )


class IsSeller(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(super().has_permission(request, view) and getattr(request.user, 'is_seller', False))
