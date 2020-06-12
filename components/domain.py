from systems.commands import profile


class ProfileComponent(profile.BaseProfileComponent):

    def priority(self):
        return 2

    def run(self, name, config):
        provider = self.pop_value('provider', config)
        records = self.pop_info('records', config)
        groups = self.pop_values('groups', config)

        if not provider:
            self.command.error("Domain {} requires 'provider' field".format(name))

        self.exec('domain save',
            domain_provider_name =  provider,
            domain_name = name,
            domain_fields = self.interpolate(config,
                provider = provider
            ),
            group_names = groups,
            test = self.test
        )
        def process_record(record):
            self.exec('domain record save',
                domain_name = name,
                domain_record_name = record,
                domain_record_fields = self.interpolate(records[record],
                    domain = name
                ),
                test = self.test
            )
        if records and self.profile.include_inner('domain_record'):
            self.run_list(records.keys(), process_record)

    def variables(self, instance):
        variables = {
            'provider': instance.provider_type,
            'groups': self.get_names(instance.groups),
            'records': {}
        }
        for record in instance.domainrecord_relation.all():
            variables['records'][record.name] = self.get_variables(record)

        return variables

    def destroy(self, name, config):
        self.exec('domain remove',
            domain_name = name,
            force = True
        )
