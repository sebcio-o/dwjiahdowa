# Generated by Django 4.0.5 on 2022-07-02 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('last_edited', models.DateTimeField(auto_now=True, verbose_name='Last edited')),
                ('creation_time', models.DateTimeField(auto_now_add=True, verbose_name='Creation time')),
            ],
        ),
        migrations.CreateModel(
            name='WorkspacePermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_type', models.CharField(choices=[('A', 'Administrator'), ('N', 'Normal'), ('O', 'Observer')], max_length=1, verbose_name='Workspace permission type')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspaces.workspace')),
            ],
        ),
        migrations.CreateModel(
            name='WorkspaceInvitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(default=uuid.uuid4, max_length=255)),
                ('generated_at', models.DateTimeField(auto_now_add=True)),
                ('generated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workspaces.workspace')),
            ],
        ),
        migrations.AddConstraint(
            model_name='workspacepermission',
            constraint=models.UniqueConstraint(fields=('workspace', 'user'), name='WorkspacePermission.unique_workspace_user'),
        ),
    ]