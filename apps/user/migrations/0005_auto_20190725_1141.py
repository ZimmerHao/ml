# Generated by Django 2.1 on 2019-07-25 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20190725_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useroauth',
            name='username',
            field=models.CharField(max_length=255, verbose_name='username'),
        ),
    ]
