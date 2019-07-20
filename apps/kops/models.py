from django.db import models
class Pod(models.Model):
    pod_name = models.CharField(max_length=100)
    pod_status = models.CharField(max_length=100)
    pod_namespace = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)

