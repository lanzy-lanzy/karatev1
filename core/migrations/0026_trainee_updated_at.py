# Generated migration for adding updated_at field to Trainee model

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_beltrankprogress_new_belt_rank_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainee',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
