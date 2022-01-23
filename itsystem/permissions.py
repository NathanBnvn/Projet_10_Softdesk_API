from rest_framework import permissions

class IsAuthor(permissions.BasePermission):
	# Author has access to CRUD methods 

	def has_permission(self, request, view):
		if request.user.is_authenticated:
			return True

		# If current user is among contributors of the related project, she/he may access the endpoints of referenced views
		if view.basename == 'issues'| view.basename == 'comments' | view.basename == 'contributors':
			contributors = Project.objects.get(pk=view.kwargs.get('project_pk')).contributors.all()
			if request.user in contributors:
				return True

	def has_object_permission(self, request, view, obj):
		if request.user.is_superuser:
			return True

		if request.method in permissions.SAFE_METHODS:
			return True

		if obj.author_user == request.user:
			return True


class IsContributor(permissions.BasePermission):
	# Contributor are not allow to Update or Delete project, issue or comment instances

	editing_methods = ("PUT", "PATCH", "DEL")

	def has_permission(self, request, view):
		if request.user.is_authenticated:
			return True

		# If current user is among contributors, she/he may access the projects endpoint
		if view.basename == 'projects':
			contributors = Project.objects.get(pk=view.kwargs.get('pk', None)).contributors.all()
			if request.user in contributors:
				return True


		# If current user is among contributors of the project, she/he may access the endpoints of referenced views
		if view.basename == 'issues'| view.basename == 'comments' | view.basename == 'contributors':
			contributors = Project.objects.get(pk=view.kwargs.get('project_pk')).contributors.all()
			if request.user in contributors:
				return True


	def has_object_permission(self, request, view, obj):
		if request.user.is_superuser:
			return True

		if request.method in permissions.SAFE_METHODS:
			return True

		if obj.author_user != request.user and request.method not in editing_methods:
			return True
