# Generated by Django 4.1.4 on 2022-12-19 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Board',
            new_name='Forum',
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='board',
            new_name='forum',
        ),
    ]
