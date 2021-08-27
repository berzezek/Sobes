# Generated by Django 2.2.1 on 2021-08-26 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0002_answernumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='owner',
        ),
        migrations.AddField(
            model_name='answer',
            name='answer_numbers',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='interview.AnswerNumber', to_field='number'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answernumber',
            name='number',
            field=models.IntegerField(unique=True),
        ),
    ]
