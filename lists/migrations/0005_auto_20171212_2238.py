# Generated by Django 2.0 on 2017-12-13 04:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('lists', '0004_item_list'),
    ]
    
    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('id',)},
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('list', 'text')},
        ),
    ]
