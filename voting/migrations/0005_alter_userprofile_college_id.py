# Generated by Django 4.2 on 2025-02-15 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0004_alter_vote_college_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='college_id',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
