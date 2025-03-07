from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Election(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    party = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.party})"

class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    college_id = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.voter.username} voted for {self.candidate.name}"
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college_id = models.CharField(max_length=20, unique=True, blank=True, null=True)  # Allow blank/null initially
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.college_id}"

# ✅ Fix: No need to import UserProfile above
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
