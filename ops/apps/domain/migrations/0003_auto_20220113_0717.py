# Generated by Django 2.1.8 on 2022-01-13 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0002_dmmodel_looks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dmmodel',
            name='group',
            field=models.ForeignKey(help_text='所属域名组', on_delete=django.db.models.deletion.CASCADE, to='domain.DmGroupsModel', verbose_name='所属域名组'),
        ),
        migrations.AlterField(
            model_name='dmmodel',
            name='looks',
            field=models.PositiveIntegerField(default=0, help_text='访问量', verbose_name='访问量'),
        ),
    ]
