# Generated by Django 4.1.3 on 2022-11-06 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('greensapp', '0002_rename_post_type_social_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='social',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='greensapp.posttype'),
        ),
    ]