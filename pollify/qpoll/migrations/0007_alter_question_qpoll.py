# Generated by Django 4.2 on 2023-04-08 21:59
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qpoll', '0006_remove_qpoll_publication_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='qpoll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='qpoll.qpoll'),
        ),
    ]
