from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
	BACK_END = 'Back-end'
	FRONT_END = 'Front-end'
	IOS = 'IOS'
	ANDROID = 'Android'

	TYPE_CHOICE = [
		(BACK_END, 'Back-end'),
		(FRONT_END, 'Front-end'),
		(IOS,'IOS'),
		(ANDROID, 'Android')
	]

	title = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	type_project = models.CharField(max_length=20, choices=TYPE_CHOICE)
	author_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='projects')
	contributors = models.ManyToManyField(User, through='Contributor')

	def __str__(self):
		return self.title


class Contributor(models.Model):
	AUTEUR = 'Auteur'
	CONTRIBUTEUR = 'Contributeur'

	ROLE_CHOICE = [
		(AUTEUR, 'Auteur'),
		(CONTRIBUTEUR, 'Contributeur'),
	]

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributor')
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributor')
	permission = models.CharField(max_length=20, choices=ROLE_CHOICE)
	role = models.CharField(max_length=20)

# @TODO set unique user with meta in Contributor

class Issue(models.Model):
	BUG = 'Bug'
	AMELIORATION = 'Amélioration'
	TACHE = 'Tâche'

	TAG_CHOICE = [
		(BUG, 'Bug'),
		(AMELIORATION, 'Amélioration'),
		(TACHE,'Tâche'),
	]
	
	FAIBLE = 'Faible'
	MOYENNE = 'Moyenne'
	ELEVEE = 'Elevée'

	PRIORITY_CHOICE = [
		(FAIBLE, 'Faible'),
		(MOYENNE, 'Moyenne'),
		(ELEVEE, 'Élevée'),
	]

	A_FAIRE = 'À faire'
	EN_COURS = 'En cours'
	TERMINÉ = 'Terminé'

	STATUS_CHOICE = [
		(A_FAIRE, 'À faire'),
		(EN_COURS, 'En Cours'),
		(TERMINÉ, 'Terminé'),
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
	issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comment')
	created_time = models.DateTimeField(auto_now_add=True)

