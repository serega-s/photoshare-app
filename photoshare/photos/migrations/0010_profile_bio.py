# Generated by Django 3.2.5 on 2021-08-04 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0009_alter_profile_card_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
