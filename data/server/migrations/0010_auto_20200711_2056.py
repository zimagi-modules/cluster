# Generated by Django 3.0 on 2020-07-12 00:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0009_auto_20200605_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='load_balancer',
        ),
        migrations.RemoveField(
            model_name='server',
            name='load_balancer_listeners',
        ),
    ]