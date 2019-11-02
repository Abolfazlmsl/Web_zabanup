from django.contrib.auth.models import User
from rest_framework import permissions
from Reading import models


class UserPermission(permissions.BasePermission):
    """
    Permission check for blacklisted IPs.
    """

    def has_object_permission(self, request, view, obj):
        # ip_addr = request.GET.get('user_id')
        # current_user = User.objects.get(id=request.META.get('pk')).exists()
        return obj.username == request.user.username
