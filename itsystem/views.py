from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from itsystem.models import Comment, Issue, Project, Contributor
from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAuthor, IsContributor
from .serializers import ContributorSerializer, ProjectSerializer, IssueSerializer, CommentSerializer, SignUpSerializer, LoginSerializer


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


class ContributorViewSet(viewsets.ModelViewSet):
	queryset = Contributor.objects.all()
	serializer_class = ContributorSerializer
	permission_classes = (IsAuthor)


class ProjectViewSet(viewsets.ModelViewSet):
	queryset = Project.objects.all()
	serializer_class = ProjectSerializer
	permission_classes = (IsAuthor, IsContributor)


class IssueViewSet(viewsets.ModelViewSet):
	queryset = Issue.objects.all()
	serializer_class = IssueSerializer
	permission_classes = (IsAuthor, IsContributor)


class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	permission_classes = (IsAuthor, IsContributor)

