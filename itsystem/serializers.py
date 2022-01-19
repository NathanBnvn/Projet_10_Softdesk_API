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

	class Meta:
		model = Project
		fields = '__all__'
		read_only_fields = ['author_user']

	def create(self, validated_data):
	 	project = Project.objects.create(**validated_data)
	 	project.author_user = self.context['request'].user
	 	project.save()
	 	Contributor.objects.create(user=project.author_user, project=project, permission='Auteur', role='Author')
	 	return project


class IssueSerializer(serializers.ModelSerializer):
	#project = ProjectSerializer()
	#project = serializers.PrimaryKeyRelatedField(read_only=True)

	class Meta:
		model = Issue
		fields = '__all__'
		depth = 1

	def create(self, validated_data):
		issue = Issue.objects.create(**validated_data)
		issue.author_user = self.context['request'].user
		issue.assignee_user = self.context['request'].user
		#issue.save()
		return issue


class CommentSerializer(serializers.ModelSerializer):
	issue = IssueSerializer()

	class Meta:
		model = Comment
		fields = '__all__'

	def create(self, validated_data):
		comment = Comment.objects.create(**validated_data)
		#comment.issue = Issue.objects.get()
		comment.author_user = self.context['request'].user
		comment.save()
		return comment

