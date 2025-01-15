# Generated by Django 5.1.4 on 2025-01-11 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('email', models.EmailField(max_length=400)),
                ('mobile', models.CharField(max_length=13)),
                ('subject', models.CharField(max_length=400)),
                ('content', models.TextField(max_length=400)),
            ],
        ),
    ]
