from django.db import models


from django.contrib.auth.models import User

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    videoid= models.CharField(max_length=100,primary_key=True)
    positive_count= models.CharField(max_length=100)
    neutral_count= models.CharField(max_length=100)
    negative_count= models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username} - {self.videoid}'