# Generated by Django 4.2.11 on 2024-11-01 02:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_order_order_source'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDeviceMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(blank=True, help_text='IP address of the user when placing the order.', null=True)),
                ('user_agent', models.TextField(blank=True, help_text="Browser's user-agent string for identifying the browser and device.", null=True)),
                ('browser', models.CharField(blank=True, help_text='Browser name extracted from the user-agent.', max_length=100, null=True)),
                ('browser_version', models.CharField(blank=True, help_text='Browser version extracted from the user-agent.', max_length=50, null=True)),
                ('operating_system', models.CharField(blank=True, help_text='Operating system of the device.', max_length=100, null=True)),
                ('device_type', models.CharField(blank=True, help_text='Device type (e.g., Mobile, Desktop, Tablet).', max_length=50, null=True)),
                ('order', models.OneToOneField(help_text='Related order for which this device metadata is recorded.', on_delete=django.db.models.deletion.CASCADE, related_name='device_meta', to='order.order')),
            ],
            options={
                'verbose_name': 'Order Device Metadata',
                'verbose_name_plural': 'Order Device Metadata',
            },
        ),
    ]
