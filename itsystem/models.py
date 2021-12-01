from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
	BACK_END = 'BCK'
	FRONT_END = 'FRT'
	IOS = 'IOS'
	ANDROID = 'AND'

	TYPE_CHOICE = [
		(BACK_END, 'Back-end'),
		(FRONT_END, 'Front-end'),
		(IOS,'IOS'),
		(ANDROID, 'Android')
	]

	title = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	type_project = models.CharField(max_length=3, choices=TYPE_CHOICE)
	author_user_id = models.ManyToManyField(User, through='Contributor')

	def __str__(self):
		return self.title


class Contributor(models.Model):
	AUTEUR = 'AUT'
	RESPONSABLE = 'RES'
	CREATEUR = 'CRE'

	ROLE_CHOICE = [
		(AUTEUR, 'Auteur'),
		(RESPONSABLE, 'Responsable'),
		(CREATEUR, 'Créateur')
	]

	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
	permission = models.CharField(max_length=3)
	role = models.CharField(max_length=100, choices=ROLE_CHOICE)


class Issue(models.Model):
	BUG = 'BUG'
	AMELIORATION = 'AML'
	TACHE = 'TCH'

	TAG_CHOICE = [
		(BUG, 'Bug'),
		(AMELIORATION, 'Amélioration'),
		(TACHE,'Tâche'),
	]
	
	FAIBLE = 'FBL'
	MOYENNE = 'MOY'
	ELEVE = 'ELV'

	PRIORITY_CHOICE = [
		(FAIBLE, 'Faible'),
		(MOYENNE, 'Moyenne'),
		(ELEVE, 'Élevée'),
	]

	A_FAIRE = 'AFR'
	EN_COURS = 'NCR'
	TERMINÉ = 'TRM'

	STATUS_CHOICE = [
		(A_FAIRE, 'À faire'),
		(EN_COURS, 'En Cours'),
		(TERMINÉ, 'Terminé'),
	]

	title = models.CharField(max_length=100)
	desc = models.CharField(max_length=100)
	tag = models.CharField(max_length=3, choices=TAG_CHOICE)
	priority = models.CharField(max_length=3, choices=PRIORITY_CHOICE)
	project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
	status = models.CharField(max_length=3, choices=STATUS_CHOICE)
	author_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_user_id')
	assignee_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee_user_id')
	created_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title


class Comment(models.Model):
	description = models.CharField(max_length=700)
	author_user_id = models.ForeignKey(User, on_delete=models.CASCADE )
	issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE)
	created_time = models.DateTimeField(auto_now_add=True)

