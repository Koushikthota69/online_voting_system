from django.db import models
from django.contrib.auth.models import User

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
    college_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.voter.username} voted for {self.candidate.name}"
