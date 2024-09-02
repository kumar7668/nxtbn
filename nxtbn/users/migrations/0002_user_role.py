# Generated by Django 4.2.11 on 2024-09-02 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('CUSTOMER', 'Customer'), ('STAFF', 'Staff')], default='CUSTOMER', max_length=255),
        ),
    ]