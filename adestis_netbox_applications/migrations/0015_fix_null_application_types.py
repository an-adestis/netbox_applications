from django.db import migrations, models
import django.db.models.deletion

def fix_null_application_types(apps, schema_editor):
    InstalledApplication = apps.get_model("adestis_netbox_applications", "InstalledApplication")
    DEFAULT_APPLICATION_TYPE_ID = 1  # Standardwert (ID von `InstalledApplicationTypes`)

    # Null-Werte auf Standardwert setzen
    InstalledApplication.objects.filter(
        application_types__isnull=True
    ).update(application_types_id=DEFAULT_APPLICATION_TYPE_ID)

class Migration(migrations.Migration):

    dependencies = [
        ('adestis_netbox_applications', '0014_alter_installedapplication_options_and_more'),
    ]

    operations = [
        migrations.RunPython(fix_null_application_types),
        migrations.AlterField(
            model_name='installedapplication',
            name='application_types',
            field=models.ForeignKey(
                null=False,
                default=1,  # default nur für neue Datensätze
                on_delete=django.db.models.deletion.PROTECT,
                related_name='applications',
                to='adestis_netbox_applications.installedapplicationtypes'
            ),
        ),
    ]
