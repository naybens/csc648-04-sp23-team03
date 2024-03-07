from django.db import models

from django.db import models

# Create your models here.
# name, role, description, pronouns, image, meetingSchedule, teamComms

class Member(models.Model):
    name = models.CharField(max_length=200, null=False)
    role = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=500)
    pronouns = models.CharField(max_length=100, null=False)
    image = models.ImageField(upload_to='member_images')

    def __str__(self):
        return self.name
