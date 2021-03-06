# Generated by Django 2.0.4 on 2018-10-04 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user_account', models.CharField(max_length=255)),
                ('password_account', models.CharField(max_length=255)),
                ('recovery_email', models.EmailField(blank=True, default=None, max_length=255, null=True)),
                ('recovery_phone', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('secret_question', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('secret_response', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
