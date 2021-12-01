from django.shortcuts import render

# Create your views here.

from django.contrib.auth import authenticate
from itsystem.models import Comment, Issue, Project
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer, ProjectSerializer, IssueSerializer, CommentSerializer, SignUpSerializer

# Create your views here.

#---------------- A refaire -------------------------- 

class SignUpView(APIView):
	serializer_class = SignUpSerializer

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()

		return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
	@api_view(['POST'])

	def authenticate_user(request):
	    try:
	        email = request.data['email']
	        password = request.data['password']

	        user = User.objects.get(email=email, password=password)
	        if user:
	        		try:
	        			payload = jwt_payload_handler(user)
	        			token = jwt.encode(payload, settings.SECRET_KEY)
	        			user_details = {}
	        			user_details['name'] = "%s %s" % (
	        				user.first_name, user.last_name)
	        			user_details['token'] = token
	        			user_logged_in.send(sender=user.__class__,
	        				request=request, user=user)
	        			return Response(user_details, status=status.HTTP_200_OK)

	        		except Exception as exc:
		            		raise exc
	        else:
	        	res = {'error': 'cannot authenticate with the given credentials or the account has been deactivated'}
	        	return Response(res, status=status.HTTP_403_FORBIDDEN)

	    except KeyError:
	    	res = {'error': 'please provide a email and a password'}
	    	return Response(res)

#---------------- A refaire --------------------------

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        serializer = self.serializer_class(self.request.user)
        return serializer.data

class ProjectViewSet(viewsets.ModelViewSet):
	serializer_class = ProjectSerializer
	queryset = Project.objects.all()
	#permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		try:
			project_id = self.request.query_params['id'] 

			if project_id:
				project = Project.objects.get(id=project_id)
				serializer = self.serializer_class(project)
				return serializer.data
		except:
			projects = Project.objects.filter(author_user_id=self.request.user.id)
			serializer = self.serializer_class(projects, many=True)
		return serializer.data

	def create(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			self.perform_create(serializer)
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors)

	def update(self, request, *args, **kwargs):
		project = Project.objects.filter(pk=self.request.project.id)
		project.title = self.validated_data.get('title', project.title)
		project.description = self.validated_data.get('description', project.description)
		project.type_project = self.validated_data.get('type_project', project.type_project)
		project.update()
		return project

	def destroy(self):
		project = Project.objects.filter(pk=self.request.project.id)
		project.delete()

class IssueViewSet(viewsets.ModelViewSet):
	serializer_class = IssueSerializer
	queryset = Issue.objects.all()
	#permission_classes = (IsAuthenticated,)

	pass


class CommentViewSet(viewsets.ModelViewSet):
	serializer_class = CommentSerializer
	queryset = Comment.objects.all()
	#permission_classes = (IsAuthenticated,)

	pass

