from rest_framework import permissions

class IsAuthor(permissions.BasePermission):

	def has_permission(self, request, view):
		if request.user.is_authenticated:
			return True

	def has_object_permission(self, request, view, obj):
		if request.user.is_superuser:
			return True

		if request.method in permissions.SAFE_METHODS:
			return True

		if obj.author == request.user:
			return True


class IsContributor(permissions.BasePermission):
	# Contributor are not allow to Update or Delete project, issue or comment instances

	modify_methods = ("PUT", "PATCH", "DEL")

	def has_permission(self, request, view):
		if request.user.is_authenticated:
			return True

	def has_object_permission(self, request, view, obj):
		if request.user.is_superuser:
			return True

		if request.method in permissions.SAFE_METHODS:
			return True

		if obj.author != request.user and request.methods not in self.modify_methods:
			return True

		return False