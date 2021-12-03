from rest_framework import serializers, permissions
from django.contrib.auth.models import User
from .models import Project, Issue, Comment

#---------------- A refaire -------------------------- 

class SignUpSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'first_name', 'last_name', 'email', 'password']
		extra_kwargs = {
			'email': {'required': True},
			'password': {'write_only': True},
		}

		def create(self, validated_data):
			user = User.objects.create_user( 
				first_name=validated_data['first_name'], 
				last_name=validated_data['last_name'], 
				email=validated_data['email'],
				password=validated_data['password'],
				)
			return user


class LoginSerializer(serializers.ModelSerializer):
	class Meta:
		pass

#---------------- A refaire --------------------------


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

