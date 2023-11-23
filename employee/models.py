from django.db import models
from django.core.validators import MinValueValidator
from company.models import JobOffer
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    applied_jobs = models.ManyToManyField(JobOffer, related_name='applicants', blank=True)
    resume = models.FileField(upload_to='applicant_resumes/', blank=True, null=True)

    def __str__(self):
        return self.user.username