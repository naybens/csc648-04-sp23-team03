# Generated by Django 3.2.12 on 2023-02-21 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('role', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('pronouns', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='member_images')),
            ],
        ),
    ]