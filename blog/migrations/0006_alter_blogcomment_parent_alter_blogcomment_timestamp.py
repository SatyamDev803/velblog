# Generated by Django 5.1.3 on 2024-11-18 12:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_blogcomment_parent_alter_post_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='blog.blogcomment'),
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]