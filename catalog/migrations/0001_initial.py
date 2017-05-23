# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('date_of_death', models.DateField(verbose_name='Died', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('summary', models.TextField(max_length=1000, help_text='Enter a brief description')),
                ('isbn', models.CharField(max_length=13, help_text='13 character number', verbose_name='ISBN')),
                ('author', models.ForeignKey(to='catalog.Author', on_delete=django.db.models.deletion.SET_NULL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookInstance',
            fields=[
                ('id', models.UUIDField(serialize=False, default=uuid.uuid4, primary_key=True, help_text='Unique ID for the book')),
                ('imprint', models.CharField(max_length=200)),
                ('due_back', models.DateField(null=True, blank=True)),
                ('status', models.CharField(help_text='Book Availability', max_length=1, blank=True, default='d', choices=[('d', 'Maintainance'), ('o', 'on loan'), ('a', 'Available'), ('r', 'Reserved')])),
                ('book', models.ForeignKey(to='catalog.Book', on_delete=django.db.models.deletion.SET_NULL, null=True)),
            ],
            options={
                'ordering': ['due_back'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction, Poetry)')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(to='catalog.Genre', help_text='Select a genre'),
        ),
    ]
