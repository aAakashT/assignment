# Generated by Django 4.2.4 on 2023-08-06 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishing_app', '0004_alter_emaillog_recipient_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emaillog',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='emaillog',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='emaillog',
            name='subject',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
