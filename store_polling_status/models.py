from django.db import models
from store_time_zone.models import Store
from pytz import timezone

# Create your models here.
class PollingStatus(models.IntegerChoices):
    INACTIVE = 0
    ACTIVE = 1


class PollingLogs(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="polling_status")
    status = models.IntegerField(choices=PollingStatus.choices)
    timestamp = models.DateTimeField(verbose_name="Time Stamp in UTC",null=True,blank=True)

    class Meta:
        db_table = "store_status"

    def get_local_timestamp(self):
        return self.timestamp.astimezone(timezone(self.store.timezone_str))
    
    def __str__(self):
        return f"{self.store.store_id} - {self.status} - {self.timestamp}"