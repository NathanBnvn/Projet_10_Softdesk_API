from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
	BACK_END = 'back-end'
	FRONT_END = 'front-end'
	IOS = 'ios'
	ANDROID = 'android'

	TYPE_CHOICE = [
		(BACK_END, 'back-end'),
		(FRONT_END, 'front-end'),
		(IOS,'ios'),
		(ANDROID, 'android')
	]

	title = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	type_project = models.CharField(max_length=20, choices=TYPE_CHOICE)
	author_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='projects')
	contributors = models.ManyToManyField(User, through='Contributor')

	def __str__(self):
		return self.title


class Contributor(models.Model):
	AUTEUR = 'auteur'
	CONTRIBUTEUR = 'contributeur'

	PERMISSION_CHOICE = [
		(AUTEUR, 'auteur'),
		(CONTRIBUTEUR, 'contributeur'),
	]

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributor')
	project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE, related_name='contributor')
	permission = models.CharField(max_length=20, choices=PERMISSION_CHOICE)
	role = models.CharField(max_length=20)

	#class Meta:
		#constraints = [models.UniqueConstraint(fields=['user_id'], name="user")]

# @TODO set unique user with meta in Contributor

class Issue(models.Model):
	BUG = 'bug'
	AMELIORATION = 'amélioration'
	TACHE = 'tâche'

	TAG_CHOICE = [
		(BUG, 'bug'),
		(AMELIORATION, 'amélioration'),
		(TACHE,'tâche'),
	]
	
	FAIBLE = 'faible'
	MOYENNE = 'moyenne'
	ELEVEE = 'élevée'

	PRIORITY_CHOICE = [
		(FAIBLE, 'faible'),
		(MOYENNE, 'moyenne'),
		(ELEVEE, 'élevée'),
	]

	A_FAIRE = 'a faire'
	EN_COURS = 'en cours'
	TERMINÉ = 'terminé'

	STATUS_CHOICE = [
		(A_FAIRE, 'a faire'),
		(EN_COURS, 'en Cours'),
		(TERMINÉ, 'terminé'),
	]

	title = models.CharField(max_length=100)
	desc = models.CharField(max_length=1000)
	tag = models.CharField(max_length=20, choices=TAG_CHOICE)
	priority = models.CharField(max_length=20, choices=PRIORITY_CHOICE)
	project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.CASCADE, related_name='issue')
	status = models.CharField(max_length=20, choices=STATUS_CHOICE)
	author_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='author')
	assignee_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='assignee')
	created_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title


class Comment(models.Model):
	description = models.CharField(max_length=700)
	author_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='comment')
	issue = models.ForeignKey(Issue, blank=True, null=True, on_delete=models.CASCADE, related_name='comment')
	created_time = models.DateTimeField(auto_now_add=True)

