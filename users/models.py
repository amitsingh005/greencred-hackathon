from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    green_credits = models.IntegerField(default=0)
    weekly_credits = models.IntegerField(default=0)

    total_co2_saved_kg = models.FloatField(default=0.0)
    streak_days = models.IntegerField(default=0)
    oauth_uid = models.CharField(max_length=255, default="default")
    trust_score = models.FloatField(default=1.0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name or self.user.username
    



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            full_name=instance.username,
            oauth_uid="default"
        )