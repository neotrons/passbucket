from django.db import models

# Create your models here.


class Bucket(models.Model):
    name = models.CharField(max_length=100)
    user_account = models.CharField(max_length=255)
    password_account = models.CharField(max_length=255)
    recovery_email = models.EmailField(max_length=255, blank=True, null=True, default=None)
    recovery_phone = models.CharField(max_length=255, blank=True, null=True, default=None)
    secret_question = models.CharField(max_length=255, blank=True, null=True, default=None)
    secret_response = models.CharField(max_length=255, blank=True, null=True, default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
