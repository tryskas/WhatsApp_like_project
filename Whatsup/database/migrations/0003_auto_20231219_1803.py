# Generated by Django 3.2.18 on 2023-12-19 18:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_remove_user_nouvel_attribut'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversation',
            name='moderateur',
        ),
        migrations.AddField(
            model_name='conversation',
            name='destinataire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conversations_dest', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='utilisateur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Moderation',
        ),
    ]