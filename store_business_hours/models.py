from django.db import models
from store_time_zone.models import Store

# Create your models here.
class dayOfWeek(models.IntegerChoices):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class BusinessHours(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="business_hours")
    day = models.IntegerField(choices=dayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = "business_hours"

    def __str__(self):
        return f"{self.store.store_id} - {self.day} - {self.start_time} - {self.end_time}"

