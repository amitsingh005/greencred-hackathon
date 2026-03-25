from django.db import models
from django.contrib.auth.models import User

class Reward(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    required_credits = models.IntegerField(default=100)

    partner_brand = models.CharField(max_length=100, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class UserReward(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward, on_delete=models.CASCADE)

    redeemed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.reward.title}"