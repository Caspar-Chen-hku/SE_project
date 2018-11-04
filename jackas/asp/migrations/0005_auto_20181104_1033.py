# Generated by Django 2.1.3 on 2018-11-04 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asp', '0004_auto_20181104_1017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clinic',
            name='manager_id',
        ),
        migrations.AddField(
            model_name='user',
            name='clinic_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clinic_id', to='asp.Clinic'),
        ),
        migrations.AlterField(
            model_name='order',
            name='canceled_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='dilivered_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='dispatching_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='processing_time',
            field=models.DateTimeField(null=True),
        ),
    ]