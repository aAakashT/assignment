from django.db import models

# Create your models here.

class BlacklistedToken(models.Model):
    token = models.CharField(max_length = 500)
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.token
