# Generated by Django 3.2.9 on 2021-11-15 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0017_setting'),
    ]

    operations = [
        migrations.CreateModel(
            name='badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badge', models.CharField(default=87, max_length=30)),
            ],
        ),
    ]