# Generated by Django 4.2.17 on 2025-01-07 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_remove_team_players_player_category_player_game_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_name', models.CharField(max_length=255)),
                ('player_email', models.EmailField(max_length=254)),
                ('player_age', models.IntegerField()),
                ('player_game', models.CharField(max_length=255)),
                ('player_weight_category', models.CharField(max_length=255)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.tournament')),
            ],
        ),
    ]
