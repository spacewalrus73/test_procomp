# Generated by Django 4.2.6 on 2023-10-12 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='column_names',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='files',
            name='file_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
