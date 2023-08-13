from django.db import models

# Create your models here.
class RunningStatus(models.IntegerChoices):
    PENDING = 0
    COMPLETED = 1

class Report(models.Model):
    report_id = models.CharField(max_length=50,null=False,blank=False)
    status = models.IntegerField(choices=RunningStatus.choices)
    csv_name = models.FileField(upload_to="reports",null=True,blank=True)