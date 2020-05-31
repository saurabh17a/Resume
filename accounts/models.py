from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    user_type = [("Candidate", "Candidate"), ("Recruiter", "Recruiter")]
    user_types = models.CharField(
        choices=user_type, default="Candidate", max_length=10)
