# Generated by Django 4.1.3 on 2022-11-06 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greensapp', '0004_social_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='social',
            name='like_count',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]
