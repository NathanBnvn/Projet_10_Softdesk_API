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


class ProjectViewSet(viewsets.ModelViewSet):
	serializer_class = ProjectSerializer
	permission_classes = (IsAuthor, IsContributor,)

	def get_queryset(self):
		return Project.objects.filter(contributors=self.request.user)


class ContributorViewSet(viewsets.ModelViewSet):
	serializer_class = ContributorSerializer
	permission_classes = (IsAuthor,)

	def dispatch(self, request, *args, **kwargs):
		parent_view = ProjectViewSet.as_view({"get": "retrieve"})
		original_method = request.method
		request.method = "GET"
		parent_kwargs = {"pk": kwargs["project_pk"]}

		parent_response = parent_view(request, *args, **parent_kwargs)
		if parent_response.exception:
			return parent_response

		request.method = original_method
		return super().dispatch(request, *args, **kwargs)

	def get_queryset(self):
		return Contributor.objects.filter(project=self.kwargs['project_pk'])

class IssueViewSet(viewsets.ModelViewSet):
	serializer_class = IssueSerializer
	permission_classes = (IsAuthor, IsContributor,)

	def dispatch(self, request, *args, **kwargs):
		parent_view = ProjectViewSet.as_view({"get": "retrieve"})
		original_method = request.method
		request.method = "GET"
		parent_kwargs = {"pk": kwargs["project_pk"]}

		parent_response = parent_view(request, *args, **parent_kwargs)
		if parent_response.exception:
			return parent_response

		request.method = original_method
		return super().dispatch(request, *args, **kwargs)

	def get_queryset(self):
		return Issue.objects.filter(project=self.kwargs['project_pk'])


class CommentViewSet(viewsets.ModelViewSet):
	serializer_class = CommentSerializer
	permission_classes = (IsAuthor, IsContributor,)

	def dispatch(self, request, *args, **kwargs):
		parent_view = ProjectViewSet.as_view({"get": "retrieve"})
		original_method = request.method
		request.method = "GET"
		parent_kwargs = {"pk": kwargs["project_pk"]}

		parent_response = parent_view(request, *args, **parent_kwargs)
		if parent_response.exception:
			return parent_response

		request.method = original_method
		return super().dispatch(request, *args, **kwargs)

	def get_queryset(self):
		return Comment.objects.filter(issue=self.kwargs['issues_pk'])

