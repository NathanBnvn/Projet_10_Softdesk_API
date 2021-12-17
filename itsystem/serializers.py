from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework import serializers, permissions
from django.contrib.auth.models import User
from .models import Project, Issue, Comment


class SignUpSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
		extra_kwargs = {
			'email': {'required': True},
			'password': {'write_only': True},
		}

	def create(self, validated_data):
		user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
            )

		user.set_password(validated_data['password'])
		user.save()

		return user


class LoginSerializer(TokenObtainPairSerializer):
	# @TO DO fix login

	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)
		token['password'] = user.password
		return token


class ProjectSerializer(serializers.ModelSerializer):

	class Meta:
		model = Project
		fields = ['id', 'title', 'description', 'type_project', 'author_user_id']


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
	project = ProjectSerializer()

	class Meta:
		model = Issue
		fields = ['id', 'title', 'desc', 'tag', 'priority', 'project', 'status', 'author_user_id', 'assignee_user_id', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
	issue = IssueSerializer()

	class Meta:
		model = Comment
		fields = ['id', 'description', 'author_user_id', 'issue_id', 'created_time']

