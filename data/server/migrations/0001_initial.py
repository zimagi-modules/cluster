# Generated by Django 3.2.5 on 2021-07-13 07:03

from django.db import migrations, models
import django.db.models.deletion
import systems.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('firewall', '0001_initial'),
        ('domain', '0001_initial'),
        ('group', '0001_initial'),
        ('subnet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('created', models.DateTimeField(editable=False, null=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('id', models.CharField(editable=False, max_length=64, primary_key=True, serialize=False)),
                ('name', models.CharField(editable=False, max_length=256)),
                ('config', systems.models.fields.EncryptedDataField(default={}, editable=False)),
                ('provider_type', models.CharField(editable=False, max_length=128, null=True)),
                ('variables', systems.models.fields.EncryptedDataField(default={}, editable=False)),
                ('state_config', systems.models.fields.EncryptedDataField(default={}, editable=False)),
                ('public_ip', models.CharField(max_length=128, null=True)),
                ('private_ip', models.CharField(max_length=128, null=True)),
                ('ssh_port', models.IntegerField(default=22)),
                ('user', models.CharField(max_length=128, null=True)),
                ('password', systems.models.fields.EncryptedCharField(max_length=1096, null=True)),
                ('private_key', systems.models.fields.EncryptedDataField(null=True)),
                ('domain_name', models.CharField(max_length=128, null=True)),
                ('domain', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='server_relation', to='domain.domain')),
                ('firewalls', models.ManyToManyField(related_name='server_relations', to='firewall.Firewall')),
                ('groups', models.ManyToManyField(related_name='server_relations', to='group.Group')),
                ('subnet', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='server_relation', to='subnet.subnet')),
            ],
            options={
                'verbose_name': 'server',
                'verbose_name_plural': 'servers',
                'db_table': 'cluster_server',
                'ordering': ['name'],
                'abstract': False,
                'unique_together': {('subnet', 'name')},
            },
        ),
    ]
