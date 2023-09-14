# Generated by Django 4.1.2 on 2023-04-23 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_num', models.IntegerField()),
                ('permission_name', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=11, verbose_name='用戶名')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('gender', models.CharField(max_length=6)),
                ('birthday', models.DateField()),
                ('phone', models.CharField(max_length=10)),
                ('is_active', models.BooleanField(default=False, verbose_name='是否激活')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('user_permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userpermission')),
            ],
            options={
                'db_table': 'user_user_profile',
            },
        ),
    ]
