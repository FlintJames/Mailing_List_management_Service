# Generated by Django 4.2.2 on 2024-06-30 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0003_client_owner_mailing_owner_message_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='periodicity',
            field=models.CharField(choices=[('daily', 'Один раз в день'), ('weekly', 'Один раз в неделю'), ('monthly', 'Один раз в месяц')], max_length=100, verbose_name='Периодичность'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='status',
            field=models.CharField(choices=[('created', 'Создана'), ('completed', 'Завершена'), ('started', 'Запущена')], max_length=100, verbose_name='Статус'),
        ),
    ]
