# Generated by Django 2.1 on 2019-07-30 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_useroauth_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='useroauth',
            name='password',
            field=models.CharField(default=0, max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
    ]