from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Player(models.Model):
    AGE_GROUPS = [
        ("U15", "Under 15"),
        ("U17", "Under 17"),
        ("U20", "Under 20"),
        ("U25", "Under 25"),
        ("+25", "Over 25"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    age_group = models.CharField(max_length=4, choices=AGE_GROUPS, default="U15")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='members')
    game = models.CharField(max_length=100, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class PlayerRegistration(models.Model):
    AGE_GROUPS = [
        ("U15", "Under 15"),
        ("U17", "Under 17"),
        ("U20", "Under 20"),
        ("U25", "Under 25"),
        ("+25", "Over 25"),
    ]

    WEIGHT_CATEGORIES = [
        ("Lightweight", "Lightweight (up to 60 kg)"),
        ("Middleweight", "Middleweight (61-80 kg)"),
        ("Heavyweight", "Heavyweight (81-100 kg)"),
        ("Super Heavyweight", "Super Heavyweight (over 100 kg)"),
    ]

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=255)
    player_email = models.EmailField()
    age_group = models.CharField(max_length=4, choices=AGE_GROUPS)
    weight_category = models.CharField(max_length=20, choices=WEIGHT_CATEGORIES)
    division = models.CharField(max_length=50, editable=False)

    class Meta:
        unique_together = ('tournament', 'player_email')

    def save(self, *args, **kwargs):
        self.division = f"{self.age_group} {self.weight_category}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.player_name} - {self.division}"
