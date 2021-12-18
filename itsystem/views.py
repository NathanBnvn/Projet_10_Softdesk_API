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


class ProjectViewSet(viewsets.ModelViewSet):
	serializer_class = ProjectSerializer
	queryset = Project.objects.all()
	permission_classes = (IsAuthenticated,)


class IssueViewSet(viewsets.ModelViewSet):
	serializer_class = IssueSerializer
	queryset = Issue.objects.all()
	permission_classes = (IsAuthenticated,)


class CommentViewSet(viewsets.ModelViewSet):
	serializer_class = CommentSerializer
	queryset = Comment.objects.all()
	permission_classes = (IsAuthenticated,)


