# Generated by Django 2.2.4 on 2019-09-04 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_librocopia_prestatario'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='librocopia',
            options={'ordering': ['fecha_devolucion'], 'permissions': (('puede_marcar_devuelto', 'Establecer libro como devuelto'),)},
        ),
    ]