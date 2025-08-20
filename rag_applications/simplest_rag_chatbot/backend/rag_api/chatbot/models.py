from django.db import models

# Create your models here.
class ChatHistory(models.Model):
    user_address = models.CharField(max_length=42)
    query = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    tx_hash = models.CharField(max_length=66, blank=True, null=True)

    def __str__(self):
        return f"{self.user_address}: {self.query[:50]}..."


