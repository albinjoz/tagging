# Generated by Django 3.1.1 on 2020-09-30 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0002_auto_20200930_1450'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imageupload',
            name='postedDate',
        ),
        migrations.AddField(
            model_name='post',
            name='postedDate',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
    ]
