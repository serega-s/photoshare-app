# Generated by Django 3.2.5 on 2021-08-10 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0013_alter_profile_follows'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
