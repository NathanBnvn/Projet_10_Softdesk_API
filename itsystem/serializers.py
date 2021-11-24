from rest_framework import serializers, permissions
from django.contrib.auth.models import User
from .models import Project, Issue, Comment


class SignUpSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'first_name', 'last_name', 'email', 'password')
		extra_kwargs = {
			'password': {'write_only': True},
		}

		def create(self, validated_data):
			user = User.objects.create_user(
				username=validated_data['username'], 
				password=validated_data['password'], 
				first_name=validated_data['first_name'], 
				last_name=validated_data['last_name'], 
				email=validated_data['email']
				)
			return user


class LoginSerializer(serializers.ModelSerializer):
	class Meta:
		pass


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Project
		fields = ['id', 'title', 'description', 'type_project', 'author_user_id']

	def create(self, validated_data):
		project = Project.objects.create_project(
			title=validated_data['title'], 
			description=validated_data['description'], 
			type_project=validated_data['type_project'], 
			author_user_id=validated_data['user']
			)
		return project

class IssueSerializer(serializers.ModelSerializer):
	class Meta:
		model = Issue
		fields = ['id', 'title', 'desc', 'tag', 'priority', 'project_id', 'status', 'author_user_id', 'assignee_user_id', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = ['id', 'description', 'author_user_id', 'issue_id', 'created_time']
