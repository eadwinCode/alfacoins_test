# Generated by Django 2.2.7 on 2019-11-18 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alfacoins_model', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawaltransaction',
            name='commission',
            field=models.FloatField(default=0, verbose_name='Commission'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='withdrawaltransaction',
            name='network_fee',
            field=models.FloatField(default=0, verbose_name='Commission'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='withdrawaltransaction',
            name='tx_id',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='tx_id'),
        ),
    ]