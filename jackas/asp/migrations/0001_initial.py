# Generated by Django 2.1.2 on 2018-11-03 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinic_name', models.CharField(max_length=100)),
                ('clinic_address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='DispatchQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=150)),
                ('item_description', models.CharField(max_length=250)),
                ('photo_url', models.CharField(max_length=200)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('priority', models.IntegerField(choices=[(1, 'High'), (2, 'Medium'), (3, 'Low')], default=1)),
                ('status', models.CharField(choices=[('QFP', 'Queued for Processing'), ('PBW', 'Processing by Warehouse'), ('QFD', 'Queued for Dispatch'), ('DI', 'Dispatched'), ('DE', 'Delivered'), ('CA', 'Canceled')], default='QFP', max_length=3)),
                ('placing_time', models.DateTimeField()),
                ('processing_time', models.DateTimeField()),
                ('dispatching_time', models.DateTimeField()),
                ('dilivered_time', models.DateTimeField()),
                ('canceled_time', models.DateTimeField()),
                ('destination', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='OrderContainsItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asp.Item')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asp.Order')),
            ],
        ),
        migrations.CreateModel(
            name='PriorityQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asp.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_string', models.CharField(max_length=6)),
                ('user_role', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50)),
                ('role', models.CharField(choices=[['CM', 'Clinic Manager'], ['WP', 'Warehouse Personnel'], ['D', 'Dispacher']], default='CM', max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='dispatcher_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dispatcher_id', to='asp.User'),
        ),
        migrations.AddField(
            model_name='order',
            name='owner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_id', to='asp.User'),
        ),
        migrations.AddField(
            model_name='order',
            name='processor_id',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='processor_id', to='asp.User'),
        ),
        migrations.AddField(
            model_name='dispatchqueue',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asp.Order'),
        ),
    ]
