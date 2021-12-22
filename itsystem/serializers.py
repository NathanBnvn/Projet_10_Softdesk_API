from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework.fields import CurrentUserDefault
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

	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)
		token['password'] = user.password
		return token


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
	author_user = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

	class Meta:
		model = Project
		fields = '__all__'


class IssueSerializer(serializers.ModelSerializer):
	project = ProjectSerializer()

	class Meta:
		model = Issue
		fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
	issue = IssueSerializer()

	class Meta:
		model = Comment
		fields = '__all__'

