from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("storage_timestamps", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="timestamp",
            name="id",
            field=models.BigAutoField(
                primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
