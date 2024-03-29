# Generated by Django 2.1 on 2019-05-23 16:26

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_name', models.CharField(max_length=255, verbose_name='resource name')),
                ('short_name', models.CharField(blank=True, max_length=255, verbose_name='resource short name')),
                ('api_group', models.CharField(blank=True, max_length=255, verbose_name='api group')),
                ('namespaced', models.BooleanField(default=False, verbose_name='is namespace resource')),
                ('kind', models.CharField(max_length=255, verbose_name='resource kind')),
                ('is_active', models.BooleanField(default=True, verbose_name='active status')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='updated date')),
            ],
            options={
                'db_table': 'k8s_resource',
            },
        ),
        migrations.CreateModel(
            name='KRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='k8s role name')),
                ('namespace', models.CharField(max_length=255, verbose_name='k8s namespace name')),
                ('verbs', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, size=None, verbose_name='k8s api resource verb')),
                ('is_active', models.BooleanField(default=True, verbose_name='active status')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='updated date')),
                ('k8s_resources', models.ManyToManyField(blank=True, to='kauth.KResource', verbose_name='k8s resources')),
            ],
            options={
                'db_table': 'k8s_role',
            },
        ),
    ]
