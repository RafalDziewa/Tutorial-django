# Generated by Django 3.2.3 on 2021-05-18 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyTestClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('choice_text_2', models.CharField(max_length=200)),
                ('votes_2', models.IntegerField(default=0)),
            ],
        ),
    ]
