from django.contrib.auth.models import User
from rest_framework import permissions
from Reading import models


class CurrentUserPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username


class CurrentProfilePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user.username == request.user.username


class CurrentUserAnswerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.data['user'] == request.user.id
        elif request.method == 'GET':
            return self.has_object_permission

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return obj.user.username == request.user.username

