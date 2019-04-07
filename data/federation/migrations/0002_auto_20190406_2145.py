# Generated by Django 2.2 on 2019-04-07 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('federation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='federation',
            name='groups',
            field=models.ManyToManyField(related_name='federation_relations', to='group.Group'),
        ),
        migrations.AlterField(
            model_name='federation',
            name='networks',
            field=models.ManyToManyField(editable=False, related_name='federation_relations', to='network.Network'),
        ),
    ]
