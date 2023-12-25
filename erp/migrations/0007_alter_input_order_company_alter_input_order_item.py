# Generated by Django 4.2.5 on 2023-10-18 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0006_alter_input_order_company_alter_input_order_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='input_order',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='erp.company'),
        ),
        migrations.AlterField(
            model_name='input_order',
            name='item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='erp.item'),
        ),
    ]
