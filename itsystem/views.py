from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from itsystem.models import Comment, Issue, Project
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, ProjectSerializer, IssueSerializer, CommentSerializer, SignUpSerializer, LoginSerializer


class SignUpView(APIView):
	serializer_class = SignUpSerializer

	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		response = serializer.data
		user = User.objects.get(email=response['email'])
		refresh = RefreshToken.for_user(user)
		response['refresh'] = str(refresh)
		response['access'] = str(refresh.access_token)
		return Response(response, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
	serializer_class = LoginSerializer
	permission_classes = (AllowAny,)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
	serializer_class = ProjectSerializer
	queryset = Project.objects.all()
	permission_classes = (IsAuthenticated,)

	def create(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			self.perform_create(serializer)
			serializer.save(author_user_id=request.user.id)
			return Response(serializer.data)
		return Response(serializer.errors)

	def list(self, request):
		serializer = self.serializer_class(self.queryset, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk=None):
		project = get_object_or_404(self.queryset, pk=pk)
		serializer = self.serializer_class(project)
		return Response(serializer.data)

	def partial_update(self, request, pk=None):
		project = get_object_or_404(self.queryset, pk=pk)
		project.title = request.data.get('title')
		project.description = request.data.get('description')
		project.type_project = request.data.get('type_project')

		serializer = self.serializer_class(project, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		return Response(serializer.data)

	def update(self, request, pk=None):
		project = get_object_or_404(self.queryset, pk=pk)
		project.title = request.data.get('title')
		project.description = request.data.get('description')
		project.type_project = request.data.get('type_project')

		serializer = self.serializer_class(project, data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_update(serializer)
		return Response(serializer.data)

	def destroy(self, request, pk=None):
		project = get_object_or_404(self.queryset, pk=pk)
		project.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


class IssueViewSet(viewsets.ModelViewSet):
	serializer_class = IssueSerializer
	queryset = Issue.objects.all()
	permission_classes = (IsAuthenticated,)


class CommentViewSet(viewsets.ModelViewSet):
	serializer_class = CommentSerializer
	queryset = Comment.objects.all()
	permission_classes = (IsAuthenticated,)


