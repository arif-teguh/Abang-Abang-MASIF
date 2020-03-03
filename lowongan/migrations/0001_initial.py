# Generated by Django 3.0 on 2020-02-29 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lowongan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=100)),
                ('penyedia', models.CharField(max_length=100)),
                ('jumlah_tersedia', models.IntegerField()),
                ('durasi_magang', models.IntegerField()),
                ('jangka_waktu_lamaran', models.IntegerField()),
                ('berkas', models.CharField(max_length=100)),
                ('deskripsi', models.TextField(max_length=1000)),
                ('requirement', models.TextField(max_length=1000)),
                ('opd_foreign_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
        ),
    ]
