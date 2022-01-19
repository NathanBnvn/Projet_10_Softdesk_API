from rest_framework import permissions

class IsAuthor(permissions.BasePermission):
	# Author has access to CRUD methods 

	def has_permission(self, request, view):
		if request.user.is_authenticated:
			return True

	def has_object_permission(self, request, view, obj):
		if request.user.is_superuser:
			return True

		if request.method in permissions.SAFE_METHODS:
			return True

		if obj.author_user == request.user:
			return True

		return False


class IsContributor(permissions.BasePermission):
	# Contributor are not allow to Update or Delete project, issue or comment instances

	editing_methods = ("PUT", "PATCH", "DEL")

	def has_permission(self, request, view):
		if request.user.is_authenticated:
			return True

	def has_object_permission(self, request, view, obj):
		if request.user.is_superuser:
			return True

		if request.method in permissions.SAFE_METHODS:
			return True

		if obj.author_user != request.user and request.methods not in self.editing_methods:
			return True

		return False