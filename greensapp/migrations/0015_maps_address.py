# Generated by Django 4.1.3 on 2022-11-14 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greensapp', '0014_alter_social_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='maps',
            name='address',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]