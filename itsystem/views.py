from django.shortcuts import render

# Create your views here.

from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from itsystem.models import Comment, Issue, Project
from .serializers import UserSerializer, ProjectSerializer, IssueSerializer, CommentSerializer, SignUpSerializer

# Create your views here.


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


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProjectViewSet(viewsets.ModelViewSet):
	serializer_class = ProjectSerializer
	permission_classes = (IsAuthenticated,)

	def get(self, request, *args, **kwargs):
		try:
			project_id = request.query_params['id'] 

			if project_id:
				project = Project.objects.get(id=project_id)
				serializer = self.serializer_class(project)
				return Response(serializer.data, status=status.HTTP_200_OK)
		except:
			projects = Project.objects.filter(author_user_id=request.user.id)
			serializer = self.serializer_class(projects, many=True)

		return Response(serializer.data, status=status.HTTP_200_OK)

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, pk=None, *args, **kwargs):
		project = Project.objects.filter(pk=request.project.id).update()
		return Response()

	def delete(self, request, *args, **kwargs):
		project = Project.objects.filter(pk=request.project.id)
		project.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class IssueViewSet(viewsets.ModelViewSet):
	pass

class CommentViewSet(viewsets.ModelViewSet):
	pass