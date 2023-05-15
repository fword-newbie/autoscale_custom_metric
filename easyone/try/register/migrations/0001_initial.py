# Generated by Django 3.2.9 on 2021-11-12 03:18

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='bloodduck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('systolic', models.CharField(max_length=30, null=True)),
                ('diastolic', models.CharField(max_length=30, null=True)),
                ('pulse', models.CharField(max_length=30, null=True)),
                ('recorded_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='bloodsugar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sugar', models.CharField(max_length=30, null=True)),
                ('time_period', models.CharField(choices=[(0, '晨起'), (1, '早餐前'), (2, '早餐後'), (3, '午餐前'), (4, '午餐後'), (5, '晚餐前'), (6, '晚餐後'), (7, '睡前')], max_length=2, null=True)),
                ('recorded_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='defult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sugar_delta_max', models.CharField(max_length=30, null=True)),
                ('sugar_delta_min', models.CharField(max_length=30, null=True)),
                ('sugar_morning_max', models.CharField(max_length=30, null=True)),
                ('sugar_morning_min', models.CharField(max_length=30, null=True)),
                ('sugar_evening_max', models.CharField(max_length=30, null=True)),
                ('sugar_evening_min', models.CharField(max_length=30, null=True)),
                ('sugar_before_max', models.CharField(max_length=30, null=True)),
                ('sugar_before_min', models.CharField(max_length=30, null=True)),
                ('sugar_after_max', models.CharField(max_length=30, null=True)),
                ('sugar_after_min', models.CharField(max_length=30, null=True)),
                ('systolic_max', models.CharField(max_length=30, null=True)),
                ('systolic_min', models.CharField(max_length=30, null=True)),
                ('diastolic_max', models.CharField(max_length=30, null=True)),
                ('diastolic_min', models.CharField(max_length=30, null=True)),
                ('pulse_max', models.CharField(max_length=30, null=True)),
                ('pulse_min', models.CharField(max_length=30, null=True)),
                ('weight_max', models.CharField(max_length=30, null=True)),
                ('weight_min', models.CharField(max_length=30, null=True)),
                ('bmi_max', models.CharField(max_length=30, null=True)),
                ('bmi_min', models.CharField(max_length=30, null=True)),
                ('body_fat_max', models.CharField(max_length=30, null=True)),
                ('body_fat_min', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='diet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=30, null=True)),
                ('meal', models.CharField(choices=[(0, '早餐'), (1, '午餐'), (2, '晚餐')], max_length=2, null=True)),
                ('tag', models.TextField(max_length=30, null=True)),
                ('image', models.IntegerField(null=True)),
                ('lat', models.CharField(max_length=1, null=True)),
                ('lng', models.CharField(max_length=30, null=True)),
                ('recorded_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('phone', models.CharField(max_length=30, null=True)),
                ('emailcheck', models.CharField(max_length=10, null=True)),
                ('emailcheckcode', models.CharField(max_length=30, null=True)),
                ('name', models.CharField(max_length=30, null=True)),
                ('birthday', models.CharField(max_length=30, null=True)),
                ('height', models.CharField(max_length=30, null=True)),
                ('gender', models.CharField(max_length=1, null=True)),
                ('fcm_id', models.CharField(max_length=30, null=True)),
                ('address', models.CharField(max_length=30, null=True)),
                ('token', models.CharField(default='$token', max_length=30)),
                ('fb_id', models.CharField(default=1, max_length=30, null=True)),
                ('group', models.CharField(max_length=30, null=True)),
                ('verified', models.CharField(default=1, max_length=30)),
                ('must_change_password', models.CharField(default=0, max_length=30)),
                ('badge', models.CharField(default=87, max_length=30)),
                ('status', models.CharField(default='Normal', max_length=30)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='weight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waight', models.CharField(max_length=30, null=True)),
                ('body_fat', models.CharField(max_length=30, null=True)),
                ('bmi', models.CharField(max_length=30, null=True)),
                ('recorded_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='news',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.TextField(max_length=30, null=True)),
                ('message', models.TextField(max_length=30, null=True)),
                ('pushed_at', models.TextField(max_length=30, null=True)),
                ('created_at', models.TextField(max_length=30, null=True)),
                ('updated_at', models.TextField(max_length=30, null=True)),
                ('member_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.people')),
            ],
        ),
        migrations.CreateModel(
            name='caremessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.TextField(max_length=30, null=True)),
                ('reply_id', models.TextField(max_length=30, null=True)),
                ('message', models.TextField(max_length=30, null=True)),
                ('created_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('member_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='register.people')),
            ],
        ),
    ]