from django.db import models
from users.models import User  
from datetime import timedelta

class LoginLog(models.Model):
    id = models.AutoField(primary_key=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    login_at = models.DateTimeField(auto_now_add=True)  
    session_end = models.DateTimeField(null=True, blank=True)  
    logout_reason = models.CharField(max_length=255, null=True, blank=True)  
    session_duration = models.DurationField(null=True, blank=True)  

    def save(self, *args, **kwargs):
        if not self.session_end:
            self.session_end = self.login_at + timedelta(hours=6)
            self.logout_reason = 'session ended'

        if self.session_end and self.login_at:
            self.session_duration = self.session_end - self.login_at

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.login_at}"
