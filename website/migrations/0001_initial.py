# Generated by Django 2.1 on 2020-01-14 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='envent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.IntegerField(default=None, max_length=12)),
                ('eventID', models.IntegerField(default=None, max_length=12)),
                ('remark', models.CharField(blank=True, max_length=339, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=512, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TuPian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=256, null=True)),
                ('passwd', models.CharField(blank=True, max_length=64, null=True)),
                ('remark', models.CharField(blank=True, max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='user_openID',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, max_length=32, null=True)),
                ('openID', models.CharField(blank=True, max_length=128, null=True)),
                ('remark', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
    ]
