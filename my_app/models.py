from django.db import models

class User(models.Model):
    username = models.CharField(unique=True, max_length=30, null=False)
    email = models.CharField(unique=True, max_length=100, null=False)
    password = models.CharField(max_length=250, null=False)

    def __str__(self):
        return self.username


# Create your models here.
class Room(models.Model):
    
    roomNumber = models.BigIntegerField(null=False, unique=True )
    
    def __str__(self) -> str:
        return f"{self.id}"
    
    def __str__(self) -> str:
        return f"{self.roomNumber}"
    
    
class GameData(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    num_games_played = models.IntegerField(default=0)
    num_wins = models.IntegerField(default=0)
    num_draws = models.IntegerField(default=0)
    num_losses = models.IntegerField(default=0)

    class Meta:
        db_table = 'game_data'
    