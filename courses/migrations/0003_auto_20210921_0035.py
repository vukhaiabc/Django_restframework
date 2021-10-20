# Generated by Django 3.2.5 on 2021-09-20 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20210920_2339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, to='courses.Tag'),
        ),
    ]
