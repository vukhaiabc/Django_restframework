# Generated by Django 3.2.5 on 2021-09-24 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_alter_lesson_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, related_name='tags', to='courses.Tag'),
        ),
    ]
