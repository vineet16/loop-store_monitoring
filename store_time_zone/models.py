from django.db import models

# Create your models here.
class Store(models.Model):
    store_id = models.CharField(max_length=50, primary_key=True)
    timezone_str = models.CharField(max_length=50,null=True,blank=True)

    class Meta:
        db_table = "store_time_zone"

    def __str__(self):
        return self.store_id