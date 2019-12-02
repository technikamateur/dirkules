from django.db import models


class SambaGlobal(models.Model):
    element = models.CharField(max_length=255)
    value = models.CharField(max_length=255)


class SambaShare(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    recycle = models.BooleanField()
    btrfs = models.BooleanField()
    enabled = models.BooleanField()


class SambaOption(models.Model):
    option = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    share = models.ForeignKey(SambaShare, on_delete=models.CASCADE)
