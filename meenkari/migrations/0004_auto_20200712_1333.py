# Generated by Django 3.0.8 on 2020-07-12 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meenkari', '0003_auto_20200712_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_privacy',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='public', max_length=10),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_status',
            field=models.CharField(choices=[('empty', 'Empty'), ('united', 'United'), ('started', 'Started'), ('over', 'Over'), ('stopped', 'Stopped')], default='empty', max_length=10),
        ),
    ]
