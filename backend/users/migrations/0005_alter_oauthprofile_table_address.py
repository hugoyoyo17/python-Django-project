# Generated by Django 4.1.2 on 2023-05-15 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_oauthprofile_userprofile'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='oauthprofile',
            table='user_oauth_profile',
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.CharField(max_length=10, verbose_name='收件人')),
                ('receiver_phone', models.CharField(max_length=10, verbose_name='收件人手機')),
                ('address', models.CharField(max_length=50, verbose_name='收件地址')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile')),
            ],
            options={
                'db_table': 'user_address',
            },
        ),
    ]
