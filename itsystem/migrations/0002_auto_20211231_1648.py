# Generated by Django 3.2.9 on 2021-12-31 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('itsystem', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='project_id',
            new_name='project',
        ),
        migrations.RemoveField(
            model_name='contributor',
            name='project_id',
        ),
        migrations.RemoveField(
            model_name='contributor',
            name='user_id',
        ),
        migrations.AddField(
            model_name='contributor',
            name='project',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='contributor', to='itsystem.project'),
        ),
        migrations.AddField(
            model_name='contributor',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='contributor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='contributors',
            field=models.ManyToManyField(through='itsystem.Contributor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='issue_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='itsystem.issue'),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='permission',
            field=models.CharField(choices=[('Auteur', 'Auteur'), ('Responsable', 'Responsable'), ('Créateur', 'Créateur')], max_length=20),
        ),
        migrations.AlterField(
            model_name='contributor',
            name='role',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='issue',
            name='assignee_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='author_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='desc',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='issue',
            name='priority',
            field=models.CharField(choices=[('Faible', 'Faible'), ('Moyenne', 'Moyenne'), ('Elevée', 'Élevée')], max_length=20),
        ),
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('À faire', 'À faire'), ('En cours', 'En Cours'), ('Terminé', 'Terminé')], max_length=20),
        ),
        migrations.AlterField(
            model_name='issue',
            name='tag',
            field=models.CharField(choices=[('Bug', 'Bug'), ('Amélioration', 'Amélioration'), ('Tâche', 'Tâche')], max_length=20),
        ),
        migrations.RemoveField(
            model_name='project',
            name='author_user_id',
        ),
        migrations.AddField(
            model_name='project',
            name='author_user_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='type_project',
            field=models.CharField(choices=[('Back-end', 'Back-end'), ('Front-end', 'Front-end'), ('IOS', 'IOS'), ('Android', 'Android')], max_length=20),
        ),
    ]