# Generated by Django 4.1.3 on 2022-11-07 00:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('greensapp', '0005_social_like_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='social',
            name='like_count',
        ),
    ]