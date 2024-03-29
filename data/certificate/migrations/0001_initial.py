# Generated by Django 3.2.5 on 2021-07-13 07:03

from django.db import migrations, models
import django.db.models.deletion
import systems.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('network', '0001_initial'),
        ('domain', '0001_initial'),
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('created', models.DateTimeField(editable=False, null=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('id', models.CharField(editable=False, max_length=64, primary_key=True, serialize=False)),
                ('name', models.CharField(editable=False, max_length=256)),
                ('config', systems.models.fields.EncryptedDataField(default={}, editable=False)),
                ('provider_type', models.CharField(editable=False, max_length=128, null=True)),
                ('variables', systems.models.fields.EncryptedDataField(default={}, editable=False)),
                ('state_config', systems.models.fields.EncryptedDataField(default={}, editable=False)),
                ('private_key', systems.models.fields.EncryptedDataField(null=True)),
                ('certificate', systems.models.fields.EncryptedDataField(null=True)),
                ('chain', systems.models.fields.EncryptedDataField(null=True)),
                ('domain', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='certificate_relation', to='domain.domain')),
                ('groups', models.ManyToManyField(related_name='certificate_relations', to='group.Group')),
                ('network', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='certificate_relation', to='network.network')),
            ],
            options={
                'verbose_name': 'certificate',
                'verbose_name_plural': 'certificates',
                'db_table': 'cluster_certificate',
                'ordering': ['name'],
                'abstract': False,
                'unique_together': {('network', 'name')},
            },
        ),
    ]
