# Generated by Django 4.1.3 on 2022-11-08 19:47

from django.db import migrations
import greensapp.formatchecker


class Migration(migrations.Migration):

    dependencies = [
        ('greensapp', '0013_alter_social_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='social',
            name='file',
            field=greensapp.formatchecker.ContentTypeRestrictedFileField(blank=True, null=True, upload_to='media/'),
        ),
    ]