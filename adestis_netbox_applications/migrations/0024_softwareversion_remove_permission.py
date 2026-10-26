from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adestis_netbox_applications', '0023_alter_software_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='softwareversion',
            options={
                'ordering': ('name',),
                'permissions': [
                    ('remove', 'Remove software versions from applications'),
                ],
                'verbose_name': 'Software Version',
                'verbose_name_plural': 'Software Versions',
            },
        ),
    ]
