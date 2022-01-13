from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework.fields import CurrentUserDefault
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, Issue, Comment, Contributor


class SignUpSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
		extra_kwargs = {
			'email': {'required': True},
			'password': {'write_only': True},
		}

	def create(self, validated_data):
		user = User.objects.create(**validated_data)
		user.set_password(validated_data['password'])
		user.save()
		return user


class LoginSerializer(TokenObtainPairSerializer):

	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)
		token['password'] = user.password
		return token


class ContributorSerializer(serializers.ModelSerializer):

	class Meta:
		model = Contributor
		fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
	# Create a custom method field
	author_user = serializers.SerializerMethodField('_user')

    # Use this method for the custom field

	def _user(self, obj):
		request = self.context.get('request', None)
		if request:
			return request.user

	class Meta:
		model = Project
		fields = '__all__'
		read_only_fields = ['author_user']

	def create(self, validated_data):
	 	project = Project.objects.create(**validated_data)
	 	project.author_user = self.context['request'].user
	 	return project.save()


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

