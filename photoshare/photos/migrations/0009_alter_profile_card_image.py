# Generated by Django 3.2.5 on 2021-08-04 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0008_auto_20210804_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='card_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
