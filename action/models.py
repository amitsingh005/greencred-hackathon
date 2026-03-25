from django.db import models
from django.contrib.auth.models import User

class Challenge(models.Model):
    ACTION_TYPES = [
        ('plant_tree', 'Plant Tree'),
        ('cycle_commute', 'Cycle Commute'),
        ('clean_area', 'Clean Area'),
        ('reduce_plastic', 'Reduce Plastic'),
    ]

    title = models.CharField(max_length=255)
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)

    credits_reward = models.IntegerField(default=50)
    valid_date = models.DateField()

    sponsor_brand = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class EcoAction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.SET_NULL, null=True, blank=True)

    action_type = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='actions/')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    credits_awarded = models.IntegerField(default=0)
    co2_kg_offset = models.FloatField(default=0.0)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    performed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action_type}"


class AIVerification(models.Model):
    STATUS_CHOICES = [
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('flagged', 'Flagged'),
    ]

    action = models.OneToOneField(EcoAction, on_delete=models.CASCADE)

    vision_confidence = models.FloatField(default=0.0)
    detected_labels = models.JSONField(default=list)

    verification_status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    duplicate_detected = models.BooleanField(default=False)
    gps_verified = models.BooleanField(default=False)

    verified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.verification_status}"