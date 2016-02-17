# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-17 15:26
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geocode', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('match_option', models.CharField(blank=True, choices=[('ADDRESSID', 'AddressID'), ('STREET', 'Street'), ('CITY', 'City'), ('STATE', 'State'), ('ZIP', 'Zip')], help_text='(required) Select AddressID, Street, City, State, Zip', max_length=30, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geocode.Project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectionSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('srid', models.IntegerField(help_text='A Spatial Reference System Identifier (SRID) is a unique value used to unambiguously identify projected, unprojected, and local spatial coordinate system definitions. You will get lat_prj, and lon_prj in your files')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectProjectionOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geocode.Project')),
                ('srid', models.ForeignKey(help_text='A Spatial Reference System Identifier (SRID) is a unique value used to unambiguously identify projected, unprojected, and local spatial coordinate system definitions. You will get lat_prj, and lon_prj in your files', on_delete=django.db.models.deletion.CASCADE, to='geocode.ProjectionSetting')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectRecordIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_row_id', models.CharField(blank=True, max_length=180)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geocode.Project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(blank=True, max_length=120)),
                ('total_records', models.IntegerField(default=0)),
                ('result_file', models.FileField(blank=True, upload_to='result')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quoting', models.CharField(blank=True, choices=[('QUOTE_ALL', 'QUOTE_ALL'), ('QUOTE_MINIMAL', 'QUOTE_MINIMAL'), ('QUOTE_NONNUMERIC', 'QUOTE_NONNUMERIC'), ('QUOTE_NONE', 'QUOTE_NONE'), (None, 'NONE')], default=None, help_text='Use QUOTE_NONNUMERIC for excel. https://docs.python.org/2/library/csv.html#csv.QUOTE_ALL', max_length=30, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geocode.Project')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_id', models.CharField(blank=True, max_length=256)),
                ('street', models.CharField(blank=True, max_length=80)),
                ('ignore_street', models.BooleanField(default=False)),
                ('city', models.CharField(blank=True, max_length=80)),
                ('ignore_city', models.BooleanField(default=False)),
                ('state', models.CharField(blank=True, max_length=80)),
                ('ignore_state', models.BooleanField(default=False)),
                ('zip', models.CharField(blank=True, max_length=80)),
                ('geo_score', models.DecimalField(blank=True, decimal_places=2, help_text="Online Resource (GoogleV3, Bing, MapQuest) and User Edit own't have Geo score", max_digits=11, null=True)),
                ('geo_address', models.CharField(blank=True, max_length=180)),
                ('geo_lat', models.CharField(blank=True, help_text='projection 4326', max_length=80)),
                ('geo_lon', models.CharField(blank=True, help_text='projection 4326', max_length=80)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326)),
                ('have_value', models.BooleanField(default=False)),
                ('flag', models.BooleanField(default=False)),
                ('resource', models.CharField(blank=True, default='', max_length=80)),
                ('project', models.ManyToManyField(blank=True, related_name='project_filter', through='geocode.ProjectRecordIndex', to='geocode.Project')),
            ],
        ),
        migrations.AddField(
            model_name='projectrecordindex',
            name='record',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geocode.Record'),
        ),
    ]
