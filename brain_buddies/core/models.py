from django.db import models
from django.contrib.auth.models import User

class MathChallenge(models.Model):
    question = models.CharField(max_length=255)
    answer = models.FloatField()
    difficulty = models.CharField(max_length=50)
    points = models.IntegerField(default=10)

    def __str__(self):
        return self.question
    
class ScienceChallenge(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50)
    points = models.IntegerField(default=10)

    def __str__(self):
        return self.question
    
class CoinTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} coins"
    
class Pet(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    evolution_stage = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} (Level {self.level})"
